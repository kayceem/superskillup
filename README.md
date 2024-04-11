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

## ER Diagram

- Url: [`SuperSkillUp ER Diagram`](https://dbdocs.io/mohan939fde5586/superskillup?view=relationships)
- Password: ```superskillup@ramailo.tech0001```

## Directory Tree
```
superskillup
├─ .circleci
│  └─ config.yml
|
├─ .gitignore
|
├─ docker-compose.main.yml
|
├─ Dockerfile
|
├─ entrypoint.sh
|
├─ Makefile
|
├─ manage.py
|
├─ README.md
|
├─ requirements.txt
|
├─ superskillup
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
|  └─ wsgi.py
|
└─ app
   ├─ __init__.py
   ├─ admin.py
   ├─ apps.py
   ├─ models.py
   ├─ urls.py
   |
   ├─ api
   │  ├─ __init__.py
   │  ├─ api.py
   │  └─ response_builder.py
   |
   ├─ app_admin
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ app_admin.py
   │  ├─ serializers.py
   │  ├─ swagger.py
   │  └─ views.py
   |
   ├─ assignment
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ assignment.py
   │  ├─ serializers.py
   │  └─ views.py
   |
   ├─ course
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ course.py
   │  ├─ serializers.py
   │  └─ views.py
   |
   ├─ gpt_review
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ admin_views.py
   │  ├─ gpt_review.py
   │  ├─ open_ai.py
   │  ├─ serializer.py
   │  └─ user_views.py
   |
   ├─ manager_feedback
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ manager_feedback.py
   │  ├─ serializer.py
   │  └─ views.py
   |
   ├─ migrations
   │  ├─ 0001_initial.py
   │  └─ __init__.py
   |
   ├─ question
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ question.py
   │  ├─ serializer.py
   │  └─ views.py
   |
   ├─ question_answer
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ admin_views.py
   │  ├─ question_answer.py
   │  ├─ serializer.py
   │  └─ user_views.py
   |
   ├─ services
   │  ├─ __init__.py
   │  └─ email_service.py
   |
   ├─ shared
   │  ├─ __init__.py
   │  ├─ authentication.py
   │  └─ pagination.py
   |
   ├─ sub_topic
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ serializers.py
   │  ├─ sub_topic.py
   │  └─ views.py
   |
   ├─ tag
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ serializer.py
   │  ├─ tag.py
   │  └─ views.py
   |
   ├─ templates
   │  ├─ assignment_submitted.html
   │  ├─ course_assigned.html
   │  └─ otp_email.html
   |
   ├─ topic
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ serializers.py
   │  ├─ topic.py
   │  └─ views.py
   |
   ├─ user
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ serializers.py
   │  ├─ swagger.py
   │  ├─ user.py
   │  └─ views.py
   |
   ├─ user_assignment
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ admin_views.py
   │  ├─ serializer.py
   │  ├─ user_assignment.py
   │  └─ user_views.py
   |
   ├─ user_assignment_submission
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ admin_views.py
   │  ├─ serializer.py
   │  ├─ user_assignment_submission.py
   │  └─ user_views.py
   |
   ├─ user_course_enrollment
   │  ├─ __init__.py
   │  ├─ accessor.py
   │  ├─ admin_views.py
   │  ├─ search.py
   │  ├─ serializer.py
   │  ├─ swagger.py
   │  ├─ user_course_enrollment.py
   │  └─ user_views.py
   |
   └─ utils
      ├─ __init__.py
      ├─ hashing.py
      ├─ swagger.py
      ├─ utils.py
      └─ validators.py

```
## Tree Levels
### Root Level
Root level of project contains following items:
```
superskillup
├─ .circleci\
├─ .gitignore
├─ docker-compose.main.yml
├─ Dockerfile
├─ entrypoint.sh
├─ Makefile
├─ manage.py
├─ README.md
├─ requirements.txt
├─ superskillup\
└─ app\
```
- `.circleci\`:  contains configuration files for CI/CD pipeline

- `.gitignore`:  contains files and folders to exclude form git.

- `docker-compose.main.yml`:  contains configuration for setting up a docker container.

- `Dockerfile`:  contains configuration for building an image from the project.

- `entrypoint.sh`:  contains command to run when Docker container starts.

- `Makefile`:  contains commands for project automation using Make.

- `manage.py`: contains django project management commands.

- `README.md`: contains project documentation and information.

- `requirements.txt`: contains python dependencies for the project.

- `superskillup\`: contains project-specific files and modules.

- `app\`: contains the he main application files and modules.

### Project Level
Project level of contains following items:
```
└─ superskillup
   ├─ __init__.py
   ├─ asgi.py
   ├─ settings.py
   ├─ urls.py
   └─ wsgi.py
```
- `__init__.py`: This file is required to treat the directory as a python package.

- `asgi.py`: ASGI (Asynchronous Server Gateway Interface) configuration file for asynchronous web servers.

- `settings.py`: Django project settings and configurations, including database settings, middleware, static files, etc.

- `urls.py`: URL routing configuration for mapping URL patterns to views.

- `wsgi.py`: WSGI (Web Server Gateway Interface) configuration file for serving the Django application with web servers like Gunicorn or uWSGI.

### App Level
```
└─ app
   ├─ __init__.py
   ├─ admin.py
   ├─ apps.py
   ├─ models.py
   ├─ urls.py
   ├─ api\
   ├─ app_admin\
   ├─ assignment\
   ├─ course\
   ├─ gpt_review\
   ├─ manager_feedback\
   ├─ migrations\
   ├─ question\
   ├─ question_answer\
   ├─ services\
   ├─ shared\
   ├─ sub_topic\
   ├─ tag\
   ├─ templates\
   ├─ topic\
   ├─ user\
   ├─ user_assignment\
   ├─ user_assignment_submission\
   ├─ user_course_enrollment\
   └─ utils\
```
 - `__init__.py`: This file is required to treat the directory as a python package.

 - `admin.py`: Django admin configuration for registering models.

 - `apps.py`: Configuration for the Django application.

 - `models.py`: Django models for defining database structure.

 - `urls.py`: URL routing configuration for the Django app.

 - `api\`: Directory for API-related modules and views.

 - `app_admin\`: Directory for admin-related modules and their views.

 - `assignment\`: Directory for assignment-related modules and their views.

 - `course\`: Directory for course-related modules and their views

 - `gpt_review\`: Directory for GPT-Review-related modules and their views.

 - `manager_feedback\`: Directory for manager-feedback-related modules and their views.

 - `migrations\`: Directory for Django database migrations.

 - `question\`: Directory for question-related modules and their views.

 - `services\`: Directory for service-related modules like email service etc.

 - `shared\`: Directory for shared modules and utilities.

 - `sub_topic\`: Directory for sub-topic-related modules and their views.

 - `tag\`: Directory for tag-related modules and their views.

 - `templates\`: Directory for Django templates.

 - `topic\`: Directory for topic-related modules and their views.

 - `user\`: Directory for user-related modules and their views.

 - `user_assignment\`: Directory for user-assignment-related modules and their views.

 - `user_assignment_submission\`: Directory for user-assignment-submission modules related to user assignment submissions.

 - `user_course_enrollment\`: Directory for user-course-enrollment-related modules and their views.

 - `utils\`: Directory for utility modules and functions.


### Views Level
`User model` is taken for example:
```
   └── user
     ├─ __init__.py
     ├─ accessor.py
     ├─ serializers.py
     ├─ swagger.py
     ├─ user.py
     └─ views.py
```
 - `__init__.py`: This file is required to treat the directory as a python package.

 - `accessor.py`: contains all accessor functions responsible for managing user-related data. It serves as the designated gateway for database interactions concerning the user model, though there may be exceptions.

 - `serializers.py`: contains serializers for user model data and their interactions. 

 - `swagger.py`: contains custom swagger documentation for user-related endpoints.

 - `user.py`: contains the business logic related to user models. It also serves as a gateway for interactions between `user accessor` and business layer of other models.

 - `views.py`: contains view functions for handling user-related requests and responds in json format.

***Note: In some cases, views may be separated into user views and admin views if there is a clear distinction between them.***
```
├─ admin_views.py
└─ user_views.py
```

### API Level
```
   └── api
      ├─ __init__.py
      ├─ api.py
      └─ response_builder.py
```
 - `__init__.py`: This file is required to treat the directory as a python package.
- `api.py`: contains custom codes with their messages for responding to requests.
- `response_builder.py`: contains a response builder classs which generates a response object as required.

## Use Case Diagram
- Url: [`SuperSkillUp Use Case Diagram`](https://drive.google.com/file/d/1TGz1t_Ipd-n7ZE24WAM3dFHdZAMM3QK1/view?usp=sharing)