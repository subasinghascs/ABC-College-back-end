from Database.db import db
from api.model.student_model import Student, Address

class StudentRepository:
    @staticmethod
    def create_student(student_dto, addresses):
        new_student = Student(name=student_dto.name, email=student_dto.email)
        for address_data in addresses:
            new_address = Address(street=address_data['street'], city=address_data['city'],
                                  state=address_data['state'], zipcode=address_data['zipcode'])
            new_student.addresses.append(new_address)
        db.session.add(new_student)
        db.session.commit()
        return new_student

    @staticmethod
    def get_student_by_id(student_id):
        return Student.query.get(student_id)

    @staticmethod
    def get_all_students():
        return Student.query.all()

    @staticmethod
    def update_student(student_id, student_dto):
        student = StudentRepository.get_student_by_id(student_id)
        if student:
            student.name = student_dto.name
            student.email = student_dto.email
            db.session.commit()
            return student
        return None

    @staticmethod
    def delete_student(student_id):
        student = StudentRepository.get_student_by_id(student_id)
        if student:
            # Delete associated addresses first
            for address in student.addresses:
                db.session.delete(address)
            db.session.delete(student)
            db.session.commit()
            return True
        return False
