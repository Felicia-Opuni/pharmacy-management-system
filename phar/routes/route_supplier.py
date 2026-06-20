from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt

supplier_bp = Blueprint('supplier', __name__)

#fetch all suppliers
@supplier_bp.route('/suppliers', methods=['GET'])
@jwt_required()
def get_all_suppliers():
    try:
        conn=get_db()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Supplier")
        suppliers=cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(suppliers)
    except Exception as e:  
        return jsonify({'error': str(e)}), 500
    

#add new supplier
@supplier_bp.route('/suppliers', methods=['POST'])
@jwt_required()
def add_supplier():
    try:
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()

        claims= get_jwt()
        if claims.get('StaffRole') not in ['CEO','Pharmacist']:
            return jsonify({'messages': 'Access denied'}), 403
        
        cursor.execute("""
            INSERT INTO Supplier (SupplierName, SupplierPhoneNumber, SupplierEmail, SupplierAddress)
            VALUES (%s, %s, %s, %s)
            """, (
            data['SupplierName'],
            data['SupplierPhoneNumber'],
            data['SupplierEmail'],
            data['SupplierAddress']
            ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Supplier added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#fetch supplier by id
@supplier_bp.route('/suppliers/<int:id>', methods=['GET'])
@jwt_required()
def get_supplier_by_id(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Supplier WHERE SupplierID = %s", (id,))
        supplier = cursor.fetchone()
        cursor.close()
        conn.close()

        if supplier:
            return jsonify(supplier)
        else:
            return jsonify({'message': 'Supplier not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#update supplier by id
@supplier_bp.route('/suppliers/<int:id>', methods=['PUT'])
@jwt_required()
def update_supplier(id):

    try:
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        claims = get_jwt()
        if claims.get('StaffRole') not in ['CEO','Pharmacist']:
            return jsonify({'message': 'Accessed denied'}), 403
        
        cursor.execute("SELECT * FROM Supplier WHERE SupplierID = %s", (id,))
        supplier = cursor.fetchone()
        if not supplier:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Supplier not found'}), 404

        cursor.execute("UPDATE Supplier SET SupplierName = %s, SupplierPhoneNumber = %s, SupplierEmail = %s, SupplierAddress = %s WHERE SupplierID = %s", (
            data.get('SupplierName', supplier["SupplierName"]),
            data.get('SupplierPhoneNumber', supplier["SupplierPhoneNumber"]),
            data.get('SupplierEmail', supplier["SupplierEmail"]),
            data.get('SupplierAddress', supplier["SupplierAddress"]),
            id
            ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Supplier updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#delete supplier by id
@supplier_bp.route('/suppliers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_supplier(id):
    try:
        conn = get_db()
        cursor = conn.cursor()

        claims = get_jwt()
        if claims.get('StaffRole') not in ['CEO','Pharmacist']:
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("SELECT * FROM Supplier WHERE SupplierID = %s", (id,))
        supplier = cursor.fetchone()
        if not supplier:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Supplier not found'}), 404

        cursor.execute("DELETE FROM Supplier WHERE SupplierID = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Supplier deleted successfully'})
    except Exception as e:
        #import traceback
        #traceback.print_exc()
        return jsonify({'error': str(e)}), 500
