from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity

staff_bp = Blueprint('staff', __name__)

#Staff login
@staff_bp.route('/staff/login', methods=['POST'])
def staff_login():
    try:
        data = request.get_json()
        email = data.get('StaffEmail')
        password = data.get('password')

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Staff WHERE StaffEmail = %s", (email,))
        staff = cursor.fetchone()
        cursor.close()
        conn.close()

        if not staff:
            return jsonify({'message': 'Staff not found'}), 404

        if check_password_hash(staff['PasswordHash'], password):
            access_token = create_access_token(
                identity=str(staff['StaffID']),
                additional_claims={'StaffRole': staff['StaffRole']}
            )
            return jsonify({'access_token': access_token,
                            'staff_id': staff['StaffID'],
                            'staff_name': staff['StaffFName'] + ' ' + staff['StaffSName'],
                            'staff_role': staff['StaffRole']
                            
                            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#staff member updating their password
@staff_bp.route('/staff/<int:id>/update_password', methods=['POST'])
@jwt_required()
def update_password(id):
    try:
        data = request.get_json()
        new_password = data.get('password')
        current_user_id = get_jwt_identity()
       
        if current_user_id != str(id):
            return jsonify({'message': 'You can only change your own password'}), 403
        
        hashed_password = generate_password_hash(new_password)  
        
        conn = get_db()
        cursor = conn.cursor()  
        cursor.execute("UPDATE Staff SET PasswordHash = %s WHERE StaffID = %s", (hashed_password, id))
        conn.commit()
        cursor.close()  
        conn.close()
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Fetch all staff members
@staff_bp.route('/staff', methods=['GET']) 
@jwt_required()
def get_all_staff():
    try:
        conn = get_db()
        cursor=conn.cursor(dictionary=True)

        
        cursor.execute("SELECT * FROM Staff")
        staff=cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(staff)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#add new staff member
@staff_bp.route('/staff' , methods=['POST'])
@jwt_required()
def add_staff():
    try:
        data = request.get_json()
        password = data.get('password')
        
        conn = get_db()
        cursor = conn.cursor()

        claims = get_jwt()
        if claims.get('StaffRole') != 'CEO':
            return jsonify({'message': 'Access denied'}), 403
        
        hashed_password = generate_password_hash(data['password'])
        

        cursor.execute("""INSERT INTO Staff (StaffFName, StaffSName, StaffPhoneNumber, StaffEmail, StaffAddress, StaffRole, PasswordHash)
             VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
            data['StaffFName'],
            data['StaffSName'],
            data['StaffPhoneNumber'],
            data['StaffEmail'],
            data['StaffAddress'],
            data['StaffRole'],
            hashed_password
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Staff member added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#fetch staff member by id
@staff_bp.route('/staff/<int:id>', methods=['GET'])
@jwt_required()
def get_staff_by_id(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Staff WHERE StaffID = %s", (id,))
        staff = cursor.fetchone()
        cursor.close()
        conn.close()

        if staff:
            return jsonify(staff)
        else:
            return jsonify({'message': 'Staff member not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  


#delete staff member by id
@staff_bp.route('/staff/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_staff(id):
    try:
        conn = get_db()
        cursor = conn.cursor()

        claims = get_jwt()
        if claims.get('StaffRole') != 'CEO':
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("SELECT * FROM Staff WHERE StaffID = %s", (id,))
        staff = cursor.fetchone()
        if not staff:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Staff member not found'}), 404
        
        cursor.execute("DELETE FROM Staff WHERE StaffID = %s", (id))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Staff member deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#update staff member by id
@staff_bp.route('/staff/<int:id>', methods=['PUT'])
@jwt_required()
def update_staff(id):
    try:
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        claims = get_jwt()
        if claims.get('StaffRole') != 'CEO':
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("SELECT * FROM Staff WHERE StaffID = %s", (id,))
        staff = cursor.fetchone()
        if not staff:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Staff member not found'}), 404

        sql="""UPDATE Staff SET StaffFName = %s, StaffSName = %s, StaffPhoneNumber = %s, StaffEmail = %s, StaffAddress = %s, StaffRole = %s WHERE StaffID = %s"""
        
        values = (
            data.get('StaffFName', staff["StaffFName"]),
            data.get('StaffSName', staff["StaffSName"]),
            data.get('StaffPhoneNumber', staff["StaffPhoneNumber"]),
            data.get('StaffEmail', staff["StaffEmail"]),
            data.get('StaffAddress', staff["StaffAddress"]),
            data.get('StaffRole', staff["StaffRole"]),
            id
            )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Staff member updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500