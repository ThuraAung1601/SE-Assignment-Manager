import ZODB, ZODB.FileStorage, BTrees.OOBTree
import transaction
from class_module import *

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

gradeScheme = [
    {"Grade": "A", "min":80, "max":100},
    {"Grade": "B", "min":70, "max":79}, 
    {"Grade": "C", "min":60, "max":69}, 
    {"Grade": "D", "min":50, "max":59}, 
    {"Grade": "F", "min":0, "max":49}
]

root.courses = BTrees.OOBTree.BTree()
root.courses[101] = Course(101, "Computer Programming", 4)
root.courses[201] = Course(201, "Web Programming", 4)
root.courses[301] = Course(301, "Artificial Intelligence", 3, banner = "/images/default-banner.png")

root.courses[101].setGradeScheme(gradeScheme)
root.courses[201].setGradeScheme(gradeScheme)
root.courses[301].setGradeScheme(gradeScheme)

root.assignments = BTrees.OOBTree.BTree()
root.assignments["dff9328c-93ad-4b68-af6a-8934c809e5d0"] = Assignment("dff9328c-93ad-4b68-af6a-8934c809e5d0", "Programming Assignment 1", 10, "2025-02-01")
root.assignments["ed1c46f0-90d8-4ec9-907d-368b62446640"] = Assignment("ed1c46f0-90d8-4ec9-907d-368b62446640", "Programming Assignment 2", 10, "2025-02-01")
root.assignments["e184b3dd-0174-4bfa-b18b-786e9204d3c8"] = Assignment("e184b3dd-0174-4bfa-b18b-786e9204d3c8", "Programming Assignment 3", 10, "2025-02-01")
root.assignments["6f323d65-cbaf-4cee-b341-983a223d31f0"] = Assignment("6f323d65-cbaf-4cee-b341-983a223d31f0", "Web Assignment 1", 10, "2025-02-10")
root.assignments["d504ce3c-7ea2-4e3b-a2b8-fe33668746b7"] = Assignment("d504ce3c-7ea2-4e3b-a2b8-fe33668746b7", "Web Assignment 2", 10, "2025-02-10")
root.assignments["c2a7363c-2b0b-4cd9-8f66-effc04fc24df"] = Assignment("c2a7363c-2b0b-4cd9-8f66-effc04fc24df", "AI Assignment 1", 10, "2025-02-10")
root.assignments["cb3a49ab-4d2b-489b-9a92-2115744ec040"] = Assignment("cb3a49ab-4d2b-489b-9a92-2115744ec040", "AI Assignment 2", 10, "2025-02-10")

root.courses[101].assignments = [root.assignments["dff9328c-93ad-4b68-af6a-8934c809e5d0"], root.assignments["ed1c46f0-90d8-4ec9-907d-368b62446640"], root.assignments["e184b3dd-0174-4bfa-b18b-786e9204d3c8"]]
root.courses[201].assignments = [root.assignments["6f323d65-cbaf-4cee-b341-983a223d31f0"], root.assignments["d504ce3c-7ea2-4e3b-a2b8-fe33668746b7"]]
root.courses[301].assignments = [root.assignments["c2a7363c-2b0b-4cd9-8f66-effc04fc24df"], root.assignments["cb3a49ab-4d2b-489b-9a92-2115744ec040"]]

root.announcements = BTrees.OOBTree.BTree()
root.courses[101].announcements = []
root.courses[201].announcements = []
root.courses[301].announcements = []

root.clients = BTrees.OOBTree.BTree()

#Lecturers
root.clients[1001] = Lecturer(1001, [], "Dr. Louis", "1001", "1234")
root.clients[1001].setCourses([root.courses[101], root.courses[201], root.courses[301]])

#Students
root.clients[606] = Student(606, [], "Thura Aung", "606", "1234")
root.clients[606].enrolls = [Enrollment(root.courses[101], 80, root.clients[606]), Enrollment(root.courses[201], 87, root.clients[606]), Enrollment(root.courses[301], 80, root.clients[606])]
root.clients[634] = Student(634, [], "Ei Myat Nwe", "634", "1234")
root.clients[634].enrolls = [Enrollment(root.courses[101], 80, root.clients[634]), Enrollment(root.courses[201], 87, root.clients[634]), Enrollment(root.courses[301], 80, root.clients[634])]
root.clients[622] = Student(622, [], "Nay Chi Shunn Lei","622", "1234")
root.clients[622].enrolls = [Enrollment(root.courses[101], 80, root.clients[622]), Enrollment(root.courses[201], 87, root.clients[622]), Enrollment(root.courses[301], 80, root.clients[622])]

transaction.commit()
db.close()
