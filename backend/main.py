from fastapi import FastAPI, Request, Form, HTTPException, Body, Cookie, File, UploadFile, Depends
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from class_module import *
import ZODB, ZODB.FileStorage
import transaction
import markdown

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
clients = root.clients

client = clients[1001]

app = FastAPI()
templates = Jinja2Templates(directory="../templates")
app.mount("/css", StaticFiles(directory="../statics/css"), name="css")
app.mount("/images", StaticFiles(directory="../statics/images"), name="images")
app.mount("/js", StaticFiles(directory="../statics/js"), name="js")
app.mount("/Upload", StaticFiles(directory="Upload"), name="Upload")

templates.env.globals["generate_uuid"] = generate_uuid

@app.get("/", response_class=HTMLResponse)
def index(request: Request, ID: int = Cookie(None), client_type: str = Cookie(None)):
    # print(f"Retrieved ID: {ID}, client_type: {client_type}")  # Debugging
    
    if ID is None or client_type is None or ID not in clients:
        return templates.TemplateResponse("index.html", {"request": request, "client": None})

    client = clients[ID]
    # print(f"Client found: {client}")  # Debugging

    first_course_id = None
    if client_type == "Lecturer" and client.courses:
        first_course_id = client.courses[0].course_id
    elif client_type == "Student" and client.enrolls:
        first_course_id = client.enrolls[0].course.course_id

    return templates.TemplateResponse("index.html", {
        "request": request,
        "client": client,
        "first_course_id": first_course_id,
    })

@app.get("/users/all")
def get_all_users():
    return {"clients": list(clients.keys())}

@app.post("/login")
async def set_login(request: Request, response: Response, ID: int = Form(...), password: str = Form(...)):
    if ID in clients.keys():
        if clients[ID].login(ID, password):
            client = clients[ID]
            client_type = "None"
            if type(client) == Lecturer:
                client_type = "Lecturer"
                first_course_id = client.courses[0].course_id
            elif type(client) == Student:
                client_type = "Student"
                first_course_id = client.enrolls[0].course.course_id
            response = RedirectResponse(url="/classes/{}/assignments".format(first_course_id), status_code=303)
            response.set_cookie(key="ID", value=ID)
            response.set_cookie(key="client_type", value=client_type)
            response.set_cookie(key="first_course_id", value=first_course_id)
            return response
        else:
            return RedirectResponse(url="/login?error=1", status_code=303)
    else: 
        return RedirectResponse(url="/login?error=1", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, error: int = 0):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.get("/classes/{course_id}/assignments", response_class=HTMLResponse)
async def get_classes(request: Request, course_id: int, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    if ID == None or client_type == None:
        return RedirectResponse(url="/", status_code=303)
    
    client = clients[ID]
    course = root.courses[course_id]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "client_type": client_type,
        "first_course_id": first_course_id,
    }
    
    return templates.TemplateResponse("classes.html", data)
    
@app.get("/classes/{course_id}/announcements", response_class=HTMLResponse)
async def get_classes(request: Request, course_id: int, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    if ID == None or client_type == None:
        return RedirectResponse(url="/", status_code=303)
    
    client = clients[ID]
    course = root.courses[course_id]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "client_type": client_type,
        "first_course_id": first_course_id,
    }
    
    return templates.TemplateResponse("classes2.html", data)

@app.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="ID")
    return response

@app.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    client = clients[ID]
    return templates.TemplateResponse("profile.html", {"request": request, "client": client, "first_course_id": first_course_id})

@app.post("/profile")
async def set_profile(request: Request, ID: int = Cookie(None), name: str = Form(...), user_name: str = Form(...), avatar: UploadFile = File(...)):
    UPLOAD_DIR = "Upload"
    client = clients[ID]
    client.setName(name)
    client.setUsername(user_name)
    data = await avatar.read()
    try:
        saveas = UPLOAD_DIR + "/" + avatar.filename
        with open(saveas, 'wb') as f:
            f.write(data)
        saveas = "/" + UPLOAD_DIR + "/" + avatar.filename
        client.setAvatar(saveas)
    except:
        pass
    return RedirectResponse(url="/profile", status_code=303)

