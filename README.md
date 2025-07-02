# Statin Safety Management Tool (Web Version)

This is a web-based clinical decision support tool designed to assist physicians in quickly assessing the safety of statin medication use based on patient clinical data (Creatine Kinase CK, Transaminase ALT/AST, Total Bilirubin) and muscle symptoms, providing corresponding treatment recommendations.

This project migrates the original Tkinter desktop application to a web platform, offering improved accessibility and a smoother user experience.

## Features

-   **Web Interface**: No installation required; accessible directly via a web browser.
-   **Real-time Response**: Obtain diagnostic recommendations instantly without page reloads after data input (utilizing AJAX technology).
-   **Input Validation**: Dual front-end and back-end validation ensures the validity of input data (e.g., values cannot be negative).
-   **Concise Design**: Intuitive and easy-to-operate user interface.
-   **Containerization**: Dockerized for easy deployment and consistent environments.

## Technology Stack

-   **Backend**: Python 3.12, Flask
-   **Frontend**: HTML, CSS, JavaScript
-   **Containerization**: Docker
-   **Local Development Environment**: Conda

## 1. Prerequisites

Before you begin, ensure you have the following tools installed and configured:
-   [Google Cloud SDK (`gcloud`)](https://cloud.google.com/sdk/docs/install)
-   Docker
-   Conda

## 2. Cloud Environment Setup (GCP)

These steps only need to be performed once when setting up a new GCP project.

### Step 2.1: Login and Initialize gcloud
```bash
# Login to your Google account
gcloud auth login

# Set your project ID (replace 'statin-project' if different)
gcloud config set project statin-project
```

### Step 2.2: Enable Required APIs
```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  sqladmin.googleapis.com \
  secretmanager.googleapis.com
```

### Step 2.3: Create Cloud SQL (PostgreSQL) Instance
```bash
# Choose a strong password for the 'postgres' user
DB_ROOT_PASSWORD="YOUR_STRONG_ROOT_PASSWORD"

gcloud sql instances create statin-db \
  --database-version=POSTGRES_14 \
  --region=asia-east1 \
  --root-password="$DB_ROOT_PASSWORD"
```

### Step 2.4: Create Database and Application User
It's best practice to create a dedicated user for your application.
```bash
# Create the application database
gcloud sql databases create statin_tool_db --instance=statin-db

# Create a dedicated user for the application
gcloud sql users create statin-db-admin --instance=statin-db --password="YOUR_APP_USER_PASSWORD"
```

### Step 2.5: Store Credentials in Secret Manager
Never hardcode secrets. Store them securely.
```bash
# Store DB username
echo -n "statin-db-admin" | gcloud secrets create DB_USER --data-file=-

# Store DB password (use the password from step 2.4)
echo -n "YOUR_APP_USER_PASSWORD" | gcloud secrets create DB_PASS --data-file=-

# Store DB name
echo -n "statin_tool_db" | gcloud secrets create DB_NAME --data-file=-

# Store a random secret key for Flask sessions
python -c 'import secrets; print(secrets.token_hex(16))' | gcloud secrets create FLASK_SECRET_KEY --data-file=-
```

### Step 2.6: Create Artifact Registry Repository
This is where your Docker images will be stored.
```bash
gcloud artifacts repositories create statin-repo \
  --repository-format=docker \
  --location=asia-east1 \
  --description="Repository for Statin Safety Tool images"
```

## 3. Local Development Setup

Follow these steps to run the application on your local machine for development, connected to the Cloud SQL database.

### Step 3.1: Clone Repository and Setup Environment
```bash
git clone https://github.com/routerhan/statin.git
cd statin
conda env create -f environment.yml
conda activate statin-env
```

### Step 3.2: Configure Local Environment File
Create a `.env` file from the example. This file is ignored by Git.
```bash
cp .env.example .env
```
Now, edit the `.env` file and uncomment/fill in the variables for connecting to GCP. It should look like this:
```ini
# .env
GCP_PROJECT="statin-project"
INSTANCE_CONNECTION_NAME="statin-project:asia-east1:statin-db"
GRPC_ENABLE_FORK_SUPPORT=1
```

### Step 3.3: Run Cloud SQL Auth Proxy
Open a **new, separate terminal window** and run the following command. Keep this terminal open during your entire development session.
```bash
# Authenticate gcloud for application default credentials
gcloud auth application-default login

# Start the proxy
cloud-sql-proxy statin-project:asia-east1:statin-db
```

### Step 3.4: Run Database Migrations
Go back to your **original terminal**. This step creates the necessary tables in your Cloud SQL database.
```bash
# Generate the initial migration script (only needed if models.py changes)
flask db migrate -m "Initial migration"

# Apply the changes to the database
flask db upgrade
```

### Step 3.5: Create an Initial Physician User
Use the built-in CLI command to create a user you can log in with.
```bash
flask create-user dr_chen "Dr. Chen" "YOUR_CHOSEN_PASSWORD"
```

### Step 3.6: Run the Flask App
```bash
flask run
```
You can now access the application at `http://127.0.0.1:5000`.

## 4. Cloud Deployment to Cloud Run

### Step 4.1: Build and Push Docker Image
This command builds your Docker image using Cloud Build and pushes it to Artifact Registry.
```bash
gcloud builds submit --tag asia-east1-docker.pkg.dev/statin-project/statin-repo/statin-safety-tool:v2.0.0
```

### Step 4.2: Deploy to Cloud Run
This command deploys the container and correctly links it to the Cloud SQL instance.
```bash
gcloud run deploy statin-safety-tool \
  --image asia-east1-docker.pkg.dev/statin-project/statin-repo/statin-safety-tool:v2.0.0 \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --add-cloudsql-instances "statin-project:asia-east1:statin-db" \
  --set-env-vars "GCP_PROJECT=statin-project" \
  --set-env-vars "INSTANCE_CONNECTION_NAME=statin-project:asia-east1:statin-db"
```

### Step 4.3: Grant IAM Permissions (Crucial!)
The Cloud Run service needs permission to access Secret Manager and Cloud SQL.
```bash
# Find your Cloud Run service account email with this command
# It looks like: service-PROJECT_NUMBER@gcp-sa-run.iam.gserviceaccount.com
gcloud run services describe statin-safety-tool --platform managed --region asia-east1

# Grant Secret Manager access
gcloud projects add-iam-policy-binding statin-project \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor"

# Grant Cloud SQL access
gcloud projects add-iam-policy-binding statin-project \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/cloudsql.client"
```

After these steps, your application will be live at the URL provided by the `gcloud run deploy` command.

## Project Structure

```
.
├── app.py                  # Flask main application
├── models.py               # SQLAlchemy database models
├── statin_logic.py         # Core logic code
├── migrations/             # Flask-Migrate database migration scripts
├── templates/              # HTML templates
├── static/                 # Static files (img, CSS, JS)
├── Dockerfile              # Docker containerization configuration
├── environment.yml         # Conda local env definition
├── requirements.txt        # Pip container env dependencies
└── README.md               # Documentation
```

## ©️ Copyright and Version

-   **Own by**: National Cheng Kung University Department of Engineering Science
-   **Version**: v2.0.0