class Student:
    def __init__(self, name: str, major: str, student_id: str):
        self.name = name
        self.major = major
        self.student_id = student_id

class PartTimeStudent(Student):
    count = 0  

    def __init__(self, name: str, major: str, student_id: str, min_hour: int, max_hour: int):
        super().__init__(name, major, student_id)
        self.min_hour = min_hour
        self.max_hour = max_hour
        PartTimeStudent.count += 1  

    @staticmethod
    def get_count():
        return PartTimeStudent.count

class Lecturer:
    def __init__(self, name: str, rank: str, lecturer_id: str):
        self.name = name
        self.rank = rank
        self.lecturer_id = lecturer_id

class Project:
    def __init__(self, name: str, budget: float):
        self.name = name
        self.budget = budget

class SchoolSystem:
    def __init__(self):
        self.students = []
        self.lecturers = []
        self.projects = []

    def add_student(self, student: Student):
        if len(self.students) < 10:
            self.students.append(student)
        else:
            print("Cannot add more students. Maximum limit reached.")

    def add_lecturer(self, lecturer: Lecturer):
        if len(self.lecturers) < 10:
            self.lecturers.append(lecturer)
        else:
            print("Cannot add more lecturers. Maximum limit reached.")

    def add_project(self, project: Project):
        if len(self.projects) < 10:
            self.projects.append(project)
        else:
            print("Cannot add more projects. Maximum limit reached.")

    def display_all(self):
        print("\nStudents:")
        for student in self.students:
            print(vars(student))

        print("\nLecturers:")
        for lecturer in self.lecturers:
            print(vars(lecturer))

        print("\nProjects:")
        for project in self.projects:
            print(vars(project))

