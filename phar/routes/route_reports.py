from flask import Blueprint, jsonify
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt

reports_bp = Blueprint('reports', __name__)

# Roles allowed to view all reports
REPORT_ROLES = ['CEO', 'Pharmacist', 'Medical Counter Assistant']


# ── Helper ──────────────────────────────────────────────────────────────────

def check_report_access(claims):
    """Return True if the staff member is allowed to view reports."""
    return claims.get('StaffRole') in REPORT_ROLES


# ── Daily Sales Report ───────────────────────────────────────────────────────

@reports_bp.route('/reports/daily-sales', methods=['GET'])
@jwt_required()
def get_daily_sales_report():
    """
    Returns all sales made today.
    Uses the vw_DailySalesReport view from the database.
    """
    try:
        claims = get_jwt()
        if not check_report_access(claims):
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_DailySalesReport")
        report = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(report), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Monthly Sales Report ─────────────────────────────────────────────────────

@reports_bp.route('/reports/monthly-sales', methods=['GET'])
@jwt_required()
def get_monthly_sales_report():
    """
    Returns total sales for the current month, grouped by product.
    Uses the vw_MonthlySalesReport view from the database.
    """
    try:
        claims = get_jwt()
        if not check_report_access(claims):
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_MonthlySalesReport")
        report = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(report), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Monthly Inventory Report ─────────────────────────────────────────────────

@reports_bp.route('/reports/inventory', methods=['GET'])
@jwt_required()
def get_inventory_report():
    """
    Returns current stock levels for all products.
    Shows whether each product is In Stock, Low Stock, or Out of Stock.
    Uses the vw_MonthlyInventoryReport view from the database.
    """
    try:
        claims = get_jwt()
        if not check_report_access(claims):
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_MonthlyInventoryReport")
        report = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(report), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Expiry Report ────────────────────────────────────────────────────────────

@reports_bp.route('/reports/expiry', methods=['GET'])
@jwt_required()
def get_expiry_report():
    """
    Returns products expiring within the next 30 days.
    Uses the vw_ExpiryReport view from the database.
    """
    try:
        claims = get_jwt()
        if not check_report_access(claims):
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_ExpiryReport")
        report = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(report), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Quarterly Performance Report ─────────────────────────────────────────────

@reports_bp.route('/reports/quarterly', methods=['GET'])
@jwt_required()
def get_quarterly_report():
    """
    Returns sales performance for the current quarter, grouped by product.
    Uses the vw_Quarterly_Performance_Report view from the database.
    """
    try:
        claims = get_jwt()
        if not check_report_access(claims):
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_Quarterly_Performance_Report")
        report = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(report), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# ── Annual Performance Report ────────────────────────────────────────────────

@reports_bp.route('/reports/annual', methods=['GET'])
@jwt_required()
def get_annual_report():
    """
    Returns a full yearly summary of units sold and units expired per product.
    Uses the vw_AnnualPerformanceReport view from the database.
    """
    try:
        claims = get_jwt()
        if not check_report_access(claims):
            return jsonify({'message': 'Access denied'}), 403

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_AnnualPerformanceReport")
        report = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(report), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
