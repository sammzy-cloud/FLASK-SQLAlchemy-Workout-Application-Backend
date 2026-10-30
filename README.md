# FLASK-SQLAlchemy-Workout-Application-Backend


## Project Description

The Flask SQLAlchemy Workout Application Backend is a RESTful API that allows users to manage workouts and exercises.

The application uses Flask to handle API requests, SQLAlchemy to manage database relationships, Flask-Migrate to handle database migrations, and Marshmallow to validate, serialize, and deserialize data.

Users can create, retrieve, and delete workouts and exercises. They can also associate exercises with workouts while recording details such as sets, repetitions, and duration.

## Technologies Used

- Python 3.8.13
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy
- Marshmallow
- SQLite
- Pipenv

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sammzy-cloud/FLASK-SQLAlchemy-Workout-Application-Backend.git
cd FLASK-SQLAlchemy-Workout-Application-Backend
```

### 2. Install dependencies

Install the project dependencies using Pipenv:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

### 3. Navigate to the server directory

```bash
cd server
```

### 4. Set up the database

Initialize the migration repository if it does not already exist:

```bash
flask --app app db init
```

Generate a migration:

```bash
flask --app app db migrate -m "Initial migration"
```

Apply the migration to create the database tables:

```bash
flask --app app db upgrade
```

**Note:** If the migration directory already exists in the repository, do not run `db init` again. Use the existing migrations and run `flask --app app db upgrade`.

### 5. Seed the database

Run the seed script to populate the database with sample exercises, workouts, and workout-exercise associations:

```bash
python seed.py
```

## Running the Application

From the `server` directory, start the Flask application:

```bash
python app.py
```

The application runs at:

`http://127.0.0.1:5555`

## API Endpoints

This API provides endpoints for managing workouts, exercises, and workout-exercise associations.

### Workouts

#### `GET /workouts`
Returns all workouts stored in the database.

#### `GET /workouts/<workout_id>`
Returns a specific workout, including its associated exercises and their details.

#### `POST /workouts`
Creates a new workout.

#### `DELETE /workouts/<workout_id>`
Deletes a workout using its unique ID.


### Exercises

#### `GET /exercises`
Returns all exercises stored in the database.

#### `GET /exercises/<exercise_id>`
Returns a specific exercise, including its associated workouts.

#### `POST /exercises`
Creates a new exercise.


#### `DELETE /exercises/<exercise_id>`
Deletes an exercise using its unique ID.

---

### Workout-Exercise Associations

#### `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`
Associates an existing exercise with a workout and records its workout-specific details.

---

## Database Models

The application contains three main models:

- **Exercise:** Stores exercise information, including its name, category, and whether equipment is required.
- **Workout:** Stores workout information, including its date, duration, and notes.
- **WorkoutExercise:** Connects workouts and exercises and stores exercise-specific details such as sets, repetitions, and duration in seconds.

## Validation and Serialization

Marshmallow schemas validate incoming data and serialize model instances into JSON responses.

The application also uses SQLAlchemy model validations and database constraints to maintain data integrity.

## Author

Samantha Ng'iela