# ---------------------- Imports ------------------------
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
from io import BytesIO
import os
import smtplib
from PIL import Image
from flask import Flask, Response, jsonify, redirect, request, send_file, send_from_directory, session, url_for
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, get_jwt_identity, jwt_required
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import Flask, request, jsonify
from urllib.parse import quote

from summarizer import summarize_text
from groq_model import call_groq_api

from functions import (
    get_bitrate, plot_silence_speech_ratio_pie, 
    plot_waveform_with_peak, plot_loudness, 
    calculate_decibels_with_sampling_rate, plot_waveform_with_sampling_rate, 
    calculate_file_size, plot_harmonicity, plot_frequency_spectrum, 
    estimate_tempo
)
from transcription import perform_transcription
from diarizationM import perform_speaker_diarization

# ---------------------- Configuration ------------------------
allowed_origins = [
    "http://localhost:3000",
    "http://localhost"
]

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)
app.secret_key = os.urandom(24)
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=9)  # Set JWT expiration
jwt = JWTManager(app)

@app.route('/uploads/diarization/<path:filename>')
def serve_file(filename):
    return send_from_directory('uploads/diarization', filename)

@app.route('/uploads/features/<path:filename>')
def serve_feature_file(filename):
    return send_from_directory('uploads/features', filename)

