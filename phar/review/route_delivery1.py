from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt

delivery_bp = Blueprint('delivery', __name__)


# ── Get All Deliveries ────────────────────────────────────────────────────────

@delivery_bp.route('/delivery', methods=['GET'])
@jwt_required()
def get_all_deliveries():
    """
    Returns all deliveries.
    Uses the vw_DeliveryReport view from the database.
    Accessible by all roles.
    """
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_DeliveryReport")
        deliveries = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(deliveries), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Get Delivery by ID ────────────────────────────────────────────────────────

@delivery_bp.route('/delivery/<int:id>', methods=['GET'])
@jwt_required()
def get_delivery_by_id(id):
    """
    Returns one delivery record by DeliveryID.
    Uses the vw_DeliveryReport view.
    """
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM vw_DeliveryReport WHERE DeliveryID = %s",
            (id,)
        )
        delivery = cursor.fetchone()
        cursor.close()
        conn.close()

        if delivery is None:
            return jsonify({'message': 'Delivery not found'}), 404

        return jsonify(delivery), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Add New Delivery ──────────────────────────────────────────────────────────

@delivery_bp.route('/delivery', methods=['POST'])
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
        claims = get_jwt()
        if claims.get('StaffRole') not in ['Pharmacist', 'Medical Counter Assistant']:
            return jsonify({'message': 'Access denied'}), 403

        data = request.get_json()

        conn = get_db()
        cursor = conn.cursor()

        # Check that the Sale exists before creating a delivery for it
        cursor.execute("SELECT * FROM Sale WHERE SaleID = %s", (data['SaleID'],))
        sale = cursor.fetchone()
        if not sale:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Sale not found. Cannot create delivery.'}), 404

        cursor.execute("""
            INSERT INTO Delivery (SaleID, StaffID, DeliveryDate, DeliveryStatus, DeliveryAddress)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['SaleID'],
            data['StaffID'],
            data['DeliveryDate'],
            data['DeliveryStatus'],
            data['DeliveryAddress']
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Delivery created successfully'}), 201
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Update Delivery Status ────────────────────────────────────────────────────

@delivery_bp.route('/delivery/<int:id>', methods=['PUT'])
@jwt_required()
def update_delivery_status(id):
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
        claims = get_jwt()
        role = claims.get('StaffRole')

        # Only these roles can update a delivery
        allowed_roles = ['Pharmacist', 'Medical Counter Assistant', 'Rider']
        if role not in allowed_roles:
            return jsonify({'message': 'Access denied'}), 403

        data = request.get_json()

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Check the delivery exists
        cursor.execute("SELECT * FROM Delivery WHERE DeliveryID = %s", (id,))
        delivery = cursor.fetchone()

        if not delivery:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Delivery not found'}), 404

        if role == 'Rider':
            # Riders can only change the status
            new_status = data.get('DeliveryStatus', delivery['DeliveryStatus'])
            cursor.execute(
                "UPDATE Delivery SET DeliveryStatus = %s WHERE DeliveryID = %s",
                (new_status, id)
            )
        else:
            # Pharmacist and Medical Counter Assistant can update all fields
            cursor.execute("""
                UPDATE Delivery
                SET StaffID = %s, DeliveryDate = %s, DeliveryStatus = %s, DeliveryAddress = %s
                WHERE DeliveryID = %s
            """, (
                data.get('StaffID', delivery['StaffID']),
                data.get('DeliveryDate', delivery['DeliveryDate']),
                data.get('DeliveryStatus', delivery['DeliveryStatus']),
                data.get('DeliveryAddress', delivery['DeliveryAddress']),
                id
            ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Delivery updated successfully'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Delete Delivery ───────────────────────────────────────────────────────────

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
