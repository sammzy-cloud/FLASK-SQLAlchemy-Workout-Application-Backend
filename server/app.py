from flask import Flask, request
from flask_migrate import Migrate
from datetime import date

from models import db, Workout, Exercise, WorkoutExercise

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return {"message": "Workout Application API is running!"}


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return [
        {
            "id": workout.id,
            "date": workout.date.isoformat(),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        }
        for workout in workouts
    ], 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    exercises = []

    for association in workout.workout_exercises:
        exercises.append({
            "id": association.exercise.id,
            "name": association.exercise.name,
            "category": association.exercise.category,
            "equipment_needed": association.exercise.equipment_needed,
            "reps": association.reps,
            "sets": association.sets,
            "duration_seconds": association.duration_seconds
        })

    return {
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "exercises": exercises
    }, 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Request body must be a JSON object"}, 400

    duration = data.get("duration_minutes")

    if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
        return {"error": "duration_minutes must be a positive integer"}, 400

    try:
        workout = Workout(
            duration_minutes=duration,
            date=date.fromisoformat(data["date"]) if data.get("date") else date.today(),
            notes=data.get("notes")
        )

        db.session.add(workout)
        db.session.commit()

    except (ValueError, TypeError):
        db.session.rollback()
        return {"error": "Invalid workout data or date format"}, 400
    except Exception:
        db.session.rollback()
        return {"error": "Could not create workout"}, 400

    return {
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes
    }, 201



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

    return [
        {
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        }
        for exercise in exercises
    ], 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    workouts = []

    for association in exercise.workout_exercises:
        workouts.append({
            "id": association.workout.id,
            "date": association.workout.date.isoformat(),
            "duration_minutes": association.workout.duration_minutes,
            "notes": association.workout.notes
        })

    return {
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed,
        "workouts": workouts
    }, 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Request body must be a JSON object"}, 400

    name = data.get("name")
    category = data.get("category")
    equipment_needed = data.get("equipment_needed", False)

    if not isinstance(name, str) or not name.strip():
        return {"error": "name must be a non-empty string"}, 400

    if not isinstance(category, str) or not category.strip():
        return {"error": "category must be a non-empty string"}, 400

    if not isinstance(equipment_needed, bool):
        return {"error": "equipment_needed must be true or false"}, 400

    exercise = Exercise(
        name=name,
        category=category,
        equipment_needed=equipment_needed
    )

    try:
        db.session.add(exercise)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "Could not create exercise. The name may already exist."}, 400

    return {
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed
    }, 201



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

    reps = data.get("reps")
    sets = data.get("sets")
    duration_seconds = data.get("duration_seconds")

    for field, value in [
        ("reps", reps),
        ("sets", sets),
        ("duration_seconds", duration_seconds)
    ]:
        if value is not None and (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value <= 0
        ):
            return {"error": f"{field} must be a positive integer"}, 400

    association = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=reps,
        sets=sets,
        duration_seconds=duration_seconds
    )

    try:
        db.session.add(association)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {
            "error": "Could not add exercise. It may already be linked to this workout."
        }, 400

    return {
        "id": association.id,
        "workout_id": association.workout_id,
        "exercise_id": association.exercise_id,
        "reps": association.reps,
        "sets": association.sets,
        "duration_seconds": association.duration_seconds
    }, 201





if __name__ == "__main__":
    app.run(port=5555, debug=True)

