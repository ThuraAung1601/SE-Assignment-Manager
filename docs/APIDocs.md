# FastAPI Project Documentation

This document provides an overview of the endpoints for the FastAPI application, which manages a learning management system (LMS) for students and lecturers.

## Endpoints

### GET / (Home Page)
- **Description**: This endpoint returns the homepage of the application.
- **Parameters**:
  - `ID` (Cookie, Optional): The unique client ID.
  - `client_type` (Cookie, Optional): Type of client (`Lecturer` or `Student`).
- **Response**:
  - Renders the `index.html` template with the client data if valid, otherwise shows the default homepage.

### POST /login
- **Description**: Logs a client (Lecturer or Student) into the system by verifying their credentials.
- **Parameters**:
  - `ID` (Form): The client ID.
  - `password` (Form): The password for authentication.
- **Response**:
  - Redirects to the appropriate course assignments page if login is successful, otherwise redirects back to the login page with an error.

### GET /login
- **Description**: Returns the login form page.
- **Parameters**:
  - `error` (Query, Optional): Error code for failed login.
- **Response**: Renders the login page template.

### GET /classes/{course_id}/assignments
- **Description**: Displays the list of assignments for a specific course.
- **Parameters**:
  - `course_id` (Path): The ID of the course.
  - `ID` (Cookie): The client ID.
  - `client_type` (Cookie): Type of client (`Lecturer` or `Student`).
  - `first_course_id` (Cookie): The ID of the first course.
- **Response**:
  - Renders the `classes.html` template with the assignments of the course.

### GET /classes/{course_id}/assignments/{assignment_id}
- **Description**: Displays the details of a specific assignment.
- **Parameters**:
  - `course_id` (Path): The ID of the course.
  - `assignment_id` (Path): The ID of the assignment.
  - `ID` (Cookie): The client ID.
  - `client_type` (Cookie): Type of client (`Lecturer` or `Student`).
  - `first_course_id` (Cookie): The ID of the first course.
- **Response**:
  - Renders the `assignment.html` template with assignment details.

### POST /uploadFile/{course_id}/{ASS_ID}
- **Description**: Allows a student to upload assignment files for a specific course and assignment.
- **Parameters**:
  - `course_id` (Path): The ID of the course.
  - `ASS_ID` (Path): The ID of the assignment.
  - `assignmentFiles` (Form): The files to be uploaded.
  - `ID` (Cookie): The client ID.
- **Response**:
  - Redirects to the assignment details page after successful file upload.

### GET /logout
- **Description**: Logs the client out and deletes the session cookies.
- **Response**: Redirects to the home page.

### GET /profile
- **Description**: Displays the profile of the logged-in client.
- **Parameters**:
  - `ID` (Cookie): The client ID.
  - `client_type` (Cookie): Type of client (`Lecturer` or `Student`).
  - `first_course_id` (Cookie): The ID of the first course.
- **Response**:
  - Renders the `profile.html` template with the client’s profile data.

### POST /profile
- **Description**: Updates the profile information (name, username, avatar) of the logged-in client.
- **Parameters**:
  - `name` (Form): The updated name.
  - `user_name` (Form): The updated username.
  - `avatar` (File): The avatar file.
- **Response**:
  - Redirects to the profile page after updating the information.

### GET /classes/{course_id}/addAssignment
- **Description**: Displays the form to add a new assignment to a course.
- **Parameters**:
  - `course_id` (Path): The ID of the course.
  - `ID` (Cookie): The client ID.
  - `client_type` (Cookie): Type of client (`Lecturer` or `Student`).
  - `first_course_id` (Cookie): The ID of the first course.
- **Response**:
  - Renders the `edit_assignment.html` template with a new assignment form.

### POST /classes/{course_id}/editAssignment/{assignment_id}
- **Description**: Saves the edited assignment details.
- **Parameters**:
  - `name` (Form): The updated assignment name.
  - `due_date` (Form): The updated due date.
  - `description` (Form): The updated description.
  - `attachmentFiles` (File): The updated attachment files.
  - `ID` (Cookie): The client ID.
- **Response**:
  - Redirects to the assignment details page after saving the changes.

### GET /classes/{course_id}/removeAssignment/{assignment_id}
- **Description**: Removes an assignment from a course.
- **Parameters**:
  - `course_id` (Path): The ID of the course.
  - `assignment_id` (Path): The ID of the assignment.
  - `ID` (Cookie): The client ID.
- **Response**:
  - Redirects to the course assignments page after removing the assignment.

### GET /classes/{course_id}/unsubmit/{ASS_ID}
- **Description**: Allows a student to unsubmit their assignment submission.
- **Parameters**:
  - `course_id` (Path): The ID of the course.
  - `ASS_ID` (Path): The ID of the assignment.
  - `ID` (Cookie): The client ID.
- **Response**:
  - Redirects to the assignment page after unsubmission.
 
---

### GET /classes/{course_id}/announcements/{announcement_id}
- **Description**: This endpoint displays the details of a specific announcement for a given course.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `announcement_id` (Path): The unique ID of the announcement.
  - `ID` (Cookie, Optional): The unique client ID.
  - `client_type` (Cookie, Optional): Type of client (`Lecturer` or `Student`).
  - `first_course_id` (Cookie, Optional): The ID of the first course the client is enrolled in.
- **Response**:
  - Renders the `announcements.html` template with the course and announcement data if valid, otherwise redirects to the homepage.

---

### POST /uploadFile/{course_id}/{ANN_ID}
- **Description**: This endpoint allows a student to upload files for an assignment.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `ANN_ID` (Path): The unique ID of the announcement (assignment).
  - `assignmentFiles` (Form Data, Optional): A list of files to upload for the assignment.
  - `ID` (Cookie): The unique client ID.
