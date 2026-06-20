from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from db import get_db
from flask_jwt_extended import JWTManager
from datetime import timedelta



from routes.route_product import product_bp
from routes.route_supplier import supplier_bp
from routes.route_staff import staff_bp
from routes.route_customer import customer_bp
from routes.route_batch import batch_bp
from routes.route_purchase import purchase_bp
from routes.route_alerts_reorder import alerts_bp
from routes.route_reports import reports_bp
from routes.route_sale import sale_bp


# app = Flask(__name__)
app = Flask(__name__, static_folder='review', static_url_path='/review')
CORS(app)


app.config['JWT_SECRET_KEY'] = 'pharmacy_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)
jwt = JWTManager(app)


app.register_blueprint(staff_bp)
app.register_blueprint(product_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(batch_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(sale_bp)

#new changes
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/login')
def login_page():
    return send_from_directory('review', 'login.html')
#new changes end

# ID Format Functions
def format_product_id(id):   return f"P{str(id).zfill(3)}"
def format_sale_id(id):      return f"S{str(id).zfill(3)}"
def format_customer_id(id):  return f"C{str(id).zfill(3)}"
def format_staff_id(id):     return f"ST{str(id).zfill(3)}"
def format_supplier_id(id):  return f"SUP{str(id).zfill(3)}"
def format_batch_id(id):     return f"B{str(id).zfill(3)}"
def format_delivery_id(id):  return f"D{str(id).zfill(3)}"
def format_record_id(id):    return f"R{str(id).zfill(3)}"
def format_purchase_id(id):  return f"PUR{str(id).zfill(3)}"
def format_order_id(id):     return f"ORD{str(id).zfill(3)}"

@app.route('/')
def home():
    return 'Pharmacy System is running!'

    
if __name__ == '__main__':
    app.run(debug=True)