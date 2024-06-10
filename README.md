# video-watch-history
The video-watch-history contains a python application designed to track and log watch events for videos. It provides RESTful API endpoints to record when a user watches a video and to retrieve the watch history for a specific user.


# Setup

   1. Clone the repository:
       git clone https://github.com/akashrajk54/video-watch-history.git

   2. Navigate to the project directory:
       cd video-watch-history

   3. Create a virtual environment (optional but recommended):
       python -m venv venv

   4. Activate the virtual environment:
      a). Windows:
          venv\Scripts\activate
      b). Linux/macOS:
          source venv/bin/activate

   5. Install dependencies:
      pip install -r requirements.txt

   6. Set up environment variables:
       # DATABASE Use: PostgresSQL
       DATABASE_NAME=''
       DATABASE_USER=''
       DATABASE_PASSWORD=''
       DATABASE_HOST='localhost'
       DATABASE_PORT='5432'

       MAX_TIME_LIMIT_TO_VERIFY_OTP='3' (otp valid max 3min)
        
       TWILIO_ACCOUNT_SID=''
       TWILIO_AUTH_TOKEN=''
       TWILIO_PHONE_NUMBER=''

       # During production 
            Debug = False
            ALLOWED_HOSTS = insted of ['*'], please add specific frontend url, so that request from anyother will be rejected.
       # Please Update DEFAULT_THROTTLE_RATES into the settings currently set to 100/Hours

   7. Run migrations to create the database schema:
      python manage.py makemigrations
      python manage.py migrate

   8. Create a superuser (admin) account:
      python manage.py createsuperuser

   9. Run the development server:
      python manage.py runserver
      (by default it will use 8000 port)

# To use ElasticSearch(skip 7, 8, 9 points and start from 10 after 6)
   10. Install Docker.
   11. Create a Dockerfile for the project image creation.
   12. Configure the Docker Compose file to include services for the Django project, PostgreSQL database, Elasticsearch container, and Kibana container.
   13. Build and start the Docker containers:
        docker-compose up --build
   14. Run migrations to create the database schema:
       docker-compose exec web python manage.py makemigrations
       docker-compose exec web python manage.py migrate
   15. Create a superuser (admin) account:
       docker-compose exec web python manage.py createsuperuser
   16. Create an Elasticsearch index and document:
       docker-compose exec web python manage.py search_index --create
   17. Check if all fine:
       This below command will return information about all indices in Elasticsearch, and you should see mediacontents among them.
       curl -X GET "localhost:9200/_cat/indices?v"
       


# Functionality:
The backend provides comprehensive functionality for managing video watch history, including user authentication, video uploading, watching videos, and retrieving watch history. Each API endpoint is designed to fulfill specific requirements, ensuring that users can perform desired actions efficiently and effectively.

# Code Quality:
The backend codebase adheres to best practices for clean, maintainable, and well-documented code. It follows the Django framework conventions, utilizes descriptive variable and function names, and includes comments and docstrings to explain the purpose and usage of different components.
# User Experience:
The backend aims to deliver a smooth and intuitive user experience by offering a straightforward API interface with clear and consistent endpoint naming and request/response formats. Error messages are informative and user-friendly, guiding users on how to rectify issues or provide necessary input.

# Problem Solving:
The backend effectively handles potential issues such as API errors and load performance through robust error handling mechanisms, caching strategies, and optimization techniques. Error responses are properly formatted with appropriate HTTP status codes and error messages, enabling clients to identify and address issues promptly. Additionally, caching mechanisms are employed to improve performance and reduce database load by caching frequently accessed data.
