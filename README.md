## Python
### Version: 3.10.12


## Technology Used 
- Django (Backend/Migration)
- PostgreSQL (Database)


## What you will find
- Django(backend/migration)
- Database(postgresql)
- swagger
- env
- Login with email
- JWT (access and refresh)
- Standard Error Response and Success Response
- AWS S3 for (upload file, videos , get file url)
- Email Services
- APIs (Register, Login, ...)


## Env setup
- Setup Project Env 
    1. Create .env at root directory of the project and copy it
```bash
        DEBUG=
        TEST_MODE=

        # Keys
        SECRET_KEY=
        JWT_SIGNING_KEY=
        SALT_KEY=

        # Database
        POSTGRES_DB=
        POSTGRES_USER=
        POSTGRES_PASSWORD=
        POSTGRES_HOST=
        POSTGRES_PORT=

        # Email
        EMAIL_HOST_USER=
        EMAIL_HOST_PASSWORD= 

        # Open AI
        OPENAI_API_KEY=

        # AWS
        AWS_STORAGE_BUCKET_NAME=
        AWS_S3_ACCESS_KEY_ID= 
        AWS_S3_SECRET_ACCESS_KEY= 
        AWS_S3_REGION_NAME= 
```
and for their values contact to your `Leads` or `Project Manger` 


## Installation and Execution
- Through Docker
    1. Make sure you have Docker Installed on your system
    2. Clone the repository 
    3. setup local env file `.env` to the root directory
    4. Open the terminal and run the command 
        ```bash 
         docker-compose -f .\docker-compose.main.yml up
        ```
        
- To verify project is running \
    `http://localhost:8033/swagger/`

- Alternative Way
    1. Clone the repository 
    2. setup local env file `.env` to the root directory
    3. Open the terminal:

        1. Create virtual environment 
        ```bash 
        python -m venv .venv 
        ```
        2. Activate virtual environment 
        ```bash 
        source .venv/bin/activate
        ```
        3. Install requirements 
        ```bash 
        pip install -r requirements.txt
        ```
        4. Run server 
        ```bash 
        python manage.py runserver
        ```
        
- To verify project is running \
    `http://localhost:8000/swagger/`
    

## Swagger UI

- After running the project visit the following url to view swagger ui.
    1. Docker \
    `http://localhost:8033/swagger/`

    2. Alternate way \
    `http://localhost:8000/swagger/`


 ## Migration 

- Generate migrations :
```bash 
     python manage.py makemigrations
```
    
- Apply migrations :
```bash 
     python manage.py migrate
```
