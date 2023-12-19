from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/<str:role_select>", views.register, name="register"),
    path("login", views.login_user, name="login_user"),
    path("logout", views.logout_user, name="logout_user"),
    path("change-password", views.change_password, name="change_password"),
    path("password-reset", views.password_reset, name="password_reset"),
    path("change-profile", views.change_profile, name="change_profile"),
    path("add-body-stats/<int:customer_id>", views.add_body_stats, name="add_body_stats"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("workout-list/<int:filter_id>", views.workout_list, name="workout_list"),
    path("workout-view/<int:workout_id>", views.workout_view, name="workout_view"),
    path("delete-workout-exercise/<int:exercise_id>", views.delete_workout_exercise, name="delete_workout_exercise"),
    path("move-up-workout-exercise/<int:exercise_id>", views.move_up_workout_exercise, name="move_up_workout_exercise"),
    path("move-down-workout-exercise/<int:exercise_id>", views.move_down_workout_exercise, name="move_down_workout_exercise"),
    path("update-workout-sets/<int:exercise_id>", views.update_workout_sets, name="update_workout_sets"),
    path("add-workout-set/<int:exercise_id>", views.add_workout_set, name="add_workout_set")
]