# IITBBS-BLOG

This repository contains a Flask application with a fully functional backend and database integration. The application includes user authentication, blog posts, and an account management system. Below are the steps to set up and run the application both locally and using Docker.


## Installation

### Local Installation

1. **Create and Activate Virtual Environment**

    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

2. **Install Dependencies**

    ```sh
    pip install --no-cache-dir -r requirements.txt
    ```

3. **Initialize the Database**

    ```sh
    flask db upgrade
    ```

4. **Run the Application**

    ```sh
    flask run
    ```

### Docker Installation

1. **Build the Docker Image**

    ```sh
    docker build -t flask-database-app .
    ```

2. **Run the Docker Container**

    ```sh
    docker run -d -p 8000:8000 flask-database-app
    ```

## Routes

| Route                  | Method    | Endpoint                          |
|------------------------|-----------|-----------------------------------|
| `main.about`           | GET       | `/about`                          |
| `main.home`            | GET       | `/home`                           |
| `main.home`            | GET       | `/`                               |
| `posts.delete_post`    | POST      | `/post/<int:post_id>/delete`      |
| `posts.new_post`       | GET, POST | `/post/new`                       |
| `posts.post`           | GET       | `/post/<int:post_id>`             |
| `posts.update_post`    | GET, POST | `/post/<int:post_id>/update`      |
| `static`               | GET       | `/static/<path:filename>`         |
| `users.account`        | GET, POST | `/account`                        |
| `users.confirm_token`  | GET, POST | `/confirm/<token>`                |
| `users.delete_account` | POST      | `/user/<int:user_id>/delete`      |
| `users.login`          | GET, POST | `/login`                          |
| `users.logout`         | GET       | `/logout`                         |
| `users.register`       | GET, POST | `/register`                       |
| `users.reset_request`  | GET, POST | `/reset_password`                 |
| `users.reset_token`    | GET, POST | `/reset_password/<token>`         |
| `users.user_posts`     | GET       | `/user/<string:username>`         |

## Features

- User Registration and Authentication
- Password Reset via Email
- Blog Post Creation, Update, and Deletion
- User Profile Management
- Error Handling and Custom Error Pages


## Configuration

The application uses environment variables for configuration. Ensure you set the following variables in your environment or Docker container:

- `FLASK_APP`: Set to `wsgi.py`
- `FLASK_ENV`: Set to `development` or `production`
- `SECRET_KEY`: Your secret key for sessions
- `SQLALCHEMY_DATABASE_URI`: The URI for your database
- `MAIL_SERVER`: Your mail server (for password reset)
- `MAIL_PORT`: Mail server port
- `MAIL_USE_TLS`: Whether to use TLS
- `MAIL_USERNAME`: Mail username
- `MAIL_PASSWORD`: Mail password

## Dockerfile

```dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP wsgi.py
ENV FLASK_RUN_HOST 0.0.0.0

# Set the working directory
WORKDIR /app

# Create and activate virtual environment, then install dependencies
RUN python -m venv .venv && \
    source .venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application to the container
COPY . /app/

# Create the necessary directories and initialize the database
RUN flask db upgrade

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
```

## Setup Script

```sh
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Initialize the database
flask db upgrade

# Command to run the application
exec gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

## Running the Application

- For local setup, the application will be available at `http://127.0.0.1:5000`
- For Docker setup, the application will be available at `http://localhost:8000`

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -m 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Contact

- Author: Your Name
- Email: your.email@example.com

Feel free to reach out for any questions or collaboration ideas!

---

This README provides a comprehensive overview of the project, including setup instructions for both local and Docker environments, as well as additional information about the application features and structure.