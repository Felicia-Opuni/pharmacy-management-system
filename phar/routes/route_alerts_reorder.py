from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt

alerts_bp = Blueprint('alerts', __name__)

# Roles allowed to view alerts
ALERT_ROLES = ['CEO', 'Pharmacist', 'Medical Counter Assistant']


# ── Expiry Alerts ────────────────────────────────────────────────────────────

@alerts_bp.route('/alerts/expiry', methods=['GET'])
@jwt_required()
def get_expiry_alerts():
    """
    Returns batches that will expire within the next 90 days.
    Uses the vw_ExpiryAlerts view from the database.
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') not in ALERT_ROLES:
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_expiryalerts")
        alerts = cursor.fetchall()
        cursor.close()
        conn.close()
        for alert in alerts:
            for key, value in alert.items():
                if hasattr(value, 'isoformat'):
                    alert[key] = value.isoformat()

        return jsonify(alerts), 200
        
    except Exception as e:
        
        return jsonify({'Error': str(e)}), 500


# ── Low Stock Alerts ─────────────────────────────────────────────────────────

@alerts_bp.route('/alerts/low-stock', methods=['GET'])
@jwt_required()
def get_low_stock_alerts():
    """
    Returns products that are Low in Stock or Out of Stock.
    Uses the vw_MonthlyInventoryReport view and filters by StockStatus.
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') not in ALERT_ROLES:
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM vw_MonthlyInventoryReport
            WHERE StockStatus IN ('Low Stock', 'Out of Stock')
        """)
        alerts = cursor.fetchall()
        cursor.close()
        conn.close()
        for alert in alerts:
             for key, value in alert.items():
                 if hasattr(value, 'isoformat'):
                    alert[key] = value.isoformat()

        return jsonify(alerts), 200
       
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Get All Reorder Suggestions ───────────────────────────────────────────────

@alerts_bp.route('/reorder', methods=['GET'])
@jwt_required()
def get_all_reorder_suggestions():
    """
    Returns all reorder suggestions.
    Uses the vw_PendingReorders view from the database.
    Only Pharmacists can access this.
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_PendingReorders")
        suggestions = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(suggestions), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Approve Reorder Suggestion ────────────────────────────────────────────────

@alerts_bp.route('/reorder/approve/<int:id>', methods=['PUT'])
@jwt_required()
def approve_reorder(id):
    """
    Approves a reorder suggestion.
    This calls the stored procedure sp_ApproveSuggestion,
    which moves the suggestion into a Purchase Order Item
    and then removes it from Reorder_Suggestion.
    Only Pharmacists can do this.
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # First check if the suggestion exists
        cursor.execute(
            "SELECT * FROM Reorder_Suggestion WHERE SuggestionID = %s",
            (id,)
        )
        suggestion = cursor.fetchone()

        if not suggestion:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Reorder suggestion not found'}), 404

        # Check it is still Pending — cannot approve a Rejected one
        if suggestion['SuggestionStatus'] != 'Pending':
            cursor.close()
            conn.close()
            return jsonify({
                'message': f"Cannot approve. Suggestion status is '{suggestion['SuggestionStatus']}'"
            }), 400

        # Call the stored procedure
        cursor.callproc('sp_ApproveSuggestion', [id])
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Reorder suggestion approved and added to Purchase Order'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Reject Reorder Suggestion ─────────────────────────────────────────────────

@alerts_bp.route('/reorder/reject/<int:id>', methods=['PUT'])
@jwt_required()
def reject_reorder(id):
    """
    Rejects a reorder suggestion with a reason.
    This calls the stored procedure sp_RejectSuggestion.
    Only Pharmacists can do this.

    Expected JSON body:
    {
        "RejectionReason": "We still have enough stock from another supplier"
    }
    """
    try:
        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403

        data = request.get_json()

        # RejectionReason is required
        rejection_reason = data.get('RejectionReason')
        if not rejection_reason:
            return jsonify({'message': 'RejectionReason is required'}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Check the suggestion exists
        cursor.execute(
            "SELECT * FROM Reorder_Suggestion WHERE SuggestionID = %s",
            (id,)
        )
        suggestion = cursor.fetchone()

        if not suggestion:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Reorder suggestion not found'}), 404

        # Check it is still Pending
        if suggestion['SuggestionStatus'] != 'Pending':
            cursor.close()
            conn.close()
            return jsonify({
                'message': f"Cannot reject. Suggestion status is '{suggestion['SuggestionStatus']}'"
            }), 400

        # Call the stored procedure
        cursor.callproc('sp_RejectSuggestion', [id, rejection_reason])
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Reorder suggestion rejected'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
