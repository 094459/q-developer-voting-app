# Voting Application

This is a Flask-based voting application that allows users to create polls and vote on them.

## Prerequisites

- Python 3.7 or higher
- PostgreSQL

## Installation

1. Clone the repository:


2. Create a virtual environment:

```
python -m venv venv
```


3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install the required dependencies:

```
pip install -r requirements.txt
```


## Database Setup

1. Ensure PostgreSQL is installed and running on your system.

2. Create a new PostgreSQL database for the application:

```
createdb voting
```


3. Update the database connection string in `app.py`:

```
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/voting'
```
Replace username and password with your PostgreSQL credentials.



## Running the Application

Set the Flask application environment variables:

On Windows:

```
set FLASK_APP=app.py
set FLASK_ENV=development

```

On macOS and Linux:

```
export FLASK_APP=app.py
export FLASK_ENV=development

```

Run the Flask development server:

```
flaskk run
```

Open your web browser and navigate to http://127.0.0.1:5000 to access the application.

## Usage

Usage
Register a new account or log in with an existing one.

Create new polls with multiple options.

Vote on existing polls.

View poll results.

## Contributing

Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