@app.get("/classes/{course_id}/assignments/{assignment_id}", response_class=HTMLResponse)
async def get_assignment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    
    if ID == None or client_type == None:
        return RedirectResponse(url="/", status_code=303)

    try:
        course = root.courses[course_id]
        assignment = root.assignments[assignment_id]
    except:
        return RedirectResponse(url="/", status_code=303)
    
    if assignment not in course.assignments:
        print("not in course")
        return RedirectResponse(url="/", status_code=303)
    
    client = clients[ID]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "client_type": client_type, 
        "assignment": assignment, 
        "ID": ID,
        "first_course_id": first_course_id
    }

    return templates.TemplateResponse("assignment.html", data)

@app.post("/uploadFile/{course_id}/{ASS_ID}")
async def upload_file(request: Request, course_id: int, ASS_ID: str, assignmentFiles: List[UploadFile] = File(None), ID: int = Cookie(None)):
    
    try:
        course = root.courses[course_id]
        assignment = root.assignments[ASS_ID]
    except:
        print("Error")
        return RedirectResponse(url="/", status_code=303)
    
    if assignment not in course.assignments:
        print("Not in course")
        return RedirectResponse(url="/", status_code=303)
    
    UPLOAD_DIR = "Upload"
    summitfiles = []
    
    if assignmentFiles[0].filename != "":
        for file in assignmentFiles:
            data = await file.read()
            saveas = UPLOAD_DIR + "/" + file.filename
            with open(saveas, 'wb') as f:
                f.write(data)
            summitfiles.append(saveas)
        
    student = root.clients[ID]
    assignment = root.assignments[ASS_ID]
    assignment.summitWork(ID, summitfiles)
    print(assignment.submitted_work, summitfiles)
    return RedirectResponse("/classes/{}/assignments/{}".format(course_id, ASS_ID), status_code=303)

@app.get("/unsubmit/{course_id}/{ASS_ID}")
async def upload_file(request: Request, course_id: int, ASS_ID: str, ID: int = Cookie(None)):

    student = root.clients[ID]
    assignment = root.assignments[ASS_ID]
    assignment.unSummitWork(ID)
    
    return RedirectResponse("/classes/{}/assignments/{}".format(course_id, assignment.id), status_code=303)

@app.get("/classes/{course_id}/addAssignment", response_class=HTMLResponse)
async def add_Assignment(request: Request, course_id: int, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    client = clients[ID]
    course = root.courses[course_id]
    assignments = course.assignments
    new_id = None

    while True:
        new_id = generate_uuid()
        if not any(new_id == assignment.id for assignment in assignments):
            break

    due_date = str(date.today())
    assignment_index = len(assignments)
    new_assignment = Assignment(new_id, "Assignment {}".format(assignment_index + 1), 10, due_date)
    root.assignments[new_assignment.id] = new_assignment
    course.addAssignment(root.assignments[new_assignment.id])
    # for i in assignments:
    #     print(i)
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "assignment": new_assignment, 
        "client_type": client_type, 
        "first_course_id": first_course_id,
        "ID": ID
    }
        
    return templates.TemplateResponse("edit_assignment.html", data)

@app.get("/classes/{course_id}/editAssignment/{assignment_id}", response_class=HTMLResponse)
async def edit_Assignment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    client = clients[ID]
    assignment = root.assignments[assignment_id]
    course = root.courses[course_id]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course,
        "client_type": client_type, 
        "assignment": assignment, 
        "ID": ID,
        "first_course_id": first_course_id,
    }
    
    return templates.TemplateResponse("edit_assignment.html", data)

@app.get("/classes/{course_id}/removeAssignment/{assignment_id}")
async def remove_assignment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None)):
    client = clients[ID]
    course = root.courses[course_id]
    try:
        assignment = root.assignments[assignment_id]
    except KeyError:
        IncorrectAssignments = course.assignments
        for i in IncorrectAssignments:
            if i.id == assignment_id:
                IncorrectAssignments.p
        return RedirectResponse("/classes/{}/assignments".format(course_id), status_code=303)
    
    if course.removeAssignment(assignment):
        root.assignments.pop(assignment_id)
        root._p_changed = True
    
    return RedirectResponse("/classes/{}/assignments".format(course_id), status_code=303)

