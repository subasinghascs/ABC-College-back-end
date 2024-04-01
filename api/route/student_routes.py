from flask import Blueprint, request, jsonify
from api.DTO.student_dto import StudentDTO
from api.service.student_service import StudentService

student_bp = Blueprint('student', __name__)

@student_bp.route('/student', defaults={'student_id': None}, methods=['GET'])
@student_bp.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    if student_id is not None:
        student = StudentService.get_student_by_id(student_id)
        if student:
            return jsonify({"id": student.id, "name": student.name, "email": student.email}), 200
        return jsonify({"message": "Student not found"}), 404
    else:
        all_students = StudentService.get_all_students()
        student_list = [{"id": student.id, "name": student.name, "email": student.email} for student in all_students]
        return jsonify(student_list), 200

@student_bp.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    addresses_data = data.get('addresses')

    if not name or not email or not addresses_data:
        return jsonify({"message": "Name, email, and addresses are required fields"}), 400

    # Create a student DTO object
    student_dto = StudentDTO(name, email)

    # Extract address data from the request and create address objects
    addresses = []
    for address_data in addresses_data:
        street = address_data.get('street')
        city = address_data.get('city')
        state = address_data.get('state')
        zipcode = address_data.get('zipcode')
        if not street or not city or not state or not zipcode:
            return jsonify({"message": "All fields (street, city, state, zipcode) are required for each address"}), 400
        addresses.append({"street": street, "city": city, "state": state, "zipcode": zipcode})

    # Create the student with associated addresses
    new_student = StudentService.create_student(student_dto, addresses)
    return jsonify({"message": "Student created successfully", "student_id": new_student.id}), 201


@student_bp.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student_dto = StudentDTO(data['name'], data['email'])
    updated_student = StudentService.update_student(student_id, student_dto)
    if updated_student:
        return jsonify({"message": "Student updated successfully"}), 200
    return jsonify({"message": "Student not found"}), 404

@student_bp.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    deleted = StudentService.delete_student(student_id)
    if deleted:
        return jsonify({"message": "Student deleted successfully"}), 200
    return jsonify({"message": "Student not found"}), 404

@student_bp.route('/student/<int:student_id>/address', methods=['GET'])
def get_student_with_address(student_id):
    student, addresses = StudentService.get_student_with_address(student_id)
    if student:
        student_data = {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "addresses": [
                {
                    "street": address.street,
                    "city": address.city,
                    "state": address.state,
                    "zipcode": address.zipcode
                } for address in addresses
            ]
        }
        return jsonify(student_data), 200
    return jsonify({"message": "Student not found"}), 404
