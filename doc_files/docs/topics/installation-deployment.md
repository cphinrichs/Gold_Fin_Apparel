---
description: Installing and deploying Gold Fin Apparel, including frontend, backend, and database configuration.
---

# Installation and Deployment Guide

Installing and deploying Gold Fin Apparel, including frontend, backend, and database configuration.

!!! note "Prerequisites"

    Ensure you have the following installed on your system:
    
    - Node.js and npm (for frontend development)
    - Python 3.9+ and pip (for backend development)
    - Access to an IBM Db2 for z/OS instance

## Frontend Setup

The frontend is a Vue.js-based single-page application built with Vite.

1. Navigate to the frontend directory.

    `cd frontend`

1. Install all required npm packages.

    `npm install`

    This command reads `package.json` and installs all dependencies including:

    - Vue.js 4.6.4
    - Vue Router 4.6.4
    - Vite 5.0.0
    - TypeScript 5.0.0

!!! note "Optional"

    Run the development server with hot-reload.

    `npm run dev`

    The development server typically runs on `http://localhost:5173`. You can access the application in your browser and see changes update in real-time.

1. Create an optimized production build.

    `npm run build`

## Backend Setup

The backend is a Flask REST API application that connects to IBM Db2 for z/OS.

1. Navigate to the backend directory.

    `cd backend`

1. Create an isolated Python virtual environment for the project.

    **Windows:**

    `python -m venv .venv`
    `.venv\Scripts\activate`

    After activation, your terminal prompt will show `(.venv)` at the beginning.

1. Install all required Python packages.

    `pip install -r requirements.txt`

    This installs:

    - Flask 3.1.3 — Web framework
    - ibm_db 3.2.8 — IBM Db2 Python driver
    - requests 2.32.5 — HTTP library
    - Additional supporting packages

1. Configure database credentials by creating or updating `backend/src/config/db_credentials.json`.

    ```JSON
        {
          "host": "<your_db2_hostname>",
          "port": "50000",
          "db_instance": "GOLDDB",
          "protocol": "TCPIP",
          "username": "<your_user>",
          "password": "<your_pass>"
        }
    ```

!!! warning "Security"

    Never commit `db_credentials.json` to version control. Add it to `.gitignore` and manage credentials securely in your deployment environment.

1. Configure backend settings by ensuring `backend/src/config/backend_settings.json` exists with appropriate application configuration.

    ```JSON
        {
          "debug": false,
          "host": "0.0.0.0",
          "port": 5000,
          "log_level": "INFO"
        }
    ```

    Adjust these settings based on your deployment environment.

1. Start the Flask API server.

    `python -m src.api`

    The API server typically starts on `http://localhost:5000`. You should see output indicating the server is running.

    !!! note "Running in Production"

        For production deployment, use a production WSGI server such as Gunicorn or uWSGI instead of Flask's development server:

        ```bash
            pip install gunicorn
            gunicorn -w 4 -b 0.0.0.0:5000 src.api:app
        ```