@app.post("/classes/{course_id}/editAssignment/{assignment_id}")
async def save_Edit_Assignment(request: Request, course_id: int, assignment_id: str, name: str = Form(...), due_date: str = Form(...), description: str = Form(...), attachmentFiles: List[UploadFile] = File(None), ID: int = Cookie(None), client_type: str = Cookie(None)):
    client = clients[ID]
    assignment = root.assignments[assignment_id]
    assignment.setName(name)
    assignment.setDueDate(due_date)
    assignment.setDescription(description)
    # set attachment
    UPLOAD_DIR = "Upload"
    summitfiles = []
    
    # print(assignment.attachment)
    if attachmentFiles != None :
        try:
            for file in attachmentFiles:
                data = await file.read()
                saveas = UPLOAD_DIR + "/" + file.filename
                with open(saveas, 'wb') as f:
                    f.write(data)
                summitfiles.append(saveas)
            
            assignment.setAttachment(summitfiles)
        except:
            pass
        
    return RedirectResponse("/classes/{}/assignments".format(course_id), status_code=303)


@app.get("/classes/{course_id}/editAssignment/{assignment_id}/removeAttachment")
async def remove_attachment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None)):
    
    client = root.clients[ID]
    assignment = root.assignments[assignment_id]
    assignment.removeAttachment()

    return RedirectResponse("/classes/{}/editAssignment/{}".format(course_id, assignment_id), status_code=303)

@app.get("/classes/{course_id}/assignments/{assignment_id}", response_class=HTMLResponse)
async def get_assignment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    
    if ID == None or client_type == None:
        return RedirectResponse(url="/", status_code=303)

    try:
        course = root.courses[course_id]
        assignment = root.assignments[assignment_id]
    except:
        return RedirectResponse(url="/", status_code=303)
    
    if assignment not in course.assignments:
        print("not in course")
        return RedirectResponse(url="/", status_code=303)
    
    client = clients[ID]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "client_type": client_type, 
        "assignment": assignment, 
        "ID": ID,
        "first_course_id": first_course_id
    }

    return templates.TemplateResponse("assignment.html", data)

@app.post("/uploadFile/{course_id}/{ASS_ID}")
async def upload_file(request: Request, course_id: int, ASS_ID: str, assignmentFiles: List[UploadFile] = File(None), ID: int = Cookie(None)):
    
    try:
        course = root.courses[course_id]
        assignment = root.assignments[ASS_ID]
    except:
        print("Error")
        return RedirectResponse(url="/", status_code=303)
    
    if assignment not in course.assignments:
        print("Not in course")
        return RedirectResponse(url="/", status_code=303)
    
    UPLOAD_DIR = "Upload"
    summitfiles = []
    
    if assignmentFiles[0].filename != "":
        for file in assignmentFiles:
            data = await file.read()
            saveas = UPLOAD_DIR + "/" + file.filename
            with open(saveas, 'wb') as f:
                f.write(data)
            summitfiles.append(saveas)
        
    student = root.clients[ID]
    assignment = root.assignments[ASS_ID]
    assignment.summitWork(ID, summitfiles)
    print(assignment.submitted_work, summitfiles)
    return RedirectResponse("/classes/{}/assignments/{}".format(course_id, ASS_ID), status_code=303)

@app.get("/unsubmit/{course_id}/{ASS_ID}")
async def upload_file(request: Request, course_id: int, ASS_ID: str, ID: int = Cookie(None)):

    student = root.clients[ID]
    assignment = root.assignments[ASS_ID]
    assignment.unSummitWork(ID)
    
    return RedirectResponse("/classes/{}/assignments/{}".format(course_id, assignment.id), status_code=303)

@app.get("/classes/{course_id}/addAssignment", response_class=HTMLResponse)
async def add_Assignment(request: Request, course_id: int, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    client = clients[ID]
    course = root.courses[course_id]
    assignments = course.assignments
    new_id = None

    while True:
        new_id = generate_uuid()
        if not any(new_id == assignment.id for assignment in assignments):
            break

    due_date = str(date.today())
    assignment_index = len(assignments)
    new_assignment = Assignment(new_id, "Assignment {}".format(assignment_index + 1), 10, due_date)
    root.assignments[new_assignment.id] = new_assignment
    course.addAssignment(root.assignments[new_assignment.id])
    # for i in assignments:
    #     print(i)
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "assignment": new_assignment, 
        "client_type": client_type, 
        "first_course_id": first_course_id,
        "ID": ID
    }
        
    return templates.TemplateResponse("edit_assignment.html", data)

