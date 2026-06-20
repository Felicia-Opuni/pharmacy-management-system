from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended  import jwt_required, get_jwt

sale_bp = Blueprint('sale',__name__)

#get all sales
@sale_bp.route('/sale', methods = ['GET'])
@jwt_required()
def get_all_sale():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Sale")
        sale= cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(sale)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


#add a new sale
@sale_bp.route('/sale', methods= ['POST'])
@jwt_required()
def add_new_sale():
    try:
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()

        claims = get_jwt()
        if claims.get('StaffRole') not in ['Cashier','Medical Counter Assistant']:
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("""
                      INSERT INTO Sale (CustomerID,StaffID,SaleDate,TotalAmount, PaymentMethod)
                      VALUES (%s,%s,%s,%s,%s)"""
                      ,(
                          data['CustomerID'],
                          data['StaffID'],
                          data['SaleDate'],
                          data['TotalAmount'],
                          data['PaymentMethod']
                      ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'New Sale added'})
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    

#get receipt from sale
@sale_bp.route('/sale/receipt/<int:id>', methods = ['GET'])
@jwt_required()
def get_sale_receipt_by_id(id):
    try:
        conn= get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_Receipt WHERE SaleID = %s", (id))
        sale=cursor.fetchone()
        cursor.close()
        conn.close()

        if sale is None:
            return jsonify({'message': 'Sale not found'}),404
        return jsonify(sale)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500