# College Management API (FastAPI + PostgreSQL + Docker)

A backend API project for managing **Students and Departments** using **FastAPI, PostgreSQL, SQLAlchemy ORM, and Docker**.

This project demonstrates:
- API development using FastAPI for performing CRUD operations on a PostgreSQL database
- Database design using PostgreSQL
- ORM operations using SQLAlchemy
- Input validation using Pydantic
- Containerization using Docker
- Environment variable security using `.env`

---

# Project Structure

```
college management/
│
├── database/
│   └── college_management.py
│
├── schema/
│   └── user_input.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
└── README.md
```

---

# 1. Database Folder

Inside the **database** folder there is a file:

```
college_management.py
```

This file performs all **CRUD operations** using **SQLAlchemy ORM**.

### Key Features

- `load_dotenv()` is used to load the **DATABASE_URL** from `.env`
- SQLAlchemy **engine** is created
- Two tables are created using ORM classes:

### Tables

#### Departments Table
Class: `Department`

Columns:
- `dept_id` (Primary Key)
- `dept_name`

#### Students Table
Class: `Student`

Columns:
- `st_id` (Primary Key)
- `st_name`
- `age`
- `email`
- `city`
- `dept_id` (Foreign Key)

Both tables are connected using **Foreign Key relationship**.

### Functions Implemented

- `view_all_data()`  
  View all student data.

- `sorted_data()`  
  Return students sorted by a specific field.

- `view_a_student()`  
  View details of a specific student.

- `get_st_value()`  
  Finds the highest student ID in each department.

- `add_data()`  
  Add a new student record.

- `update_student()`  
  Update student details based on:
  - st_name
  - age
  - city
  - dept_name

- `delete_data()`  
  Delete a student using **student ID**.

---

# 2. Schema Folder

Inside **schema** folder:

```
user_input.py
```

This file uses **Pydantic** for input validation.

### Automatic Student ID Generation

```
_dept_counter : ClassVar[dict[int,int]] = get_st_value()
```

This ensures:

- `st_id` automatically increases
- Prevents **Primary Key violation**
- User does not need to manually manage IDs

Users only provide required fields through the API.

---

# 3. .dockerignore

This file prevents unnecessary files from being copied into the Docker image.

Ignored files include:

```
.env
env/
venv/
**/__pycache__/
.git
.gitignore
.vscode/
.idea/
*.pyc
*.db
*.sqlite3
```

This helps:
- Reduce Docker image size
- Improve build speed
- Protect sensitive information

---

# 4. .env.example

This file provides **example environment variables** for other developers.

Example:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=college

DATABASE_URL=postgresql+psycopg2://postgres:password@db:5432/college
```

Developers should rename it to:

```
.env
```

and update the values.

---

# 5. .gitignore

Prevents sensitive or unnecessary files from being uploaded to GitHub.

Ignored files include:

```
.env
__pycache__/
*.pyc
venv/
env/
```

---

# 6. FastAPI Application

Main API logic is implemented in:

```
app.py
```

### API Endpoints

Home Route

```
GET /
```

About API

```
GET /about
```

Add Student

```
POST /add_details
```

View All Students

```
GET /students
```

Sorted Students

```
GET /students/sort
```

View Single Student

```
GET /students/{st_id}
```

Update Student

```
PATCH /edit_student/{st_id}
```

Delete Student

```
DELETE /delete/{st_id}
```

---

# 7. Dockerfile

Used to build the **Docker image** for the FastAPI application.

It includes:
- Python base image
- Copying project files
- Installing dependencies
- Running FastAPI with Uvicorn

---

# 8. docker-compose.yml

This file creates and runs two containers:

### 1️⃣ FastAPI Container
Runs the backend API.

### 2️⃣ PostgreSQL Container
Runs the database.

Docker Compose automatically connects both containers using environment variables.

---

# 9. requirements.txt

Contains all Python dependencies required for the project.

Example:

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
pydantic
```

Install using:

```
pip install -r requirements.txt
```

---

# Running the Project

## Method 1 — Run Using VS Code (Without Docker)

### Step 1

Rename:

```
.env.example
```

to

```
.env
```

### Step 2

Update database credentials:

```
POSTGRES_PASSWORD
POSTGRES_DB
```

### Step 3

Update `DATABASE_URL`

Replace:
- password
- db_name

Example:

```
postgresql+psycopg2://postgres:yourpassword@localhost:5432/college
```

### Step 4

Install requirements

```
pip install -r requirements.txt
```

### Step 5

Run FastAPI server

```
uvicorn app:app --reload
```

### Step 6

Open browser:

```
http://localhost:8000/docs
```

---

# Method 2 — Run Using Docker

### Step 1

Rename:

```
.env.example
```

to

```
.env
```

### Step 2

Update:

```
POSTGRES_PASSWORD
POSTGRES_DB
DATABASE_URL
```

### Step 3

Build and start containers

For **latest Docker version**

```
docker compose up --build
```

For **older Docker version**

```
docker-compose up --build
```

### Step 4

Open browser

```
http://localhost:8000/docs
```

Make sure **Docker Desktop is running**.

---

# Features of This Project

- FastAPI REST API
- PostgreSQL Database
- SQLAlchemy ORM
- Pydantic Validation
- Dockerized Application
- Environment Variable Security
- Persistent Database using Docker Volumes

---

# Author

**Akhilesh Kumar**

B.Tech CSE Student  
Interested in **Cybersecurity, Software Development, and Machine Learning and Mainly in AI Engineer and taking steps toward AI Engineer**