from flask import Flask, request
from flask_migrate import Migrate
from datetime import date
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from models import db, Workout, Exercise, WorkoutExercise
from marshmallow import ValidationError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


@app.route("/")
def home():
    return {"message": "Workout Application API is running!"}


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return workouts_schema.dump(workouts), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    workout_data = workout_schema.dump(workout)

    workout_data["exercises"] = []

    for association in workout.workout_exercises:
        exercise_data = exercise_schema.dump(association.exercise)

        exercise_data["reps"] = association.reps
        exercise_data["sets"] = association.sets
        exercise_data["duration_seconds"] = association.duration_seconds

        workout_data["exercises"].append(exercise_data)

    return workout_data, 200


@app.route("/workouts", methods=["POST"])
def create_workout():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Request body must be a JSON object"}, 400

    try:
        workout_data = workout_schema.load(data)

        if workout_data.get("date") is None:
            workout_data["date"] = date.today()

        workout = Workout(**workout_data)

        db.session.add(workout)
        db.session.commit()

    except ValidationError as error:
        db.session.rollback()
        return {"error": error.messages}, 400

    except (ValueError, TypeError):
        db.session.rollback()
        return {"error": "Invalid workout data or date format"}, 400

    except Exception:
        db.session.rollback()
        return {"error": "Could not create workout"}, 500

    return workout_schema.dump(workout), 201


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    try:
        db.session.delete(workout)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "Could not delete workout"}, 500

    return {"message": "Workout deleted successfully"}, 200


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return exercises_schema.dump(exercises), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    exercise_data = exercise_schema.dump(exercise)
    exercise_data["workouts"] = []

    for association in exercise.workout_exercises:
        workout_data = workout_schema.dump(association.workout)
        exercise_data["workouts"].append(workout_data)

    return exercise_data, 200


@app.route("/exercises", methods=["POST"])
def create_exercise():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Request body must be a JSON object"}, 400

    try:
        exercise_data = exercise_schema.load(data)

    except ValidationError as error:
        return {"error": error.messages}, 400

    try:
        exercise = Exercise(**exercise_data)
        db.session.add(exercise)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {
            "error": "Could not create exercise. The name may already exist."
        }, 500

    return exercise_schema.dump(exercise), 201


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    try:
        db.session.delete(exercise)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "Could not delete exercise"}, 500

    return {"message": "Exercise deleted successfully"}, 200

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Request body must be a JSON object"}, 400

    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return {"error": "Workout not found"}, 404

    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return {"error": "Exercise not found"}, 404

    try:
        association_data = workout_exercise_schema.load({
            **data,
            "workout_id": workout_id,
            "exercise_id": exercise_id
        })

    except ValidationError as error:
        return {"error": error.messages}, 400

    try:
        association = WorkoutExercise(**association_data)
        db.session.add(association)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {
            "error": "Could not add exercise. It may already be linked to this workout."
        }, 400

    return workout_exercise_schema.dump(association), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)

