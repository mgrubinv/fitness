# Generated by Django 4.1 on 2023-12-06 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workout", "0017_workout_scheduled_date_workout_scheduled_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="workout",
            name="workout_title",
            field=models.CharField(default="Workout", max_length=50),
        ),
    ]
