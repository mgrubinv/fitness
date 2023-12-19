# Generated by Django 4.1 on 2022-12-28 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workout", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[],
            options={"proxy": True, "indexes": [], "constraints": [],},
            bases=("workout.user",),
        ),
        migrations.CreateModel(
            name="Trainer",
            fields=[],
            options={"proxy": True, "indexes": [], "constraints": [],},
            bases=("workout.user",),
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("CUSTOMER", "Customer"), ("TRAINER", "Trainer")],
                default="CUSTOMER",
                max_length=50,
            ),
        ),
    ]
