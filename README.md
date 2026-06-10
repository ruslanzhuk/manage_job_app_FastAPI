# Job Marketplace API
Backend application developed as a university project over a two-month period.

The project is a job marketplace platform inspired by services such as OLX, where users can publish job offers, search for work opportunities, submit applications, leave reviews, and interact through a REST API.

The application was built using FastAPI and follows Clean Architecture principles to separate business logic, infrastructure, and API layers.

## ✨ Features
- 👤 User registration and authentication
- 💼 Job offer creation and management
- 📨 Job applications
- ⭐ Review system
- 🚩 Reporting functionality
- 🌍 Continents, countries, and cities management
- 📂 Job categories
- 🛡️ Admin operations
- 📖 Interactive Swagger documentation

## 🏗️ Architecture

The project follows the Clean Architecture approach, separating business logic from infrastructure and external dependencies.

### Layers

🔹 API Layer

- FastAPI routers
- Request/response handling
- Endpoint definitions

🔹 Domain Layer

- Core business entities
- Repository interfaces (contracts)
- Business rules

🔹 Infrastructure Layer

- Database repositories
- DTOs
- Service implementations
- Authentication and utility components

This separation improves maintainability, testability, and scalability.

### Project Structure
```
.
├── docker-compose.debug.yml
├── docker-compose.yml
├── Dockerfile
├── init.sql
├── manage_job_app
│   ├── api
│   │   ├── __init__.py
│   │   └── routers
│   │       ├── admin.py
│   │       ├── application.py
│   │       ├── city.py
│   │       ├── continent.py
│   │       ├── country.py
│   │       ├── __init__.py
│   │       ├── job_category.py
│   │       ├── offer.py
│   │       ├── report.py
│   │       ├── review.py
│   │       └── user.py
│   ├── config.py
│   ├── container.py
│   ├── core
│   │   ├── domain
│   │   │   ├── admin.py
│   │   │   ├── application.py
│   │   │   ├── __init__.py
│   │   │   ├── job_category.py
│   │   │   ├── location.py
│   │   │   ├── offer.py
│   │   │   ├── report.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   └── repositories
│   │       ├── iadmin.py
│   │       ├── iapplication.py
│   │       ├── icity.py
│   │       ├── icontinent.py
│   │       ├── icountry.py
│   │       ├── ijob_category.py
│   │       ├── __init__.py
│   │       ├── ioffer.py
│   │       ├── ireport.py
│   │       ├── ireview.py
│   │       └── iuser.py
│   ├── db.py
│   ├── infrastructure
│   │   ├── dto
│   │   │   ├── admindto.py
│   │   │   ├── applicationdto.py
│   │   │   ├── __init__.py
│   │   │   ├── job_categorydto.py
│   │   │   ├── locationdto.py
│   │   │   ├── offerdto.py
│   │   │   ├── reportdto.py
│   │   │   ├── reviewdto.py
│   │   │   ├── tokendto.py
│   │   │   └── userdto.py
│   │   ├── __init__.py
│   │   ├── repositories
│   │   │   ├── admindb.py
│   │   │   ├── applicationdb.py
│   │   │   ├── citydb.py
│   │   │   ├── continentdb.py
│   │   │   ├── countrydb.py
│   │   │   ├── __init__.py
│   │   │   ├── job_categorydb.py
│   │   │   ├── offerdb.py
│   │   │   ├── reportdb.py
│   │   │   ├── reviewdb.py
│   │   │   └── userdb.py
│   │   ├── services
│   │   │   ├── admin.py
│   │   │   ├── application.py
│   │   │   ├── city.py
│   │   │   ├── continent.py
│   │   │   ├── country.py
│   │   │   ├── iadmin.py
│   │   │   ├── iapplication.py
│   │   │   ├── icity.py
│   │   │   ├── icontinent.py
│   │   │   ├── icountry.py
│   │   │   ├── ijob_category.py
│   │   │   ├── __init__.py
│   │   │   ├── ioffer.py
│   │   │   ├── ireport.py
│   │   │   ├── ireview.py
│   │   │   ├── iuser.py
│   │   │   ├── job_category.py
│   │   │   ├── offer.py
│   │   │   ├── report.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   └── utils
│   │       ├── consts.py
│   │       ├── __init__.py
│   │       ├── password.py
│   │       └── token.py
│   ├── __init__.py
│   └── main.py
├── requirements-dev.txt
└── requirements.txt
```

## 🛠️ Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker

## 🚀 Running with Docker

1. Clone repository
```
git clone https://github.com/your-username/manage_job_app_FastAPI.git 
cd manage_job_app_FastAPI
```

2. Create an environment file
Copy the example configuration:
```
cp .env.example .env
```

The default values can be used for local development. If necessary, update the database credentials inside the .env file.

3. Build and start the application
```
docker compose up --build
```
Docker Compose will:

- Build the FastAPI application container
- Start a PostgreSQL database container
- Initialize the database using init.sql
- Connect the application to the database automatically

4. Access the application
API:
```
http://localhost:8000
```
Swagger UI:
``` 
http://localhost:8000/docs
```
5. Stop the application
```
docker compose down
```

## 📌 Notes

This project was developed as part of a university backend development course and is included in this repository for portfolio purposes.

The focus of the project was on backend architecture, REST API design, database integration, and applying Clean Architecture principles in practice.