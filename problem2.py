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