- **Response**:
  - Redirects to the announcement page after successfully uploading the files for the assignment.

---

### GET /unsubmit/{course_id}/{ANN_ID}
- **Description**: This endpoint allows a student to unsubmit a previously submitted assignment.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `ANN_ID` (Path): The unique ID of the announcement (assignment).
  - `ID` (Cookie): The unique client ID.
- **Response**:
  - Redirects to the assignment page after successfully unsubmiting the assignment.

---

### GET /classes/{course_id}/addAnnouncement
- **Description**: This endpoint allows a lecturer to add a new announcement to the course.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `ID` (Cookie): The unique client ID.
  - `client_type` (Cookie): Type of client (`Lecturer` or `Student`).
  - `first_course_id` (Cookie, Optional): The ID of the first course the client is enrolled in.
- **Response**:
  - Renders the `edit_announcement.html` template with the data for the newly added announcement.

---

### GET /classes/{course_id}/editAnnouncement/{announcement_id}
- **Description**: This endpoint allows a lecturer to edit an existing announcement.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `announcement_id` (Path): The unique ID of the announcement to be edited.
  - `ID` (Cookie): The unique client ID.
  - `client_type` (Cookie): Type of client (`Lecturer` or `Student`).
  - `first_course_id` (Cookie, Optional): The ID of the first course the client is enrolled in.
- **Response**:
  - Renders the `edit_announcement.html` template with the data for the announcement to be edited.

---

### GET /classes/{course_id}/removeAnnouncement/{announcement_id}
- **Description**: This endpoint allows a lecturer to remove an existing announcement from the course.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `announcement_id` (Path): The unique ID of the announcement to be removed.
  - `ID` (Cookie): The unique client ID.
- **Response**:
  - Redirects to the announcements page after successfully removing the announcement from the course.

---

### POST /classes/{course_id}/editAnnouncement/{announcement_id}
- **Description**: This endpoint allows a lecturer to save edited details for an announcement, including its name, date, description, and attachments.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `announcement_id` (Path): The unique ID of the announcement to edit.
  - `name` (Form): The updated name of the announcement.
  - `this_date` (Form): The updated date of the announcement.
  - `description` (Form): The updated description of the announcement.
  - `attachmentFiles` (Form Data, Optional): A list of files to upload as attachments to the announcement.
  - `ID` (Cookie): The unique client ID.
  - `client_type` (Cookie): Type of client (`Lecturer` or `Student`).
- **Response**:
  - Redirects to the announcements page after successfully saving the edited announcement.

---

### GET /classes/{course_id}/editAnnouncement/{announcement_id}/removeAttachment
- **Description**: This endpoint allows a lecturer to remove the attachments from an announcement.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `announcement_id` (Path): The unique ID of the announcement.
  - `ID` (Cookie): The unique client ID.
- **Response**:
  - Redirects to the edit announcement page after removing the attachment.

---

### GET /classes/{course_id}/grade/{ass_id}
- **Description**: This endpoint displays the grade page for a specific assignment, showing submitted works from students.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `ass_id` (Path): The unique ID of the assignment.
  - `ID` (Cookie): The unique client ID.
  - `client_type` (Cookie): Type of client (`Lecturer` or `Student`).
  - `first_course_id` (Cookie, Optional): The ID of the first course the client is enrolled in.
- **Response**:
  - Renders the `gradeall.html` template with the assignment and student work data.

---

### GET /delete/submission/{course_id}/{ass_id}/{student_id}
- **Description**: This endpoint allows a lecturer to remove a student's submission for a specific assignment.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `ass_id` (Path): The unique ID of the assignment.
  - `student_id` (Path): The unique ID of the student.
  - `ID` (Cookie): The unique client ID.
  - `client_type` (Cookie): Type of client (`Lecturer`).
- **Response**:
  - Redirects to the grade page after successfully removing the student's submission.

---

### GET /classes/{course_id}/grade/{ass_id}/{student_id}
- **Description**: This endpoint displays the grade page for a specific student's submission of an assignment.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `ass_id` (Path): The unique ID of the assignment.
  - `student_id` (Path): The unique ID of the student.
  - `ID` (Cookie): The unique client ID.
  - `client_type` (Cookie): Type of client (`Lecturer` or `Student`).
  - `first_course_id` (Cookie, Optional): The ID of the first course the client is enrolled in.
- **Response**:
  - Renders the `gradeIndividual.html` template with the assignment and student's submission data.

---

### POST /grading/{course_id}/{ass_id}/{student_id}
- **Description**: This endpoint allows a lecturer to grade a student's submission for an assignment.
- **Parameters**:
  - `course_id` (Path): The unique ID of the course.
  - `ass_id` (Path): The unique ID of the assignment.
  - `student_id` (Path): The unique ID of the student.
  - `score` (Form): The grade to assign to the student.
  - `ID` (Cookie): The unique client ID.
  - `client_type` (Cookie): Type of client (`Lecturer`).
- **Response**:
  - Redirects to the grade page after successfully grading the student's submission.

---

### GET /event
- **Description**: This endpoint displays the event calendar for the user.
- **Parameters**:
  - `client` (Depends): The client data (retrieved via a dummy function).
  - `first_course_id` (Depends): The ID of the first course the client is enrolled in (retrieved via a dummy function).
- **Response**:
  - Renders the `calender.html` template with event data for the client.

---

### On Shutdown Event
- **Description**: This event handler commits any pending changes to the database when the application shuts down.
- **Response**:
  - Commits the transaction to the database.
