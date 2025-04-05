# 📄 Document Management API

A **FastAPI-based application** for managing document uploads, OCR processing, Google OAuth authentication, and role-based access control. This project integrates **MinIO** for file storage, **Celery** for asynchronous OCR tasks, and **PostgreSQL/SQLite** for persistent data storage.

---

## 📚 Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Running the Application](#running-the-application)  
- [API Endpoints](#api-endpoints)  
- [Contributing](#contributing)  
- [License](#license)  
- [Notes](#notes)  

---

## ✅ Features

- **User Authentication:** Google OAuth 2.0 login/logout with JWT-based session management.
- **Role-Based Access:** Supports roles like `manager` and `account` for document control.
- **Document Management:** Upload, retrieve, search, and delete documents using MinIO.
- **OCR Processing:** Asynchronous text extraction from images using Tesseract and Celery.
- **Logging:** Tracks user actions such as uploads and deletions.
- **Search Functionality:** Full-text search on OCR-extracted content for authorized users.

---

## 🧰 Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite (configurable for PostgreSQL)
- **File Storage:** MinIO
- **Task Queue:** Celery with RabbitMQ
- **OCR Engine:** Tesseract OCR (`pytesseract`)
- **Authentication:** Google OAuth 2.0 with `authlib`
- **ORM:** SQLAlchemy
- **NLP (Optional):** SpaCy (for future text processing)

---

## ⚙️ Prerequisites

- Python 3.9+
- Docker (optional; for MinIO and RabbitMQ)
- RabbitMQ
- MinIO
- Tesseract OCR (installed and available in PATH)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/document-management-api.git
cd document-management-api
2. Set Up a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Create a requirements.txt with packages like fastapi, sqlalchemy, pytesseract, celery, minio, authlib, python-jose, python-dotenv, spacy, etc.

4. Install Tesseract OCR
Ubuntu:

bash
Copy
Edit
sudo apt install tesseract-ocr
macOS:

bash
Copy
Edit
brew install tesseract
Windows:
Install from the official Tesseract website and add to your system PATH.

5. Download SpaCy Model
bash
Copy
Edit
python -m spacy download en_core_web_sm
🔧 Configuration
Create a .env file in the project root with the following:

env
Copy
Edit
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
URL=sqlite:////path/to/your/database.db  # Or use PostgreSQL
MinIO Setup (via Docker)
bash
Copy
Edit
docker run -p 9000:9000 --name minio \
-e "MINIO_ROOT_USER=minioadmin" \
-e "MINIO_ROOT_PASSWORD=minioadmin" \
minio/minio server /data
Update minio_upload.py if you're using different credentials or endpoint.

RabbitMQ Setup (via Docker)
bash
Copy
Edit
docker run -d -p 5672:5672 rabbitmq:3
🏃 Running the Application
1. Start the FastAPI Server
bash
Copy
Edit
uvicorn main:app --reload --host 127.0.0.1 --port 8000
2. Start the Celery Worker
Open another terminal and run:

bash
Copy
Edit
celery -A celery worker --loglevel=info
3. Access the API
Visit: http://127.0.0.1:8000/docs for Swagger UI

📡 API Endpoints
🔐 Authentication
Method	Endpoint	Description
GET	/login	Redirect to Google OAuth
GET	/auth	Handle OAuth callback
GET	/logout	Logout and clear session
📁 Document Management
Method	Endpoint	Description
POST	/Uplode_Document/	Upload a document (requires account or manager)
GET	/get_files	Retrieve documents (filtered by role)
GET	/searech_file/	Full-text search on OCR text
DELETE	/Delete_Document/	Delete a document (manager only)
👥 User Management
Method	Endpoint	Description
GET	/Get_ALL_USER_DATA	Fetch all user data (admin/manager access)
PUT	/give_role/	Assign a role to a user
🤝 Contributing
Fork the repository.

Create a feature branch:

bash
Copy
Edit
git checkout -b feature/your-feature
Commit your changes:

bash
Copy
Edit
git commit -m "Add your feature"
Push to the branch:

bash
Copy
Edit
git push origin feature/your-feature
Open a pull request.

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

📝 Notes
Replace yourusername in the clone URL with your actual GitHub username.

Ensure requirements.txt includes all necessary packages.

Adjust database path in .env based on your system.

For PostgreSQL, make sure the database is created and accessible.

Built with ❤️ using FastAPI, Celery, MinIO, and OCR tech.