# ---------------------- Helper Functions ------------------------
def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            print(f"Claims: {claims}")  # Debugging: Print claims
            user_role = claims.get('role', 'user')  # Default to 'user' if not found
            if user_role not in allowed_roles:
                return jsonify({"message": f"Access forbidden: Requires one of the roles {allowed_roles}"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='audio',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        port=3306,
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        role ENUM('admin', 'user', 'guest') DEFAULT 'user' NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS features (
                    audio_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    filename VARCHAR(255) NOT NULL,
                    bitrate INT NOT NULL,
                    loudness_plot_path VARCHAR(255) NOT NULL,
                    waveform_plot_path VARCHAR(255) NOT NULL,
                    silence_speech_ratio_plot_path VARCHAR(255) NOT NULL,
                    frequency_plot_path VARCHAR(255) NOT NULL,
                    plot_path_sr VARCHAR(255) NOT NULL,
                    harmonicity_plot_path VARCHAR(255) NOT NULL,
                    decibels DECIMAL(5, 2),
                    tempo DECIMAL(5, 2),
                    file_size DECIMAL(10, 2),
                    FOREIGN KEY (user_id) REFERENCES users(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transcription (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT DEFAULT NULL,
                        filename VARCHAR(255) DEFAULT NULL,
                        transcription_output_file VARCHAR(255) DEFAULT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS diarization (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        filename VARCHAR(255) NOT NULL,
                        diarization_output_file VARCHAR(255) NOT NULL,
                        diarization_graph_output VARCHAR(255) NOT NULL)''')

    conn.commit()
    cursor.close()
    conn.close()

init_db()

def send_email(to_email, subject, body):
    from_email = "audioapp655@gmail.com"
    from_password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_login_email(to_email):
    subject = "Login Successful"
    body = "Dear user,\n\nYou have successfully logged into your account.\n\nBest regards,\nAudio App Team"
    send_email(to_email, subject, body)

def send_signup_email(to_email):
    subject = "Welcome to Our Services"
    body = "Dear user,\n\nYou have successfully created your account.\n\nBest regards,\nAudio App Team"
    send_email(to_email, subject, body)

def ensure_directories():
    if not os.path.exists('database'):
        os.makedirs('database')
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

ensure_directories()

# =================== All Routes ===================

# ---------------------Route # 01------------------------

@app.route('/')
def index():
    return "This is home page route, Welcome Here."

# Signup Route
@app.route('/signup', methods=['POST'])
@cross_origin() 
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    role = data.get('role', 'user')  # Role provided by the client or default to 'user'

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)', 
                       (username, email, password, role))
        conn.commit()
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        id = cursor.fetchone()['id']
        access_token = create_access_token(identity={'username': username, 'email': email, 'user_id': id, 'role': role})
        send_signup_email(email)
        return jsonify(access_token=access_token), 200
    except pymysql.MySQLError:
        return jsonify({"message": "Username or email already exists."}), 409
    finally:
        conn.close()


# ---------------------Route # 02------------------------

@app.route('/login', methods=['POST'])
@cross_origin() 
def login():
    data = request.json  # Get the JSON payload from the request
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400  # Return error if either is missing

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the user exists in the database
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            # If password is correct, create JWT token
            token = create_access_token(identity={'username': user['username'], 'email': user['email'], 'user_id': user['id'], 'role': user['role']})
            
            # Send a login notification email (optional, if implemented)
            send_login_email(user['email'])
            
            # Return the access token
            return jsonify(token=token), 200
        else:
            # Invalid credentials
            return jsonify({"message": "Invalid login credentials"}), 401
    finally:
        conn.close()  # Close the connection in the finally block to ensure it always closes

# --------- Login / Signup with Github ----------

# GitHub OAuth registration
oauth = OAuth(app)

github = oauth.register(
    name='github',
    client_id='Ov23lioBQHMEhpVm49bn',
    client_secret='16698dcf970bb8164900b8bd181acb4802764da7',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    redirect_uri='http://127.0.0.1:5000/github/callback',
    scope='user:email',
)

@app.route('/login_with_github', methods=['GET'])
def login_with_github():
    # Redirect user to GitHub authorization page
    return github.authorize_redirect(url_for('github_callback', _external=True))

@app.route('/github/callback', methods=['GET'])
def github_callback():
    try:
        # Retrieve token from GitHub
        token = github.authorize_access_token()
        if not token:
            return jsonify({"error": "Authorization failed"}), 400

        # Get user info from GitHub API
        user_info = github.get('https://api.github.com/user').json()

        # Fallback to create an email in case GitHub doesn't provide one
        email = user_info.get('email') or f"{user_info['login']}@github.com"
        username = user_info['login']

        # Database operation
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()

            if user:
                # User exists, generate access token
                token = create_access_token(identity={'username': user['username'], 'email': user['email'], 'user_id': user['id'], 'role': user['role']})
                print(f"Access token generated: {token}")
            else:
                password = "github"
                # New user, insert into the database and generate access token
                cursor.execute(
                    'INSERT INTO users (username,password, email) VALUES (%s, %s)', 
                    (username,password, email)
                )
                conn.commit()
                token = create_access_token(identity={'username': user['username'], 'email': user['email'], 'user_id': user['id'], 'role': user['role']})
                print(f"Access token generated: {token}")


        return redirect(f"http://localhost:3000/?access_token={token}")

    except Exception as e:
        # Return an error response in JSON format
        return jsonify({"error": f"Error during GitHub OAuth: {str(e)}"}), 500
    
# --------- Login / Signup with Google ----------

import json
import os
from flask import jsonify, session, request
from flask_jwt_extended import create_access_token

# Load Google client secrets from JSON securely
with open(os.path.join(os.path.dirname(__file__), 'client_secrets.json'), 'r') as f:
    client_secrets = json.load(f)

# Register Google OAuth
google = oauth.register(
    name='google',
    client_id=client_secrets['web']['client_id'],
    client_secret=client_secrets['web']['client_secret'],
    authorize_url=client_secrets['web']['auth_uri'],
    access_token_url=client_secrets['web']['token_uri'],
    redirect_uri='http://127.0.0.1:5000/callback',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
)

@app.route('/login_with_google', methods=['GET'])
def login_with_google():
    # Create a nonce for security purposes
    session['nonce'] = os.urandom(24).hex()
    # Redirect the user to Google's OAuth consent screen
    return google.authorize_redirect(url_for('authorized', _external=True), nonce=session['nonce'])

@app.route('/callback', methods=['GET'])
def authorized():
    try:
        # Get token from Google
        token = google.authorize_access_token()
        if not token:
            return jsonify({"error": "Authorization failed"}), 400

        # Parse ID token to get user info
        userinfo = google.parse_id_token(token, nonce=session.pop('nonce', None))
        email = userinfo['email']
        username = userinfo.get('name', email.split('@')[0])

        # Database operation
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()

            if user:
                # If the user exists, generate an access token for login
                token = create_access_token(identity={
                    'username': user['username'],
                    'email': user['email'],
                    'user_id': user['id'],
                    'role': user['role']
                })
                print(f"Access token generated for existing user: {token}")

            else:
                # If the user is new, insert their details
                cursor.execute(
                    'INSERT INTO users (username, email) VALUES (%s, %s)', 
                    (username, email)
                )
                conn.commit()

                # After inserting, fetch the user again to get the details
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                new_user = cursor.fetchone()
                
                # Generate an access token for the new user
                token = create_access_token(identity={
                    'username': new_user['username'],
                    'email': new_user['email'],
                    'user_id': new_user['id'],
                    'role': new_user['role']
                })
                print(f"Access token generated for new user: {token}")

        # Redirect with the access token
        return redirect(f"http://localhost:3000/?access_token={quote(token)}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# ---------------------Route # 03------------------------

def dict_fetch_all(cursor):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@app.route('/profile', methods=['GET'])
@cross_origin()
@jwt_required()
def profile():
    user_identity = get_jwt_identity()
    print(f"User Identity: {user_identity}")  # Debugging: Log user identity

    username = user_identity.get('username')
    if not username:
        return jsonify({"error": "Invalid token"}), 401

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Fetch user profile
                cursor.execute('SELECT username, email, role FROM users WHERE username = %s', (username,))
                profile = dict_fetch_all(cursor)

                if not profile:
                    return jsonify({"error": "User profile not found"}), 404

                # Fetch user uploads from the 'features' table (renamed from 'uploads')
                cursor.execute('SELECT * FROM features WHERE user_id = %s', (profile[0]['id'],))
                uploads = dict_fetch_all(cursor)

                # Build the profile response
                user_profile = {
                    "username": profile[0]['username'],
                    "email": profile[0]['email'],
                    "role": profile[0]['role'],
                    "uploads": uploads  # Attach the uploaded audios here
                }

                return jsonify(user_profile), 200

    except Exception as e:
        print(f"Error: {str(e)}")  # Log any errors
        return jsonify({"error": str(e)}), 500
        
# ---------------------Route # 04------------------------

@app.route('/features', methods=['GET', 'POST'])
# @cross_origin()
@jwt_required()  # Use JWT authentication
@role_required('user', 'admin')  # Restricting access to users and admins
def features():
    if request.method == 'OPTIONS':
        return '', 200  # Handle CORS preflight request
    
    # Extract identity from the JWT token
    user_identity = get_jwt_identity()

    identity = user_identity
    if not identity:
        return jsonify({"error": "Unauthorized access"}), 401

    # Assuming the token contains 'username', 'user_id'
    username = identity.get('username')
    user_email = identity.get('email')
    user_id = identity.get('user_id')
    print(f"username: {username}, user_email: {user_email}, user_id: {user_id}")

    if not username or not user_email:
        return jsonify({"error": "Unauthorized access"}), 401
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if not (file.filename.lower().endswith('.mp3') or file.filename.lower().endswith('.wav')):
            return jsonify({"error": "Unsupported file format. Only .mp3 and .wav are allowed."}), 400
        
        # Add timestamp to the filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = secure_filename(f"{timestamp}_{file.filename}")
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        # Check if the file is saved successfully
        if not os.path.exists(file_path):
            return jsonify({"error": "Error saving the file"}), 500
    
        # Calculate the bitrate using the get_bitrate function
        bitrate = get_bitrate(file_path)
        
        # Check if bitrate calculation is successful
        if bitrate is None:
            return jsonify({"error": "Error calculating bitrate"}), 500
        
        # username = session.get('username')  # Get username from session

        # Plot the waveform with sampling rate and save the plot
        plot_path_sr = plot_waveform_with_sampling_rate(file_path, filename, username)

        # Calculate decibels with sampling rate
        decibels_value = calculate_decibels_with_sampling_rate(file_path, bitrate)
        decibels_with_units = f"{decibels_value:.2f} dB"

        # Plot the loudness and save the plot
        loudness_plot_path = plot_loudness(file_path, filename, username)
        
        # Plot the waveform with peak and save the plot
        waveform_plot_path = plot_waveform_with_peak(file_path, filename, username)

        # Plot the silence-speech ratio pie chart and save the plot
        silence_speech_ratio_plot_path = plot_silence_speech_ratio_pie(file_path, filename, username)

        # Plot harmonicity and save the plot
        harmonicity_plot_path = plot_harmonicity(file_path, filename, username)

        # Plot the frequency spectrum and save the plot
        frequency_plot_path = plot_frequency_spectrum(file_path, filename, username)

        # Estimate tempo and save the tempo value
        tempo = estimate_tempo(file_path)

        # Calculate the file size
        file_size_mb = calculate_file_size(file_path)
        
        # user_id = session.get('user_id')  # Get user_id from session

        # Connect to MySQL database
        conn = get_db_connection()
        cursor = conn.cursor()
        print(f"User ID: {user_id}")
        
        try:
            # Insert upload details into MySQL database
            # Insert upload details into MySQL database
            cursor.execute('''INSERT INTO features 
                            (user_id, filename, bitrate, loudness_plot_path, waveform_plot_path, 
                            silence_speech_ratio_plot_path, frequency_plot_path, plot_path_sr, 
                            harmonicity_plot_path, decibels, tempo, file_size) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                        (user_id, filename, bitrate, loudness_plot_path, waveform_plot_path, 
                            silence_speech_ratio_plot_path, frequency_plot_path, plot_path_sr, 
                            harmonicity_plot_path, decibels_value, tempo, file_size_mb))

            audio_id = cursor.lastrowid
            conn.commit()
        except pymysql.MySQLError as e:
            return jsonify({"error": f"Error uploading file to database {e}"}), 500
        finally:
            conn.close()

        try:
            response = jsonify({
            "audio_id": audio_id,
            "filename": filename,
            "bitrate": f"{bitrate} kbps",
            "decibels": decibels_with_units,
            "tempo": tempo,
            "file_size": f"{file_size_mb:.2f} MB",
            "plot_paths": {
                "waveform_with_sr": plot_path_sr,
                "loudness": loudness_plot_path,
                "waveform_with_peak": waveform_plot_path,
                "silence_speech_ratio": silence_speech_ratio_plot_path,
                "harmonicity": harmonicity_plot_path,
                "frequency_spectrum": frequency_plot_path
            }
            })
            response.status_code = 200
            # Return the extracted features and paths as JSON
            return response
        except Exception as e:
            return jsonify({"message": f"Method not allowed. Use POST method to extract features. Error: {e}"}), 405

@app.route('/download_record/<int:record_id>') 
@jwt_required()  
# @role_required('user', 'admin')  # Restricting access to users and admins
def download_record(record_id):
    user_identity = get_jwt_identity()

    if not user_identity:
        return jsonify({"error": "Unauthorized access no identify"})
    # Assuming the token contains 'username' and 'user_id'
    user_id = user_identity.get('user_id')
    username = user_identity.get('username')

    # Connect to MySQL database
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # Use DictCursor for dictionary output
    cursor.execute('SELECT * FROM features WHERE audio_id = %s AND user_id = %s', (record_id, user_id))
    upload = cursor.fetchone()  # Fetch a single record
    conn.close()

    if not upload:
        return jsonify({'error': 'Record not found'}), 404

    # Removing timestamp from filename
    filename_parts = upload['filename'].split('_', 1)
    original_filename = filename_parts[1] if len(filename_parts) > 1 else upload['filename']

    # Create a PDF file
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    page_number = 1

    # Function to add text to PDF with pagination
    def add_text_to_pdf(content, start_x, start_y, line_height):
        nonlocal y_position, page_number
        lines = content.split('\n')
        for line in lines:
            if y_position < 100:  # Check if we need a new page
                add_page_number(c, page_number)
                c.showPage()
                page_number += 1
                c.setFont("Helvetica-Bold", 16)
                c.drawString(100, height - 50, "Audio Record Analysis (continued)")
                c.setFont("Helvetica", 12)
                y_position = height - 80
            c.drawString(start_x, y_position, line)
            y_position -= line_height

    # Function to add images to PDF with pagination
    def add_image_to_pdf(image_path, description, c, y_position):
        nonlocal page_number
        if y_position < 100:
            add_page_number(c, page_number)
            c.showPage()
            page_number += 1
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, height - 50, "Audio Record Analysis (continued)")
            c.setFont("Helvetica", 12)
            y_position = height - 80
        c.drawString(100, y_position, description)
        y_position -= 20
        image = Image.open(image_path)
        aspect = image.height / float(image.width)
        c.drawInlineImage(image, 100, y_position - 200 * aspect, width=400, height=200 * aspect)
        return y_position - 200 * aspect - 30

    # Function to add page numbers
    def add_page_number(c, page_number):
        c.setFont("Helvetica", 10)
        c.drawString(width - 50, 30, f"Page {page_number}")

    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Audio Record Analysis")
    c.setFont("Helvetica", 12)
    try:
        # Add metadata
        y_position = height - 80
        c.drawString(100, y_position, f"Name: {username}")
        y_position -= 20
        c.drawString(100, y_position, f"File Name: {original_filename}")
        y_position -= 20
        c.drawString(100, y_position, f"Bitrate: {upload['bitrate']} kbps")
        y_position -= 20
        c.drawString(100, y_position, f"Tempo: {upload['tempo']} BPM")
        y_position -= 20
    except Exception as e:
        print("-------->" + str(e))
        return jsonify({'error': 'Error generating text in PDF: ' + str(e)}), 500

    # Draw images
    try:
        # y_position = add_image_to_pdf(upload['plot_path_decibels'].replace('\\', '/'), "Loudness Plot", c, y_position)
        y_position = add_image_to_pdf(upload['waveform_plot_path'].replace('\\', '/'), "Waveform Plot", c, y_position)
        y_position = add_image_to_pdf(upload['silence_speech_ratio_plot_path'].replace('\\', '/'), "Silence/Speech Ratio Plot", c, y_position)
        y_position = add_image_to_pdf(upload['frequency_plot_path'].replace('\\', '/'), "Frequency Plot", c, y_position)
        y_position = add_image_to_pdf(upload['plot_path_sr'].replace('\\', '/'), "Sampling Rate Plot", c, y_position)
        y_position = add_image_to_pdf(upload['harmonicity_plot_path'].replace('\\', '/'), "Harmonicity Plot", c, y_position)
    except Exception as e:
        print("-------->" + str(e))
        return jsonify({'error': 'Error generating images in PDF: ' + str(e)}), 500

    add_page_number(c, page_number)
    c.save()

    # Save the PDF file to disk temporarily
    pdf_filename = f"{original_filename}_features.pdf"
    pdf_path = os.path.join("uploads/features", pdf_filename.replace(':', '_'))  # Replace illegal characters in filename
    try:
        with open(pdf_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
    finally:
        pdf_buffer.close()  # Ensure the buffer is closed

    # Send the PDF file as a response
    return send_file(pdf_path, as_attachment=True)

    # Remove the PDF file from disk after sending
    # try:
    #     os.remove(pdf_path)
    # except Exception as e:
    #     print(f"Error while removing file: {e}")

    # return response

app.route('/uploads/<string:path>', methods=['GET'])
def serve_feature_file(path):
    return send_from_directory('uploads/features', path)

# ---------------------Route # 05------------------------

@app.route('/diarization', methods=['POST'])
# @cross_origin()
@jwt_required()  # Use JWT authentication
@role_required('user', 'admin')  # Restrict access to users and admins
def diarization():
    if request.method == 'OPTIONS':
        return '', 200  # Handle CORS preflight request

    # Extract identity from the JWT token
    user_identity = get_jwt_identity()

    identity = user_identity
    if not identity:
        return jsonify({"error": "Unauthorized access"}), 401

    # Assuming the token contains 'username', 'user_id'
    username = identity.get('username')
    print(username)
    user_email = identity.get('email')
    user_id = identity.get('user_id')

    if not username or not user_email:
        return jsonify({"error": "Unauthorized access"}), 401

    # If the request method is POST
    if request.method == 'POST':
        # Check if the 'file' part is in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        # Check if the user has selected a file
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Check for valid file extensions
        if not (file.filename.lower().endswith('.mp3') or file.filename.lower().endswith('.wav')):
            return jsonify({'error': 'Unsupported file format. Only .mp3 and .wav are allowed.'}), 400

        # Add a timestamp to the filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = secure_filename(f"{timestamp}_{file.filename}")
        file_path = os.path.join('uploads', filename)

        try:
            # Save the file to the uploads folder
            file.save(file_path)
        except Exception as e:
            return jsonify({'error': 'Error saving the file', 'details': str(e)}), 500

        # Verify if the file was saved successfully
        if not os.path.exists(file_path):
            return jsonify({'error': 'File saving failed'}), 500

        try:
            diarization_output_file, diarization_graph_output = perform_speaker_diarization(filename, username, file_path)
        except Exception as e:
            return jsonify({'error': 'Diarization failed', 'details': str(e)}), 500

        # If diarization fails or the function returns None
        if not diarization_output_file or not diarization_graph_output:
            return jsonify({'error': 'Diarization failed'}), 500

        # Connect to the MySQL database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Insert into the diarization table
            cursor.execute(
                'INSERT INTO diarization (user_id, filename, diarization_output_file, diarization_graph_output) VALUES (%s, %s, %s, %s)',
                (user_id, filename, diarization_output_file, diarization_graph_output)
            )
            audio_id = cursor.lastrowid
            conn.commit()
        except pymysql.MySQLError as e:
            print(f"SQL Error: {e}") 
            return jsonify({'error': 'Error saving diarization data to database', 'details': str(e)}), 500
        finally:
            conn.close()

        # Parse diarization content
        diarization_content = []
        colors = {
            'SPEAKER_00': 'blue',
            'SPEAKER_01': 'red',
            'SPEAKER_02': 'green',
            'SPEAKER_03': 'purple'
        }

        try:
            with open(diarization_output_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.split("from")
                    if len(parts) > 1:
                        speaker = parts[0].split()[1]
                        time_part = parts[1].split(":")[0].strip() if len(parts[1].split(":")) > 0 else ''
                        content = parts[1].split(":")[1].strip() if len(parts[1].split(":")) > 1 else ''
                        color = colors.get(speaker, 'black')
                        diarization_content.append({
                            'speaker': speaker,
                            'time': time_part,
                            'content': content,
                            'color': color
                        })
        except Exception as e:
            return jsonify({'error': 'Error reading diarization output file', 'details': str(e)}), 500

        response = jsonify({
            'audio_id': audio_id,
            'filename': filename,
            'diarization_output_file': diarization_output_file,
            'diarization_graph_output': diarization_graph_output,
            'diarization_content': diarization_content
        })
        response.status_code = 200
        # response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return jsonify({'message': 'Method not allowed. Use POST to upload and perform diarization.'}), 405
    
# ---------------------Route # 06------------------------

@app.route('/download_diarization/<int:record_id>')
@jwt_required() 
@role_required('user', 'admin')  # Restricting access to users and admins
def download_diarization(record_id):
    user_identity = get_jwt_identity()

    identity = user_identity
    if not identity:
        return jsonify({"error": "Unauthorized access"}), 401

    # Assuming the token contains 'username', 'user_id'
    username = identity.get('username')
    
    # Connect to MySQL database
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # Use DictCursor for dictionary output

    # Fetch diarization record based on record_id
    cursor.execute('SELECT * FROM diarization WHERE id = %s', (record_id,))
    upload = cursor.fetchone()
    conn.close()
    
    if not upload:
        return jsonify({"error": "Record not found"}), 404  # Return 404 if not found

    # Removing timestamp from filename
    filename_parts = upload['filename'].split('_', 1)
    original_filename = filename_parts[1] if len(filename_parts) > 1 else upload['filename']

    # Create a PDF file
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    page_number = 1

    # Function to add text to PDF with pagination
    def add_text_to_pdf(content, start_x, start_y, line_height):
        nonlocal y_position, page_number
        lines = content.split('\n')
        for line in lines:
            if y_position < 100:  # Check if we need a new page
                add_page_number(c, page_number)
                c.showPage()
                page_number += 1
                c.setFont("Helvetica-Bold", 16)
                c.drawString(100, height - 50, "Audio Record Analysis (continued)")
                c.setFont("Helvetica", 12)
                y_position = height - 80
            c.drawString(start_x, y_position, line)
            y_position -= line_height

    # Function to add images to PDF with pagination
    def add_image_to_pdf(image_path, description, c, y_position):
        nonlocal page_number
        if y_position < 100:
            add_page_number(c, page_number)
            c.showPage()
            page_number += 1
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, height - 50, "Audio Record Analysis (continued)")
            c.setFont("Helvetica", 12)
            y_position = height - 80
        c.drawString(100, y_position, description)
        y_position -= 20
        image = Image.open(image_path)
        aspect = image.height / float(image.width)
        c.drawInlineImage(image, 100, y_position - 200 * aspect, width=400, height=200 * aspect)
        return y_position - 200 * aspect - 30

    # Function to add page numbers
    def add_page_number(c, page_number):
        c.setFont("Helvetica", 10)
        c.drawString(width - 50, 30, f"Page {page_number}")

    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Diarization Analysis")
    c.setFont("Helvetica", 12)

    # Add metadata
    y_position = height - 80
    c.drawString(100, y_position, f"Name: {username}")
    y_position -= 20
    c.drawString(100, y_position, f"File Name: {original_filename}")
    y_position -= 20

    # Draw images
    y_position = add_image_to_pdf(upload['diarization_graph_output'].replace('\\', '/'), "Diarization Plot", c, y_position)

    # Read diarization content from file and add to PDF
    if 'diarization_output_file' in upload:
        diarization_output_file = upload['diarization_output_file']
        if os.path.exists(diarization_output_file):
            with open(diarization_output_file, 'r', encoding='utf-8') as f:
                diarization_content = f.read()
                y_position -= 40
                c.setFont("Helvetica", 12)
                c.drawString(100, y_position, "Diarization Content:")
                y_position -= 20
                add_text_to_pdf(diarization_content, 120, y_position, 15)
        else:
            return jsonify({"error": "Diarization content file not found."}), 404

    add_page_number(c, page_number)
    c.save()

    # Save the PDF file to disk temporarily
    pdf_filename = f"{original_filename}_diarization.pdf"
    pdf_path = os.path.join("uploads/diarization", pdf_filename.replace(':', '_'))  # Replace illegal characters in filename

    try:
        with open(pdf_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
    finally:
        # Close the pdf_buffer
        pdf_buffer.close()

    # Send the PDF file as a response
    response = send_file(pdf_path, mimetype='application/pdf', as_attachment=True)

    # Remove the PDF file from disk after sending
    try:
        os.remove(pdf_path)
    except Exception as e:
        print(f"Error while removing file: {e}")

    return response

app.route('/uploads/<string:path>', methods=['GET'])
def send_report(path):
    print(path)
    return send_from_directory('uploads/diarization', path)

# ---------------------Route # 07------------------------

@app.route('/transcription', methods=['POST'])
@jwt_required()  # Use JWT authentication
@role_required('user', 'admin')  # Restrict access to users and admins
def transcription():
    if request.method == 'OPTIONS':
          return '', 200
    # Extract identity from the JWT token
    user_identity = get_jwt_identity()

    identity = user_identity
    if not identity:
        return jsonify({"error": "Unauthorized access no identify"})
    # Assuming the token contains 'username' and 'user_id'
    username = identity.get('username')
    user_email = identity.get('email')
    user_id = identity.get('user_id')

    if not username or not user_email:
        print("Unauthorized access")
        return jsonify({"error": "Unauthorized access"}), 401

    # If the request method is POST
    if request.method == 'POST':
        # Check if the 'file' part is in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        print(request.files)
        
        # Check if the user has selected a file
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Check for valid file extensions
        if not (file.filename.lower().endswith('.mp3') or file.filename.lower().endswith('.wav')):
            return jsonify({"error": "Unsupported file format. Only .mp3 and .wav are allowed."}), 400
        
        # Add a timestamp to the filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = secure_filename(f"{timestamp}_{file.filename}")
        file_path = os.path.join('uploads', filename)
        
        try:
            # Save the file to the uploads folder
            file.save(file_path)
        except Exception as e:
            return jsonify({"error": "Error saving the file", "details": str(e)}), 500
        
        # Verify if the file was saved successfully
        print(file_path)
        if not os.path.exists(file_path):
            return jsonify({"error": "File saving failed"}), 500
        
        # Perform transcription (make sure `perform_transcription` function is correct)
        try:
            transcription_output_file = perform_transcription(filename, username, file_path)
        except Exception as e:
            return jsonify({"error": "Transcription failed", "details": str(e)}), 500

        # If transcription fails or the function returns None
        if not transcription_output_file:
            return jsonify({"error": "Transcription failed"}), 500

        # Connect to the MySQL database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insert into the transcription table
            cursor.execute('INSERT INTO transcription (user_id, filename, transcription_output_file) VALUES (%s, %s, %s)', 
                           (user_id, filename, transcription_output_file))
            audio_id = cursor.lastrowid
            conn.commit()
        except pymysql.MySQLError as e:
            return jsonify({"error": "Error saving transcription data to database", "details": str(e)}), 500
        finally:
            conn.close()

        # Read the transcription content
        transcription_content = ""
        try:
            with open(transcription_output_file, 'r') as f:
                transcription_content = f.read()
        except Exception as e:
            return jsonify({"error": "Error reading transcription file", "details": str(e)}), 500
        response = jsonify({
        "audio_id": audio_id,
        "filename": filename,
        "transcription_output_file": transcription_output_file,
        "transcription_content": transcription_content
        })
        response.status_code = 200
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

# ---------------------Route # 08------------------------

@app.route('/download_transcription/<int:audio_id>', methods=['GET'])
@jwt_required()  # Restricting access to users and admins
def download_transcription(audio_id):
    user_identity = get_jwt_identity()

    if not user_identity:
        return jsonify({"error": "Unauthorized access no identify"})
    # Assuming the token contains 'username' and 'user_id'
    user_id = user_identity.get('user_id')

    # Connect to the MySQL database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch the transcription file associated with the audio_id and user_id
        cursor.execute('SELECT transcription_output_file FROM transcription WHERE id = %s AND user_id = %s', 
                       (audio_id, user_id))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Transcription not found or access denied."}), 404
        
        transcription_file_path = result['transcription_output_file']  # Access using dictionary key
        
        # Check if the transcription file exists
        if not os.path.exists(transcription_file_path):
            return jsonify({"error": "Transcription file not found."}), 404

        # Serve the transcription file for download
        return send_file(transcription_file_path, as_attachment=True)
    
    except pymysql.MySQLError as e:
        return jsonify({"error": "Database error occurred."}), 500
    finally:
        conn.close()


@app.route('/chat', methods=['POST'])
def chat():
    # CORS preflight handling
    if request.method == 'OPTIONS':
        return '', 200

    # Get user input from POST request
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "Message is missing"}), 400

    try:
        # Call the Groq API with the user's input
        response_data = call_groq_api(user_input)
    except Exception as e:
        # Log the error for debugging and return a 500 response
        print(f"Error generating response: {e}")
        return jsonify({"error": str(e)}), 500

    # Return the Groq API response as JSON
    return jsonify(response_data)


@app.route('/summarize', methods=['POST'])
def summarize():
    # CORS preflight handling
    if request.method == 'OPTIONS':
        return '', 200

    # Get user input from POST request
    data = request.json
    user_input = data.get("text", "")  # Changed from "message" to "text"

    if not user_input:
        return jsonify({"error": "Text is missing"}), 400

    try:
        # Use the GROQ API for summarization
        summary = summarize_text(user_input)  # Call the summarize_text function
    except Exception as e:
        # Log the error for debugging and return a 500 response
        print(f"Error generating summary: {e}")
        return jsonify({"error": str(e)}), 500

    # Return the model-generated summary as JSON
    return jsonify({"summary": summary})
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


# 1. MVC structure completion
# 2. login with github + google
# 3. history fetching in profile page
# 4. working on professional frontend 