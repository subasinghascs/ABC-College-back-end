from api.repo.student_repo import StudentRepository

class StudentService:
    @staticmethod
    def create_student(student_dto, addresses):
        return StudentRepository.create_student(student_dto, addresses)

    @staticmethod
    def get_student_by_id(student_id):
        return StudentRepository.get_student_by_id(student_id)

    @staticmethod
    def get_all_students():
        return StudentRepository.get_all_students()

    @staticmethod
    def update_student(student_id, student_dto):
        return StudentRepository.update_student(student_id, student_dto)

    @staticmethod
    def delete_student(student_id):
        return StudentRepository.delete_student(student_id)
