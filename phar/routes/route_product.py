from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt

product_bp = Blueprint('product', __name__)

#fectch all products
@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_all_products():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_MonthlyInventoryReport")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(products)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'Error': str(e)}), 500
    
#add new product   
@product_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    try:
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()
         
        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("""
            INSERT INTO Product (CategoryName, GenericName, BrandName, SellingPrice, ReorderLevel)
            VALUES (%s, %s, %s, %s, %s)
            """, (
            data['CategoryName'],
            data['GenericName'],
            data['BrandName'],
            data['SellingPrice'],
            data['ReorderLevel']
            ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'Error': str(e)}), 500
    
#fetch product by id
@product_bp.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
    
        cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()

        if product is None:
            return jsonify({'message': 'Product not found'}), 404
        return jsonify(product)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'Error': str(e)}), 500


#update product by id
@product_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()

        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (id,))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Product not found'}), 404
        sql = """
            UPDATE Product
            SET CategoryName = %s, GenericName = %s, BrandName = %s, SellingPrice = %s, ReorderLevel = %s
            WHERE ProductID = %s
        """
        values = (    
            data.get('CategoryName', product['CategoryName']), 
            data.get('GenericName', product['GenericName']), 
            data.get('BrandName', product['BrandName']),
            data.get('SellingPrice', product['SellingPrice']), 
            data.get('ReorderLevel', product['ReorderLevel']),
            id
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product updated successfully'}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'Error': str(e)}), 500


#delete product by id
@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403

        cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (id,))
        product = cursor.fetchone()

        if not product:
            cursor.close()
            db.close()
            return jsonify({'message': 'Product not found'}), 404
        
        # Check if product has any batches
        cursor.execute("SELECT COUNT(*) AS batch_count FROM Batch WHERE ProductID = %s", (id,))
        result = cursor.fetchone()

        if result['batch_count'] > 0:
            cursor.close()
            db.close()
            return jsonify({
                'message': 'Cannot delete this product because it has existing batches linked to it.'
            }), 400
        
        cursor.execute("DELETE FROM Product WHERE ProductID = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Product deleted successfully'}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'Error': str(e)}), 500
    