from flask import Blueprint ,jsonify, request
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt

delivery_bp=Blueprint('delivery'/__name__)

roles=['Medical Counter Assistant','Pharmacist']

#get all delivery
@delivery_bp.route('/delivery', methods=['GET'])
@jwt_required()
def get_all_delivery():
    """
    Returns all deliveries.
    Uses the vw_DeliveryReport view from the database.
    Accessible by all roles.
    """
    try:
        conn = get_db()
        cursor= conn.cursor(dictionary=True)
        cursor.execute("""SELECT * FROM vw_DeliveryReport""")
        delivery=cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(delivery), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    

#get delivery by id
@delivery_bp.route('/delivery/<int:id>', methods=['GET'])
@jwt_required()
def get_all_delivery_id(id):
    """
    Returns one delivery record by DeliveryID.
    Uses the vw_DeliveryReport view.
    """
    try:
        conn = get_db()
        cursor= conn.cursor(dictionary=True)
        cursor.execute("""SELECT * FROM vw_DeliveryReport WHERE DeliveryID =%s""")
        delivery=cursor.fetchone()
        cursor.close()
        conn.close()
        if delivery:
            return jsonify(delivery), 200
        else:
            return jsonify({'message': 'Delivery not found'}), 404
           
        
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    

#add delivery
@delivery_bp.route('/delivery', methods=['PUT'])
@jwt_required()
def add_delivery():
    """
        Creates a new delivery record for a sale.
    Only Pharmacists and Medical Counter Assistants can create deliveries.

    Expected JSON body:
    {
        "SaleID": 1,
        "StaffID": 3,
        "DeliveryDate": "2026-05-20",
        "DeliveryStatus": "Pending",
        "DeliveryAddress": "123 Main Street, Accra"
    }
    """
    try:
        data= request.get_json()
        conn = get_db()
        cursor=conn.cursor()

        claims=get_jwt()
        if claims.get('StaffRole') not in roles:
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("SELECT * FROM Sale WHERE SaleID = %s", (data['SaleID'],))
        sale = cursor.fetchone()
        if not sale:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Sale not found. Cannot create delivery'}), 404

        cursor.execute("""
                    INSERT INTO Delivery (SaleID,StaffID, DeliveryDate, DeliveryStatus, DeliveryAddress)
                    VALUES (%s,%s,%s,%s,%s,%s)
                       """, (
                           data['SaleID'],
                           data['SatffID'],
                           data['DeliveryDate'],
                           data['DeliveryStatus'],
                           data['DeliveryAddress']
                       ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'new delivery added'}), 201
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    

#update delivery by id
@delivery_bp.route('/delivery/<int:id>', methods=['POST'])
@jwt_required()
def update_delivery_by_id(id):
    """
         Updates the status of a delivery.
    - Riders can only update the DeliveryStatus field.
    - Pharmacists and Medical Counter Assistants can update all fields.

    Expected JSON body (Rider):
    {
        "DeliveryStatus": "Delivered"
    }

    Expected JSON body (Pharmacist / Medical Counter Assistant):
    {
        "DeliveryDate": "2026-05-21",
        "DeliveryStatus": "Delivered",
        "DeliveryAddress": "456 New Road, Kumasi",
        "StaffID": 3
    }
    """
    try:
        data=request.get_json()
        conn=get_db()
        cursor= conn.cursor(dictionary=True)

        claims= get_jwt() 

        cursor.execute("SELECT * FROM Delivery WHERE DeliveryID = %s",(id,))
        delivery=cursor.fetchone()
        if not delivery:
            conn.close()
            cursor.close()
            return jsonify({'message': 'Delivery not found'}), 404
        
        
        

        if claims.get('StaffRole') == ['Rider','Medical Counter Assistant']:
            cursor.execute("UPDATE Delivery SET DeliveryStatus = %s WHERE DeliveryID = %s", 
                           (data.get('DeliveryStatus', delivery["DeliveryStatus"]), id))
            return jsonify({'message': 'Delivery Status updated'}), 201
        
        if claims.get('StaffRole') == roles:
            cursor.execute("UPDATE Delivery SET SaleID = %s, StaffID = %s, DeliveryDate = %s, DeliveryAddress",(
                data.get('SaleID', delivery["SaleID"]),
                data.get('StaffID', delivery["StaffID"]),
                data.get('DeliveryDate', delivery["DeliveryDate"]),
                data.get('DeliveryAddress', delivery["DeliveryAddress"]),
                id
            ))

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Accessed denied'}), 403
        return jsonify({'message': 'Delivery updated successfully'}), 201
        
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
                        
                       

@delivery_bp.route('/delivery/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_delivery(id):
    """
    Deletes a delivery record.
    Only Pharmacists can delete a delivery.
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403
 
        conn = get_db()
        cursor = conn.cursor()
 
        cursor.execute("SELECT * FROM Delivery WHERE DeliveryID = %s", (id,))
        delivery = cursor.fetchone()
 
        if not delivery:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Delivery not found'}), 404
 
        cursor.execute("DELETE FROM Delivery WHERE DeliveryID = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
 
        return jsonify({'message': 'Delivery deleted successfully'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500