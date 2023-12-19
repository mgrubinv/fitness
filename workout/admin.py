from django.contrib import admin
from .models import User, Customer, Trainer, CustomerDetail, TrainerDetail, CustomerBiometric, MuscleGroup, Exercise, Workout, WorkoutExercise, WorkoutSet

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "role", "gender")

class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ("user",)

class TrainerDetailsAdmin(admin.ModelAdmin):
    list_display = ("user",)

class CustomerBiometricsAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_on")

class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "muscle")

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "exercise_name", "muscle")

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("customer", "workout_title", "scheduled_date", "scheduled_time")

class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ("workout", "exercise", "sequence_nr")

class WorkoutSetAdmin(admin.ModelAdmin):
    list_display = ("workout_exercise", "reps", "weight")

admin.site.register(User, UserAdmin)
admin.site.register(CustomerDetail, CustomerDetailsAdmin)
admin.site.register(TrainerDetail, TrainerDetailsAdmin)
admin.site.register(CustomerBiometric, CustomerBiometricsAdmin)
admin.site.register(MuscleGroup, MuscleGroupAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(WorkoutExercise, WorkoutExerciseAdmin)
admin.site.register(WorkoutSet, WorkoutSetAdmin)