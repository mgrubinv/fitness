# Generated by Django 4.1 on 2023-01-11 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "workout",
            "0014_remove_workoutset_exercise_remove_workoutset_workout_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(model_name="workoutset", name="workout_exercise",),
        migrations.DeleteModel(name="WorkoutExercise",),
        migrations.DeleteModel(name="WorkoutSet",),
    ]