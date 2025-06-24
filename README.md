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

## Installation & Usage

You can choose to run the application locally using Conda or deploy it via Docker containerization.

### 1. Local Dev (using Conda)

This method is suitable for development and debugging.

1.  **Clone repository**
    ```bash
    git clone https://github.com/routerhan/statin.git
    cd statin
    ```
2.  **Using `environment.yml` to create Conda venv**
    ```bash
    conda env create -f environment.yml
    ```
3.  **Activate venv**
    ```bash
    conda activate statin-env
    ```
4.  **Run Flask app**
    ```bash
    python app.py
    ```
5.  **Visit application**
    Open in your browser: `http://127.0.0.1:8080`.

### 2. Containerization (using Docker)

This method is suitable for simulating a production environment or for rapid deployment.

1.  **Ensure Docker installed and running**
2.  **Under the project directory，Build Docker image**
    ```bash
    docker build -t statin-safety-tool .
    ```
3.  **Run Docker container**
    ```bash
    docker run -p 8080:8080 statin-safety-tool
    ```
4.  **Visit application**
    Open in your browser: `http://localhost:8080`.

## Project Structure

```
.
├── app.py                  # Flask main application
├── statin_logic.py         # Core logic code
├── templates/              # HTML templates
├── static/                 # Static files (img, CSS, JS)
├── Dockerfile              # Docker containerization configuration
├── environment.yml         # Conda local env definition
├── requirements.txt        # Pip container env dependencies
└── README.md               # Documentation
```

## ©️ Copyright and Version

-   **Own by**: National Cheng Kung University Department of Engineering Science
-   **Version**: v1.0.0