# Employee Management API (Flask)

A production-ready REST API built with Flask, featuring secure JWT authentication, role-based access control, Marshmallow validation, SQLAlchemy ORM, and full CRUD operations for employees. Deployed on Render with a clean, modular project architecture.

---

## 🚀 Features

### 🔐 Authentication
- JWT-based login  
- Password hashing  
- Token validation middleware  
- Secure auth decorator

### 👮 Role-Based Access Control
- Two roles: **admin** and **user**
- Admin can create/update/delete employees
- Users can only view employees

### 📦 Employee Management
- Add employee  
- Update employee  
- Delete employee  
- View all employees  
- Email + salary fields  
- Marshmallow schema validation  
- Unique email constraint

### 🗄 Database Layer
- SQLite (local development)
- SQLAlchemy ORM
- Flask-Migrate / Alembic migrations
- Easy switch to PostgreSQL for production

### 📁 Clean Project Structure
project/
│── models/
│── routers/
│── utils/
│── templates/
│── init.py
│── config.py
run.py


---

## 🌐 Live API (Render Deployment)

**Base URL:**  
https://employee-management-flask-1.onrender.com

---

## 🔑 Authentication Endpoints

### 👉 Register
POST /register
{
"username": "john",
"password": "pass123"
}



### 👉 Login (returns token)
POST /login
{
"username": "john",
"password": "pass123"
}



**Response**
```json
{
  "token": "JWT_TOKEN_HERE"
}
Auth Header for All Protected Routes

Authorization: Bearer <token>
👮 Admin-Only Endpoints
➕ Create Employee
bash
Copy code
POST /employees
Authorization: Bearer <ADMIN_TOKEN>

{
  "name": "Arjun",
  "age": 28,
  "email": "arjun@example.com",
  "department": "Engineering",
  "salary": 50000
}
✏️ Update Employee

PATCH /employees/<id>
Authorization: Bearer <ADMIN_TOKEN>
❌ Delete Employee

DELETE /employees/<id>
Authorization: Bearer <ADMIN_TOKEN>
👀 User/Public Endpoints
📄 Get All Employees

GET /employees
🛠 Tech Stack
Python 3

Flask

Flask-JWT / PyJWT

SQLAlchemy ORM

Marshmallow

Alembic (Flask-Migrate)

Gunicorn

Render Deployment

🧪 Running Locally
1️⃣ Clone Repo

git clone https://github.com/Abhishek4manu/employee-management-flask
cd employee-management-flask
2️⃣ Create Virtual Environment

python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies

pip install -r requirements.txt
4️⃣ Create .env

SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
FLASK_ENV=development
5️⃣ Run Migrations

flask db upgrade
6️⃣ Start Server

python run.py
🚀 Deployment Notes
Uses Gunicorn as production server

Works out of the box on Render

Auto-build via requirements.txt

📌 Future Improvements
Switch to PostgreSQL for production

Add Swagger documentation

Add pagination

Add unit tests

Implement refresh tokens

Add CI/CD pipeline

👤 Author
Abhishek Manu
Backend Developer — Python/Flask
GitHub: https://github.com/Abhishek4manu
