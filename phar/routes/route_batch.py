from flask import Blueprint, jsonify, request
from db import get_db
from flask_jwt_extended import jwt_required, get_jwt

batch_bp = Blueprint('batch', __name__)

#fetch all batches 
@batch_bp.route('/batch', methods = ['GET'])
@jwt_required()
def get_all_batch():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Batch")
        batch=cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(batch)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    

#fetch batch by id
@batch_bp.route('/batch/<int:id>', methods = ['GET'])
@jwt_required()
def get_batch_by_id(id):
    try:
        conn=get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Batch WHERE BatchID = %s", (id,))
        batch=cursor.fetchone()
        cursor.close()
        conn.close()

        if batch is None:
            return jsonify({'message': 'Batch not found'}), 404
        return jsonify(batch)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


#add new batch
@batch_bp.route('/batch', methods=['POST'])
@jwt_required()
def add_batch():
    try:
        data=request.get_json()
        conn = get_db()
        cursor = conn.cursor()
        
        
        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("""
                INSERT INTO Batch (ProductID, PurchaseID, BatchNumber, ExpiryDate, ManufacturingDate, CostPrice, QuantityRecieved, QuantityRemaining)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                      """,(
                        data['ProductID'],
                        data['PurchaseID'],
                        data['BatchNumber'],
                        data['ExpiryDate'],
                        data['ManufacturingDate'],
                        data['CostPrice'],
                        data['QuantityRecieved'],
                        data['QuantityRemaining']
                      ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Batch added successfully'}), 201
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


#update batch by id
@batch_bp.route('/batch/<int:id>', methods=['PUT'])
@jwt_required()
def update_batch_by_id(id):
    try:
        data=request.get_json()
        conn=get_db()
        cursor=conn.cursor(dictionary=True)

        claims=get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Accessed denied'}), 403
        
        cursor.execute("SELECT * FROM Batch WHERE BatchID = %s", (id,))
        batch=cursor.fetchone()

        if not batch:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Batch not found'}), 404
        
        cursor.execute("UPDATE Batch SET ProductID = %s, PurchaseID = %s, BatchNumber = %s, ExpiryDate = %s, ManufacturingDate = %s, CostPrice = %s, QuantityRecieved = %s, QuantityRemaining = %s WHERE BatchID = %s", (
            data.get('ProductID', batch["ProductID"]),
            data.get('PurchaseID', batch["PurchaseID"]),
            data.get('BatchNumber', batch["BatchNumber"]),
            data.get('ExpiryDate', batch["ExpiryDate"]),
            data.get('ManufacturingDate', batch["ManufacturingDate"]),
            data.get('CostPrice', batch["CostPrice"]),
            data.get('QuantityReceived', batch['QuantityReceived']),
            data.get('QuantityRemaining', batch['QuantityRemaining']),
            id
            ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Batch successfully updated'})
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


#delete batch by id
@batch_bp.route('/batch/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_batch_by_id(id):
    try:
        conn=get_db()
        cursor=conn.cursor()

        claims = get_jwt()
        if claims.get('StaffRole') != 'Pharmacist':
            return jsonify({'message': 'Access denied'}), 403
        
        cursor.execute("SELECT * FROM Batch WHERE BatchID = %s", (id,))
        batch = cursor.fetchone()
        if not batch:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Batch not found'}), 404
    
        cursor.execute("DELETE FROM Batch WHERE BatchID = %s", (id,))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Batch successfully deleted'}), 201
    except Exception as e:
        return jsonify({'Error': str(e)}), 500     



