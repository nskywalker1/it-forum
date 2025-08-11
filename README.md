# DEV FORUM 
#### An online forum for programmers, where anyone can create their own topic in a selected category and discuss it in the comments. There is a profile function, as well as the ability to add and delete posts. In general, I created this project to try out Celery for sending SMS messages and password reset notifications. I also used Docker.

### 📦 Technologies Used
1. Python
2. Django
3. JavaScript
4. Tailwind
5. PostgreSQL
6. Celery
7. Redis
8. Docker

### You must have installed

- [Docker](https://www.docker.com/get-started) >= 20.x
- [Docker Compose](https://docs.docker.com/compose/install/) >= 2.x
- Git

### 🚀 Installation
1. Clone or download the project to your local machine.
2. Rename the .env-test file to .env and configure variables.
3. Build and start the containers
```bash
docker-compose up --build
```
4. Access the application
   Homepage: http://localhost:8000
   
   Admin panel: http://localhost:8000/admin (admin = email:admin@example.com password:123) 
