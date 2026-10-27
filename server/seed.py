from datetime import date, timedelta
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    
    db.session.query(WorkoutExercise).delete()
    db.session.query(Workout).delete()
    db.session.query(Exercise).delete()

    
    pushups = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )
    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )
    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=True
    )

    db.session.add_all([pushups, squats, running])
    db.session.flush()

    
    workout1 = Workout(
        date=date.today(),
        duration_minutes=30,
        notes="Full body workout"
    )
    workout2 = Workout(
        date=date.today() - timedelta(days=1),
        duration_minutes=25,
        notes="Cardio session"
    )

    db.session.add_all([workout1, workout2])
    db.session.flush()

    
    db.session.add_all([
        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=pushups.id,
            reps=15,
            sets=3
        ),
        WorkoutExercise(
            workout_id=workout1.id,
            exercise_id=squats.id,
            reps=20,
            sets=3
        ),
        WorkoutExercise(
            workout_id=workout2.id,
            exercise_id=running.id,
            duration_seconds=1200
        )
    ])

    db.session.commit()

    print("Database seeded successfully!")
    print("Created 3 exercises, 2 workouts, and 3 workout-exercise associations.")