@app.get("/classes/{course_id}/editAssignment/{assignment_id}", response_class=HTMLResponse)
async def edit_Assignment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    client = clients[ID]
    assignment = root.assignments[assignment_id]
    course = root.courses[course_id]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course,
        "client_type": client_type, 
        "assignment": assignment, 
        "ID": ID,
        "first_course_id": first_course_id,
    }
    
    return templates.TemplateResponse("edit_assignment.html", data)

@app.get("/classes/{course_id}/removeAssignment/{assignment_id}")
async def remove_assignment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None)):
    client = clients[ID]
    course = root.courses[course_id]
    try:
        assignment = root.assignments[assignment_id]
    except KeyError:
        IncorrectAssignments = course.assignments
        for i in IncorrectAssignments:
            if i.id == assignment_id:
                IncorrectAssignments.p
        return RedirectResponse("/classes/{}/assignments".format(course_id), status_code=303)
    
    if course.removeAssignment(assignment):
        root.assignments.pop(assignment_id)
        root._p_changed = True
    
    return RedirectResponse("/classes/{}/assignments".format(course_id), status_code=303)

@app.post("/classes/{course_id}/editAssignment/{assignment_id}")
async def save_Edit_Assignment(request: Request, course_id: int, assignment_id: str, name: str = Form(...), due_date: str = Form(...), description: str = Form(...), attachmentFiles: List[UploadFile] = File(None), ID: int = Cookie(None), client_type: str = Cookie(None)):
    client = clients[ID]
    assignment = root.assignments[assignment_id]
    assignment.setName(name)
    assignment.setDueDate(due_date)
    assignment.setDescription(description)
    # set attachment
    UPLOAD_DIR = "Upload"
    summitfiles = []
    
    print(assignment.attachment)
    if attachmentFiles != None :
        try:
            for file in attachmentFiles:
                data = await file.read()
                saveas = UPLOAD_DIR + "/" + file.filename
                with open(saveas, 'wb') as f:
                    f.write(data)
                summitfiles.append(saveas)
            
            assignment.setAttachment(summitfiles)
        except:
            pass
        
    return RedirectResponse("/classes/{}/assignments".format(course_id), status_code=303)


@app.get("/classes/{course_id}/editAssignment/{assignment_id}/removeAttachment")
async def remove_attachment(request: Request, course_id: int, assignment_id: str, ID: int = Cookie(None)):
    
    client = root.clients[ID]
    assignment = root.assignments[assignment_id]
    assignment.removeAttachment()

    return RedirectResponse("/classes/{}/editAssignment/{}".format(course_id, assignment_id), status_code=303)

# =================
@app.get("/classes/{course_id}/announcements/{announcement_id}", response_class=HTMLResponse)
async def get_announcement(request: Request, course_id: int, announcement_id: str, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    
    if ID is None or client_type is None:
        return RedirectResponse(url="/", status_code=303)

    try:
        course = root.courses[course_id]
        announcement = root.announcements[announcement_id]
    except KeyError:
        return RedirectResponse(url="/", status_code=303)
    
    if announcement not in course.announcements:
        return RedirectResponse(url="/", status_code=303)
    
    client = root.clients[ID]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "client_type": client_type, 
        "announcement": announcement, 
        "ID": ID,
        "first_course_id": first_course_id
    }

    return templates.TemplateResponse("announcements.html", data)

@app.post("/uploadFile/{course_id}/{ANN_ID}")
async def upload_file(request: Request, course_id: int, ANN_ID: str, assignmentFiles: List[UploadFile] = File(None), ID: int = Cookie(None)):
    
    try:
        course = root.courses[course_id]
        assignment = root.assignments[ANN_ID]
    except KeyError:
        return RedirectResponse(url="/", status_code=303)
    
    if assignment not in course.assignments:
        return RedirectResponse(url="/", status_code=303)
    
    UPLOAD_DIR = "Upload"
    summitfiles = []
    
    if assignmentFiles:
        for file in assignmentFiles:
            data = await file.read()
            saveas = f"{UPLOAD_DIR}/{file.filename}"
            with open(saveas, 'wb') as f:
                f.write(data)
            summitfiles.append(saveas)
        
    student = root.clients[ID]
    announcement = root.announcements[ANN_ID]
    announcement.summitWork(ID, summitfiles)
    
    return RedirectResponse(f"/classes/{course_id}/announcements/{ANN_ID}", status_code=303)

