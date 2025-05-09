from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from flask_cors import CORS
from functools import wraps
from werkzeug.utils import secure_filename
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import pandas as pd
import jwt
import datetime
import os
import random
import base64

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'flaskdb'
app.config['SECRET_KEY'] = 'Demo_123_main'
mysql=MySQL(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'panchalcodelabe@gmail.com'  # Your email here
app.config['MAIL_PASSWORD'] = 'hzyb xvja npel mdae'  # Your email password here
mail = Mail(app)

CORS(app)

otp_storage = {}


UPLOAD_FOLDER2 = 'static/uploads'
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
os.makedirs(UPLOAD_FOLDER2, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    # Define allowed file extensions
    allowed_extensions = {'xls', 'xlsx', 'csv'}
    
    # Check if the file has an extension and if it is in the allowed extensions list
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# JWT Token Verification
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_email = data['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM accounts WHERE email=%s AND password=%s", (email, password))
    account = cur.fetchone()

    if account:
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO accounts (full_name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    mysql.connection.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/logout', methods=['POST'])
@token_required
def logout():
    session.pop('user_id', None) 
    # Invalidate the token (in a real application, you would store it in a blacklist)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    if email:
        try:
            # Check if the email exists in the database
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM accounts WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                # Generate OTP and store it temporarily
                otp = random.randint(1000, 9999)
                otp_storage[email] = otp

                # Send OTP to the user's email
                msg = Message('Password Reset', sender='panchalcodelabe@', recipients=[email])
                msg.body = f'Your OTP for Password Reset is: {otp}'
                mail.send(msg)

                cursor.close()
                return jsonify({'message': 'OTP sent to your email.'}), 200
            else:
                cursor.close()
                return jsonify({'message': 'Email not found.'}), 404
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Email address not provided.'}), 400


@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if email and otp:
        # Check if the OTP matches
        if otp_storage.get(email) == int(otp):
            return jsonify({'message': 'OTP verified successfully.'}), 200
        else:
            return jsonify({'message': 'Invalid OTP.'}), 400
    else:
        return jsonify({'error': 'Email or OTP missing.'}), 400


@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')
    otp = data.get('otp')

    if email and new_password and otp:
        # Verify the OTP first
        if otp_storage.get(email) == int(otp):
            # Hash the new password
            hashed_password = new_password

            # Update the password in the database
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE accounts SET password = %s WHERE email = %s", (hashed_password, email))
            mysql.connection.commit()

            cursor.close()
            return jsonify({'message': 'Password reset successfully.'}), 200
        else:
            return jsonify({'message': 'Invalid OTP.'}), 400
    else:
        return jsonify({'error': 'Missing required fields (email, new_password, otp).'}), 400

@app.route('/add_phone', methods=['POST'])
@token_required
def add_phone():
    # Get form data
    brand = request.form.get('brand')
    model = request.form.get('model')
    ram = request.form.get('ram')
    storage = request.form.get('storage')
    camera = request.form.get('camera')
    battery = request.form.get('battery')
    price = request.form.get('price')
    image = request.files.get('image')
    print(brand, model, ram, storage, camera, battery, price, image)

    if 'image' not in request.files:
        return jsonify({'message': 'No image part in the request'}), 400

    if image.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER2'], filename)
        image.save(image_path)
        filepath = "http://127.0.0.1:5000/static/uploads/" + filename
        print(f"Image filename: {filepath}")
        cursor = mysql.connection.cursor()
    cursor.execute("""INSERT INTO phones (brand, model, ram, storage, camera, battery, price, image)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (brand, model, ram, storage, camera, battery, price, filepath))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Phone added successfully'}), 201

@app.route('/phones', methods=['GET'])
@token_required
def get_phones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM phones")
    phones = cur.fetchall()
    phone_list = [{
        "id": row[0],
        "brand": row[1],
        "model": row[2],
        "ram": row[3],
        "storage": row[4],
        "camera": row[5],
        "battery": row[6],
        "price": float(row[7]) if row[7] not in (None, '') else 0.0,
        "image": row[8] if row[8] else ""
    } for row in phones]
    return jsonify({"phones": phone_list}), 200

@app.route('/delete_phone/<int:id>', methods=['DELETE'])
@token_required
def delete_phone(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM phones WHERE id=%s", (id,))
    mysql.connection.commit()
    return jsonify({"message": "Phone deleted successfully"}), 200

# Update Phone with optional image
@app.route('/update_phone/<int:id>', methods=['PUT'])
@token_required
def update_phone(id):
    brand = request.form.get('brand')
    model = request.form.get('model')
    ram = request.form.get('ram')
    storage = request.form.get('storage')
    camera = request.form.get('camera')
    battery = request.form.get('battery')
    price = request.form.get('price')
    image = request.files.get('image')

    # Start building SQL
    update_query = """
        UPDATE phones SET brand=%s, model=%s, ram=%s, storage=%s,
        camera=%s, battery=%s, price=%s
    """
    values = [brand, model, ram, storage, camera, battery, price]

    if image:
        filename = secure_filename(image.filename)
        print(f"Image filename: {filename}")
        
        # Save image to local file system
        upload_path = os.path.join(app.config['UPLOAD_FOLDER2'], filename)
        image.save(upload_path)

        # Path to store in DB
        filepath = f"http://127.0.0.1:5000/static/uploads/{filename}"
        print(f"Image saved to {filepath}")
        
        update_query += ", image=%s"
        values.append(filepath)

    update_query += " WHERE id=%s"
    values.append(id)

    cur = mysql.connection.cursor()
    cur.execute(update_query, values)
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Phone updated successfully"}), 200

@app.route('/upload', methods=['POST'])
@token_required
def upload():
    print("FILES RECEIVED:", request.files)
    
    if 'excel_file' not in request.files:
        return jsonify({'message': 'No file part in request'}), 400

    file = request.files['excel_file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': 'Unsupported file type'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER2'], filename)
    file.save(filepath)

    # Read the file into a DataFrame
    if filename.endswith('.csv'):
        df = pd.read_csv(filepath)
        print("CSV DataFrame:", df.head())
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(filepath)
        print("Excel DataFrame:", df.head())
    else:
        return jsonify({'message': 'Unsupported file type'}), 400

    cur = mysql.connection.cursor()
    inserted_count = 0
    skipped_count = 0

    try:
        for _, row in df.iterrows():
            brand = str(row.get('brand', '')).strip()
            model = str(row.get('model', '')).strip()
            ram = str(row.get('ram', '')).strip()
            storage = str(row.get('storage', '')).strip()
            camera = str(row.get('camera', '')).strip()
            battery = str(row.get('battery', '')).strip()
            price = str(row.get('price', '')).strip()
            image_b64 = str(row.get('image_b64', '')).strip()
            check_sql = """
                SELECT 1 FROM phones WHERE brand=%s AND model=%s AND ram=%s AND storage=%s 
                AND camera=%s AND battery=%s AND price=%s AND image=%s
            """
            check_data = (brand, model, ram, storage, camera, battery, price, image_b64)
            cur.execute(check_sql, check_data)
            result = cur.fetchone()

            if result:
                skipped_count += 1
                continue  # Skip if duplicate is found

            # Insert new record
            insert_sql = """
                INSERT INTO phones (brand, model, ram, storage, camera, battery, price, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        # Commit to the database
            cur.execute(insert_sql, (brand, model, ram, storage, camera, battery, price, image_b64))
        mysql.connection.commit()

        return jsonify({
            'message': 'Upload complete',
            'inserted': inserted_count,
            'skipped_duplicates': skipped_count
        }), 200
    
    except Exception as e:
        mysql.connection.rollback()  # Rollback in case of error
        return jsonify({'message': 'Error inserting data', 'error': str(e)}), 500
    finally:
        cur.close()
def process_excel(file_path):
    # Load the workbook
    wb = load_workbook(file_path)
    sheet = wb.active

    # Iterate through the rows and handle images
    for image in sheet._images:
        # Image is embedded in the sheet
        img = image.ref
        print(f'Image found at {img}')

        # Saving the image to a specific folder
        img_file = image.image
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'images', img)
        with open(img_path, 'wb') as f:
            f.write(img_file)
    
    # You can also read data from the Excel file using pandas
    data = pd.read_excel(file_path, engine='openpyxl')
    print(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)