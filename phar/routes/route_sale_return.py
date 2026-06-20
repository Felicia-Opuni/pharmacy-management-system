from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt

sale_return_bp = Blueprint('sale_return', __name__)


# ── Get All Sale Returns ──────────────────────────────────────────────────────

@sale_return_bp.route('/sale-return', methods=['GET'])
@jwt_required()
def get_all_sale_returns():
    """
    Returns all sale return records.
    Accessible by Pharmacists and CEO.
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') not in ['Pharmacist', 'CEO']:
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                sr.ReturnID,
                sr.SaleID,
                sr.BatchID,
                sr.ReturnDate,
                sr.QuantityReturned,
                sr.Reason,
                st.StaffFName,
                st.StaffSName,
                p.GenericName,
                p.BrandName
            FROM Sale_Return sr
            JOIN Staff st   ON sr.StaffID  = st.StaffID
            JOIN Batch b    ON sr.BatchID  = b.BatchID
            JOIN Product p  ON b.ProductID = p.ProductID
            ORDER BY sr.ReturnDate DESC
        """)
        returns = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(returns), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Get Sale Return by ID ─────────────────────────────────────────────────────

@sale_return_bp.route('/sale-return/<int:id>', methods=['GET'])
@jwt_required()
def get_sale_return_by_id(id):
    """
    Returns one sale return record by ReturnID.
    Accessible by Pharmacists and CEO.
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') not in ['Pharmacist', 'CEO']:
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                sr.ReturnID,
                sr.SaleID,
                sr.BatchID,
                sr.ReturnDate,
                sr.QuantityReturned,
                sr.Reason,
                st.StaffFName,
                st.StaffSName,
                p.GenericName,
                p.BrandName
            FROM Sale_Return sr
            JOIN Staff st   ON sr.StaffID  = st.StaffID
            JOIN Batch b    ON sr.BatchID  = b.BatchID
            JOIN Product p  ON b.ProductID = p.ProductID
            WHERE sr.ReturnID = %s
        """, (id,))
        sale_return = cursor.fetchone()
        cursor.close()
        conn.close()

        if sale_return is None:
            return jsonify({'message': 'Sale return not found'}), 404

        return jsonify(sale_return), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Record a New Sale Return ──────────────────────────────────────────────────

@sale_return_bp.route('/sale-return', methods=['POST'])
@jwt_required()
def add_sale_return():
    """
    Records a new sale return.
    When this is inserted, the database trigger trg_AfterSaleReturn
    will automatically:
      1. Add the returned quantity back to Batch stock
      2. Reduce the Sale_Item subtotal
      3. Recalculate the Sale TotalAmount

    Only Pharmacists and Cashiers can record a return.

    Expected JSON body:
    {
        "SaleID": 1,
        "BatchID": 2,
        "StaffID": 1,
        "ReturnDate": "2026-05-20",
        "QuantityReturned": 2,
        "Reason": "Customer received wrong medicine"
    }
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') not in ['Pharmacist', 'Cashier']:
            return jsonify({'message': 'Access denied'}), 403

        data = request.get_json()

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Check the Sale exists
        cursor.execute("SELECT * FROM Sale WHERE SaleID = %s", (data['SaleID'],))
        sale = cursor.fetchone()
        if not sale:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Sale not found'}), 404

        # Check the Sale_Item exists — confirms this product was actually sold in this sale
        cursor.execute(
            "SELECT * FROM Sale_Item WHERE SaleID = %s AND BatchID = %s",
            (data['SaleID'], data['BatchID'])
        )
        sale_item = cursor.fetchone()
        if not sale_item:
            cursor.close()
            conn.close()
            return jsonify({'message': 'This product was not part of that sale'}), 404

        # Make sure the quantity returned does not exceed the quantity originally sold
        if data['QuantityReturned'] > sale_item['QuantitySold']:
            cursor.close()
            conn.close()
            return jsonify({
                'message': f"Cannot return {data['QuantityReturned']}. Only {sale_item['QuantitySold']} were sold."
            }), 400

        # Insert the return — the trigger handles the rest automatically
        cursor.execute("""
            INSERT INTO Sale_Return (SaleID, BatchID, StaffID, ReturnDate, QuantityReturned, Reason)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['SaleID'],
            data['BatchID'],
            data['StaffID'],
            data['ReturnDate'],
            data['QuantityReturned'],
            data.get('Reason', None)
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Sale return recorded successfully. Stock has been updated.'}), 201
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Delete Sale Return ────────────────────────────────────────────────────────

@sale_return_bp.route('/sale-return/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_sale_return(id):
    """
    Deletes a sale return record.
    Only Pharmacists can delete a return.

    Important note: Deleting a return does NOT automatically reverse
    the stock changes made by the trigger when the return was first recorded.
    This is intentional — deletions should be rare and handled carefully.
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Sale_Return WHERE ReturnID = %s", (id,))
        sale_return = cursor.fetchone()

        if not sale_return:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Sale return not found'}), 404

        cursor.execute("DELETE FROM Sale_Return WHERE ReturnID = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Sale return deleted successfully'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
