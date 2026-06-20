from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt

purchase_bp = Blueprint('purchase',__name__)

#get all purchase
@purchase_bp.route('/purchase', methods=['GET'])
@jwt_required()
def get_all_purchase():
    try:
        conn=get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Purchase")
        purchase=cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(purchase)
    except Exception as e:
        return jsonify({'Error': str(e)})
    

#get purchase by id
@purchase_bp.route('/purchase/<int:id>', methods = ['GET'])
@jwt_required()
def get_purchase_by_id(id):
    try:
        conn=get_db()
        cursor= conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Purchase WHERE PurchaseID = %s", (id,))
        purchase=cursor.fetchone()
        cursor.close()
        conn.close()

        if purchase is None:
            return jsonify({'message': 'Purchase not found'})
        return jsonify(purchase)
    except Exception as e:
        return jsonify({'Error': str(e)})
    

#add new purchase
@purchase_bp.route('/purchase', methods =['POST'])
@jwt_required()
def add_purchase():
    try:
        data= request.get_json()
        conn=get_db()
        cursor = conn.cursor()

        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403
    
        cursor.execute("""
                INSERT INTO Purchase (SupplierID, PurchaseDate, InvoiceNumber)
                VALUES (%s, %s, %s)
                    """, (
                        data['SupplierID'],
                        data['PurchaseDate'],
                        data['InvoiceNumber']
                    ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Purchase added successfully'})
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
