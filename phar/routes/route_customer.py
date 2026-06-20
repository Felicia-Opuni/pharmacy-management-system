from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt


customer_bp = Blueprint('customer',__name__)

#fetch all customers
@customer_bp.route('/customer', methods = ['GET'])
@jwt_required()
def get_all_customers():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary= True)
        cursor.execute("SELECT * FROM Customer")
        customers=cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(customers)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

#fetch one customer by id
@customer_bp.route('/customer/<int:id>', methods = ['GET'])
@jwt_required()
def get_customer_by_id(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Customer WHERE CustomerID = %s", (id,))
        customers=cursor.fetchone()
        cursor.close()
        conn.close()
        
        if customers is None:
            return jsonify({'message': 'Customer not found'}), 404
        
        for key,value in customers.items():
            if hasattr(value, 'isoformat'):
                customers[key] = value.isoformat()
                
        return jsonify(customers)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

#add new customer
@customer_bp.route('/customer', methods=['POST'])
@jwt_required()
def add_customer():
    try:
        data=request.get_json()
        conn = get_db()
        cursor= conn.cursor()

        claims = get_jwt()
        if claims.get('StaffRole') not in ['Medical Counter Assistant','Pharmacist']:
            return jsonify({'message': 'Access denied'}), 403
        cursor.execute("""
            INSERT INTO Customer (CustomerFName, CustomerSName, CustomerGender, DateOfBirth, CustomerPhoneNumber, CustomerEmail, CustomerAddress, CustomerHealthStatus)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s) 
                """, (
                data['CustomerFName'],
                data['CustomerSName'],
                data['CustomerGender'],
                data['DateOfBirth'],
                data['CustomerPhoneNumber'],
                data['CustomerEmail'],
                data['CustomerAddress'],
                data['CustomerHealthStatus']
            ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'New Customer added'})
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    

#update customer by id
@customer_bp.route('/customer/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    try:
        conn=get_db()
        cursor=conn.cursor(dictionary=True)
        data = request.get_json()
        
        claims = get_jwt()
        if claims.get('StaffRole') not in ['Medical Counter Assistant','Pharmacist']:
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("SELECT * FROM Customer WHERE CustomerID = %s", (id,))
        customers = cursor.fetchone()

        if not customers:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Customer not found'}), 404
        
        sql="""
            UPDATE Customer
            SET CustomerFName = %s, CustomerSName = %s, CustomerGender = %s, DateOfBirth = %s, CustomerPhoneNumber = %s, CustomerEmail = %s, CustomerAddress = %s, CustomerHealthStatus = %s
            WHERE CustomerID = %s
            """
        values = (
            data.get('CustomerFName', customers['CustomerFName']),
            data.get('CustomerSName', customers['CustomerSName']),
            data.get('CustomerGender', customers['CustomerGender']),
            data.get('DateOfBirth', customers['DateOfBirth']),
            data.get('CustomerPhoneNumber', customers['CustomerPhoneNumber']),
            data.get('CustomerEmail', customers['CustomerEmail']),
            data.get('CustomerAddress', customers['CustomerAddress']),
            data.get('CustomerHealthStatus', customers['CustomerHealthStatus']),
            id
        )
        cursor.execute(sql,values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Customer updated successfully'}), 201
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    

#delete a customer
@customer_bp.route('/customer/<int:id>',methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    try:
        conn=get_db()
        cursor = conn.cursor(dictionary=True)

        claims = get_jwt()
        if claims.get('StaffRole') not in ['Medical Counter Assistant','Pharmacist'] :
            return jsonify({'message': 'Accessed denied'}), 403
    
        cursor.execute("SELECT * FROM Customer WHERE CustomerID = %s", (id,))
        customers = cursor.fetchone()

        if not customers:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Customer not found'})
        
        cursor.execute("DELETE FROM Customer WHERE CustomerID = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Customer successfully deleted'}), 201
    except Exception as e:
        return jsonify({'Error': str(e)}), 500