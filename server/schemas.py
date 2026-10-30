
from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Regexp(
            r".*\S.*",
            error="Name cannot be empty or contain only spaces."
        )
    )

    category = fields.Str(
        required=True,
        validate=validate.Regexp(
            r".*\S.*",
            error="Category cannot be empty or contain only spaces."
        )
    )

    equipment_needed = fields.Bool(load_default=False)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(load_default=None, allow_none=True)

    duration_minutes = fields.Int(
        required=True,
        strict=True,
        validate=validate.Range(min=1, error="Duration must be a positive integer.")
    )

    notes = fields.Str(allow_none=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(required=True, strict=True)
    exercise_id = fields.Int(required=True, strict=True)

    reps = fields.Int(
        allow_none=True,
        strict=True,
        validate=validate.Range(min=1, error="Reps must be a positive integer.")
    )

    sets = fields.Int(
        allow_none=True,
        strict=True,
        validate=validate.Range(min=1, error="Sets must be a positive integer.")
    )

    duration_seconds = fields.Int(
        allow_none=True,
        strict=True,
        validate=validate.Range(
            min=1,
            error="Duration in seconds must be a positive integer."
        )
    )

