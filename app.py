import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from statin_logic import get_statin_recommendation # Import the refactored logic
from models import db, User, Evaluation
from flask_migrate import Migrate
from google.cloud import secretmanager
from dotenv import load_dotenv
import click

load_dotenv()  # Load environment variables from .env file for local development

# Initialize Flask app
app = Flask(__name__)

# Define app constants for easy updates
APP_VERSION = "v2.0.0"
COPYRIGHT_HOLDER = "National Cheng Kung University Department of Engineering Science"

def get_secret(secret_id, project_id, version_id="latest"):
    """Fetches a secret from Google Cloud Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# --- GCP Configuration ---
project_id = os.environ.get('GCP_PROJECT')
if project_id:
    db_user = get_secret("DB_USER", project_id)
    db_pass = get_secret("DB_PASS", project_id)
    db_name = get_secret("DB_NAME", project_id)
    instance_connection_name = os.environ.get('INSTANCE_CONNECTION_NAME') # e.g. project:region:instance
    app.config['SECRET_KEY'] = get_secret("FLASK_SECRET_KEY", project_id)
    
    # Cloud SQL (PostgreSQL) connection string
    db_uri = f"postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host=/cloudsql/{instance_connection_name}"
else:
    # Local development fallback (using SQLite for simplicity)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    db_uri = "sqlite:///statin_tool.db"

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- Flask-Migrate Setup ---
migrate = Migrate(app, db)

# --- Login Manager Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to /login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    if session.get('is_guest'):
        guest = UserMixin()
        guest.id = 0
        guest.is_guest = True
        return guest
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            session['is_guest'] = False
            return redirect(url_for('tool'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/guest_login')
def guest_login():
    guest = UserMixin()
    guest.id = 0 # Guest user has ID 0
    guest.is_guest = True
    login_user(guest)
    session['is_guest'] = True
    return redirect(url_for('tool'))

@app.route('/tool')
@login_required
def tool():
    """Renders the main tool page."""
    return render_template('tool.html', version=APP_VERSION, copyright=COPYRIGHT_HOLDER)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/evaluate', methods=['POST'])
@login_required
def evaluate():
    try:
        data = request.get_json()
        ck_value = float(data['ck_value'])
        transaminase = float(data['transaminase'])
        bilirubin = float(data['bilirubin'])
        muscle_symptoms = bool(data['muscle_symptoms'])

        recommendation = get_statin_recommendation(ck_value, transaminase, bilirubin, muscle_symptoms)
        
        # Save to DB if it's a logged-in physician
        if current_user.is_authenticated and not session.get('is_guest'):
            new_eval = Evaluation(
                user_id=current_user.id, ck_value=ck_value, transaminase=transaminase,
                bilirubin=bilirubin, muscle_symptoms=muscle_symptoms, recommendation=recommendation
            )
            db.session.add(new_eval)
            db.session.commit()
        return jsonify({'success': True, 'recommendation': recommendation})
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': "Invalid input format. Please ensure all values are numbers."}), 400
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({'success': False, 'error': "An unexpected error occurred."}), 500

# --- CLI Commands ---
@app.cli.command("create-user")
@click.argument("username")
@click.argument("full_name")
@click.argument("password")
def create_user(username, full_name, password):
    """Creates a new user account for a physician."""
    if User.query.filter_by(username=username).first():
        print(f"Error: User '{username}' already exists.")
        return
    new_user = User(username=username, full_name=full_name)
    new_user.set_password(password) # This will hash the password
    db.session.add(new_user)
    db.session.commit()
    print(f"User '{username}' created successfully.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))