Document Management API
A FastAPI-based application for managing document uploads, OCR processing, user authentication with Google OAuth, and role-based access control. This project integrates MinIO for file storage, Celery for asynchronous OCR tasks, and PostgreSQL/SQLite for data persistence.

Table of Contents
Features
User Authentication: Google OAuth 2.0 login/logout with JWT-based session management.
Role-Based Access: Supports roles like manager and account for document access control.
Document Management: Upload, retrieve, search, and delete documents with MinIO storage.
OCR Processing: Asynchronous text extraction from images using Tesseract and Celery.
Logging: Tracks user activities (e.g., uploads, deletions) in the database.
Search Functionality: Full-text search on OCR-extracted text for authorized users.
Tech Stack
Backend: FastAPI (Python)
Database: SQLite (configurable for PostgreSQL)
File Storage: MinIO
Task Queue: Celery with RabbitMQ
OCR: Tesseract (via pytesseract)
Authentication: Google OAuth 2.0 with authlib
ORM: SQLAlchemy
NLP: SpaCy (for potential text processing)
Prerequisites
Python 3.9+
Docker (optional, for MinIO and RabbitMQ)
RabbitMQ (message broker for Celery)
MinIO (object storage)
Tesseract OCR installed (pytesseract dependency)
Installation
Clone the Repository
bash

Collapse

Wrap

Copy
git clone https://github.com/yourusername/document-management-api.git
cd document-management-api
Set Up a Virtual Environment
bash

Collapse

Wrap

Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies
bash

Collapse

Wrap

Copy
pip install -r requirements.txt
Note: Create a requirements.txt with dependencies like fastapi, sqlalchemy, pytesseract, celery, minio, authlib, python-jose, python-dotenv, spacy, etc.
Install Tesseract OCR
On Ubuntu: sudo apt install tesseract-ocr
On macOS: brew install tesseract
On Windows: Install via installer and add to PATH.
Download SpaCy Model
bash

Collapse

Wrap

Copy
python -m spacy download en_core_web_sm
Configuration
Environment Variables Create a .env file in the root directory with the following:
plaintext

Collapse

Wrap

Copy
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
URL=sqlite:////path/to/your/database.db  # Or PostgreSQL URL
MinIO Setup Run MinIO locally or via Docker:
bash

Collapse

Wrap

Copy
docker run -p 9000:9000 --name minio -e "MINIO_ROOT_USER=minioadmin" -e "MINIO_ROOT_PASSWORD=minioadmin" minio/minio server /data
Update minio_upload.py if using a different endpoint or credentials.
RabbitMQ Setup Run RabbitMQ via Docker:
bash

Collapse

Wrap

Copy
docker run -d -p 5672:5672 rabbitmq:3
Running the Application
Start the FastAPI Server
bash

Collapse

Wrap

Copy
uvicorn main:app --reload --host 127.0.0.1 --port 8000
Start the Celery Worker In a separate terminal:
bash

Collapse

Wrap

Copy
celery -A celery worker --loglevel=info
Access the API Open your browser to http://127.0.0.1:8000/docs for the interactive Swagger UI.
API Endpoints
Authentication
GET /login: Redirects to Google OAuth login.
GET /auth: Handles OAuth callback and sets access token.
GET /logout: Clears session and logs out the user.
Document Management
POST /Uplode_Document/: Upload a document (requires account or manager role).
GET /get_files: Retrieve documents (filtered by role).
GET /searech_file/: Search OCR text in documents (role-based).
DELETE /Delete_Document/: Delete a document (requires manager role).
User Management
GET /Get_ALL_USER_DATA: Fetch all Google user data (admin/manager access).
PUT /give_role/: Assign a role to a user (e.g., manager, account).
Contributing
Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.
License
This project is licensed under the MIT License - see the  file for details.

Notes
Replace yourusername in the clone URL with your actual GitHub username.
Add a requirements.txt file with all dependencies if not already present.
Adjust paths (e.g., SQLite database location) based on your setup.
If you use PostgreSQL instead of SQLite, update the URL in .env and ensure the database is created.