@app.get("/unsubmit/{course_id}/{ANN_ID}")
async def unsubmit_assignment(request: Request, course_id: int, ANN_ID: str, ID: int = Cookie(None)):

    student = root.clients[ID]
    announcement = root.announcements[ANN_ID]
    announcement.unSummitWork(ID)
    
    return RedirectResponse(f"/classes/{course_id}/announcements/{ANN_ID}", status_code=303)

@app.get("/classes/{course_id}/addAnnouncement", response_class=HTMLResponse)
async def add_announcement(request: Request, course_id: int, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    client = root.clients[ID]
    course = root.courses[course_id]
    announcements = course.getAnnouncements()

    # Ensure announcements is initialized
    if not hasattr(root, 'announcements'):
        root.announcements = {}

    new_id = generate_uuid()

    while any(new_id == announcement.id for announcement in announcements):
        new_id = generate_uuid()

    this_date = str(date.today())
    announcement_index = len(announcements)
    new_announcement = Announcement(new_id, f"Announcement {announcement_index + 1}", this_date)

    # Add the new announcement to the root
    root.announcements[new_announcement.id] = new_announcement

    # Add the new announcement to the course
    course.addAnnouncement(new_announcement)
    
    # Commit changes to the database
    root._p_changed = True
    
    data = {
        "request": request, 
        "client": client, 
        "course": course, 
        "announcement": new_announcement, 
        "client_type": client_type, 
        "first_course_id": first_course_id,
        "ID": ID
    }
        
    return templates.TemplateResponse("edit_announcement.html", data)

@app.get("/classes/{course_id}/editAnnouncement/{announcement_id}", response_class=HTMLResponse)
async def edit_announcement(request: Request, course_id: int, announcement_id: str, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    client = root.clients[ID]
    announcement = root.announcements[announcement_id]
    course = root.courses[course_id]
    
    data = {
        "request": request, 
        "client": client, 
        "course": course,
        "client_type": client_type, 
        "announcement": announcement, 
        "ID": ID,
        "first_course_id": first_course_id,
    }
    
    return templates.TemplateResponse("edit_announcement.html", data)

@app.get("/classes/{course_id}/removeAnnouncement/{announcement_id}")
async def remove_announcement(request: Request, course_id: int, announcement_id: str, ID: int = Cookie(None)):
    client = root.clients[ID]
    course = root.courses[course_id]
    
    try:
        announcement = root.announcements[announcement_id]
    except KeyError:
        return RedirectResponse(f"/classes/{course_id}/announcements", status_code=303)
    
    if course.removeAnnouncement(announcement):
        root.announcements.pop(announcement_id)
        root._p_changed = True
    
    return RedirectResponse(f"/classes/{course_id}/announcements", status_code=303)

# @app.post("/classes/{course_id}/editAnnouncement/{announcement_id}")
# async def save_edit_announcement(request: Request, course_id: int, announcement_id: str, name: str = Form(...), this_date: str = Form(...), description: str = Form(...), attachmentFiles: List[UploadFile] = File(None), ID: int = Cookie(None), client_type: str = Cookie(None)):
#     client = root.clients[ID]
#     announcement = root.announcements[announcement_id]
#     announcement.setName(name)
#     announcement.setDate(this_date)
#     announcement.setDescription(description)
    
#     UPLOAD_DIR = "Upload"
#     summitfiles = []
    
#     if attachmentFiles:
#         for file in attachmentFiles:
#             data = await file.read()
#             saveas = f"{UPLOAD_DIR}/{file.filename}"
#             with open(saveas, 'wb') as f:
#                 f.write(data)
#             summitfiles.append(saveas)
        
#         announcement.setAttachment(summitfiles)
    
#     return RedirectResponse(f"/classes/{course_id}/announcements", status_code=303)

@app.post("/classes/{course_id}/editAnnouncement/{announcement_id}")
async def save_edit_announcement(
    request: Request,
    course_id: int,
    announcement_id: str,
    name: str = Form(...),
    this_date: str = Form(...),
    description: str = Form(...),
    attachmentFiles: List[UploadFile] = File(None),
    ID: int = Cookie(None),
    client_type: str = Cookie(None),
):
    # Simulate getting client and announcement
    client = root.clients.get(ID)
    announcement = root.announcements.get(announcement_id)

    # Update announcement details
    announcement.setName(name)
    announcement.setDate(this_date)
    announcement.setDescription(description)

    # Directory for uploads
    UPLOAD_DIR = os.path.join("Upload")
    os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the directory exists

    summitfiles = []

    # Handle uploaded files if any
    if attachmentFiles:  # Skip if no files are uploaded
        for file in attachmentFiles:
            if file.filename:  # Ensure the file has a valid filename
                data = await file.read()
                saveas = os.path.join(UPLOAD_DIR, file.filename)
                with open(saveas, "wb") as f:
                    f.write(data)
                summitfiles.append(saveas)

        # Update attachments in the announcement
        announcement.setAttachment(summitfiles)

    # Redirect to the announcements page
    return RedirectResponse(f"/classes/{course_id}/announcements", status_code=303)

@app.get("/classes/{course_id}/editAnnouncement/{announcement_id}/removeAttachment")
async def remove_attachment(request: Request, course_id: int, announcement_id: str, ID: int = Cookie(None)):
    
    client = root.clients[ID]
    announcement = root.announcements[announcement_id]
    announcement.removeAttachment()

    return RedirectResponse(f"/classes/{course_id}/editAnnouncement/{announcement_id}", status_code=303)

# =================

@app.get("/classes/{course_id}/grade/{ass_id}")
async def gradeAssignment(request: Request, course_id: int, ass_id: str, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    
    client = root.clients[ID]
    course = root.courses[course_id]
    assignment = root.assignments[ass_id]
    submitted_work = assignment.submitted_work
    
    data = {
        "request": request,
        "client": client,
        "course": course,
        "client_type": client_type,
        "assignment": assignment,
        "submitted_work": submitted_work,
        "root": root,
        "first_course_id": first_course_id
    }
    
    print(submitted_work)
    
    return templates.TemplateResponse("gradeall.html", data)

@app.get("/delete/submission/{course_id}/{ass_id}/{student_id}")
async def removeSubmission(request: Request, course_id: int, student_id: int, ass_id: str, ID: int = Cookie(None), client_type: str = Cookie(None)):
    if client_type != "Lecturer":
        return {"Message": "NO PERMISSION"}
    assignment = root.assignments[ass_id]
    assignment.unSummitWork(student_id)
    return RedirectResponse(url = "/classes/{}/grade/{}".format(course_id, ass_id), status_code=303)

@app.get("/classes/{course_id}/grade/{ass_id}/{student_id}")
async def grade_Student(request: Request, course_id: int, ass_id: str, student_id: int, ID: int = Cookie(None), client_type: str = Cookie(None), first_course_id: int = Cookie(None)):
    client = root.clients[ID]
    course = root.courses[course_id]
    assignment = root.assignments[ass_id]
    submitted_work = assignment.submitted_work
    student = root.clients[student_id]

    data = {
        "request": request,
        "client": client,
        "course": course,
        "student": student,
        "client_type": client_type,
        "assignment": assignment,
        "submitted_work": submitted_work,
        "root": root,
        "first_course_id": first_course_id
    }

    return templates.TemplateResponse("gradeIndividual.html", data)

@app.post("/grading/{course_id}/{ass_id}/{student_id}")
async def grading_Student(request: Request, course_id: int, ass_id: str, student_id: int, score: int = Form(None) ,ID: int = Cookie(None), client_type: str = Cookie(None)):
    
    if score == None:
        pass
    else:
        assignment = root.assignments[ass_id]
        if score > assignment.max_score:
            score = assignment.max_score
        assignment.grading(student_id, score)

    return RedirectResponse("/classes/{}/grade/{}".format(course_id, ass_id), status_code=303)

# ================

# Dummy functions for client and first_course_id (Replace with actual logic)
def get_client():
    return {"avatar": "/images/user-avatar.png"}  # Example client data

def get_first_course_id():
    return 1 


@app.get("/event", response_class=HTMLResponse)
async def getEventCalendar(request: Request, client: dict = Depends(get_client), first_course_id: int = Depends(get_first_course_id)):
    # Data to be passed into the template
    data = {
        "client": client,
        "first_course_id": first_course_id
    }
    return templates.TemplateResponse("calender.html", {"request": request, **data})
# ================
@app.on_event("shutdown")
async def shutdown():
    transaction.commit()