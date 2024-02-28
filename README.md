# Capstone Project CS50's Web Programming with Python and JavaScript

By Matthias Gruber

## Distinctiveness and Complexity

This project was my final project of Harvard's CS50 Web Programming with Python and JavaScript. The requirement was to develop a web application of my own idea and entirely from scratch. The project utilizes the Django framework. The main programming language used is Python supported by JavaScript, CSS and HTML code.

`Personal Training Log` is a web application for Personal Trainers and their customers to log training records and customer body stats biometrics.

I have based my work on following criterias to be distinctive and offering additional complexity to the material learned in the course:

1. Being a Personal Trainer myself, I have developed the application based on my personal experiece which functionality a trainer and his customers would be interested in.

2. Introducing two different user types/roles:

I have introduced two different types/roles of users which are `CUSTOMER` and `TRAINER`. Inheriting from the main `User` class, two separate proxy classes `Customer` and `Trainer` were introduced. Furthermore this offers the ability add specific `CustomerDetails` and `CustomerBiometrics` for customes only, as well as specific `TrainerDetails` for trainers.

Each customer can have 0 or 1 trainer. A trainer can have 0 to many customers. Customers have access to their own profile, workout list and workout details. Trainers have access to those views for all of their customers and themselves.

3. Django messages framework

The Django message framework has been added to allowing to display flash notifications to users.

4. Django testing

Django testing including client testing has been added to the application in the `tests.py` file.


## Models

### User

* Inheriting from Django's `AbstractUser` model
* Additional `role` field has been added to distinguish between customer and trainer

### Trainer, TrainerManager, TrainerDetail
* The `Trainer` proxy class inherits from `User` for the role of trainer
* Supported by `TrainerManager` and `TrainerDetail`
* A trainer can have 0 to many customers

### Customer, CustomerManager, CustomerDetail, CustomerBiometric
* The `Customer` proxy class inherits from `User` for the role of customer 
* Supported by `CustomerManager`, `CustomerDetail` and `CustomerBiometric`
* Body stats biometrics can only be added for customers
* Each customer can have 0 or 1 trainer

### MuscleGroup
* Defines the `MuscleGroup` trained by an specific `Exercise`

### Exercise
* An `Exercise` that can be part of a `Workout`

### Workout
* A `Workout` scheduled for a specific user and time

### WorkoutExercise
* An `Exercise` being part of a specific `Workout`

### WorkoutSet
* A `Set` tracking repetitions, weight and number of sets for a specific `WorkoutExercise`


## URL patterns and related view functions

### Index

HTML: `index.html`
URL: ` `
View: `index`

* Initial welcome page for all users
* If the user is not authenticated the page shows links to the login and registration pages
* If the user is authenticated it shows a personalized welcome message and a link to the personal workout list

### Register

HTML: `register_select.html` and `register_form.html`
Path: `register/<str:role_select>`
View: `register`

* Registration for new users
* First at `register/select` new users can select if they are customers or trainers
* Then users get redirected to the respecive form on `register/customer` or `register/trainer`

### Login

HTML: `login.html`
Path: `login`
View: `login_user`

* Login page
* If a user is already authenticated the request gets redirected to `index`

### Logout

HTML: Not applicable
Path: `logout`
View: `login_user`

* Path to request the logout of the current user
* The user gets logged out and redirected to `index`

### Change Password

HTML: `change_password.html`
Path: `change-password`
View: `change_password`

* Allows the logged in user to change their current password
* If no user is authenticated the request gets redirected to `login`

### Password Reset

HTML: `password_reset.html`
Path: `password-reset`
View: `password_reset`

* Allows the logged in user to request an email to reset their password
* This feature is currently only in preparation, but not able to send emails since the application is not online yet

### Change Profile

HTML: `change_profile.html`
Path: `change-profile`
View: `change_profile`

* Allows the logged in user to update their profile information for both `Customer`/`CustomerDetail` or `Trainer`/`TrainerDetail` model fields
* If no user is authenticated the request gets redirected to `login`

### Add Body Stats

HTML: `add_body_stats.html`
Path: `add-body-stats/<int:customer_id>`
View: `add_body_stats`

* Allows users to add body stats biometrics for a specific customer
* Trainers are able to add stats for all their customers, and customers are able to add stats for themselfes only
* Stats can not be added to trainer user profiles (Error pop-up message and redirect to the trainer's `profile` page)
* Stats can not be added by customers to other users, or trainers for users who are not their customers (Error pop-up message and redirect `index`)
* If no user is authenticated the request gets redirected to `login`

### Profile

HTML: `profile.html`
Path: `profile/<int:user_id>`
View: `profile`

* Allows customers to see their profile information and body stats
* Trainers are able access all their customers profile pages, but not the pages of customers not related to them
* Traines profile pages will show a list of their customers instead of the body stats section
* If no user is authenticated the request gets redirected to `login`

### Workout List

HTML: `workout_list.html`
Path: `workout-list/<int:filter_id>`
View: `workout_list`
JavaScript: `workout-list.js`

* Shows a list of all workouts
* A customer will only see their own workouts
* A trainer will see all workouts related to their customers
* Workouts are sorted by date descending
* Paginiation has been added to show 5 workouts a time
* Trainers can filter the workouts for one customer or show all. `filter_id` relates to the `user_id` and 0 would show all avalialable workouts.
* This page also allows to add new workouts. Customers can add new workouts only for themselves. Trainers can add new workouts for all their customers only.
* If no user is authenticated the request gets redirected to `login`

### Workout View

HTML: `workout_view.html`
Path: `workout-view/<int:workout_id>`
View: `workout_view`
JavaScript: `workout-view.js`

* Views all exercises and details of a single workout
* Workout details can be updated utilizing `AddWorkoutForm`
* New exercises can be added utelizing `AddWorkoutExerciseForm`
* A customer will only have access to view and update their own workouts
* A trainer will have access to view and update all their customer's workouts
* If no user is authenticated the request gets redirected to `login`

**The workout view also integrates addional url paths and view functions to fetch PUT requests and utelize DOM manipulation:**

1. Delete a workout exercise by icon click
2. Move-up a workout exercise by icon click
3. Move-down a workout exercise by icon click
4. Update workout sets
5. Add workout sets
6. Workout sets automatically will be deleted if both the number of repecitions and the weigth are 0 or empty

### Layout

HTML: `layout.html`
CSS `styles.css`

* All  html files above extent to `layout.html` including `styles.css` 
* Addtionally the Bootstrap library has been utelized to support mobile-responsive design and application


## Requirments and instructions

I have run this application and all previous projects of this course on a `conda` environment on a `win-64` system. The full specifications of the environment can be found in the `requirements.txt` file.

The project's main directory `fitness` contains the Django project `fitness` with a single app called `workout`.

The project can be started from the terminal in the main directory with `python manage.py runserver`.

The sqlite3 database `db.sqlite3` has been pre-filled with example data for a few customers and trainers. Additionally you will be able to create new customers or trainers and add workout details directly.


## Limitations

The current version of this applications has following limitaions which I would aim to further improve in the future:

* A functionality to evaluate the customers progress of their workouts and body stats biometrics is not yet available.
* Each exercise can only be paired with one major muscle group and not several muscles.
* `Exercise` and `MuscleGroup` instances can only be modifide utilizing the admin interface, not by trainers or clients direclty.
* A `reset password` view has been created but is unavailable due the applicaiton not being online.
* After the initial registration of a new user, the role can not be changed later.
* Body stats biometrics can not be amended or deleted (only from the admin interface).


Video overview: <https://youtu.be/fULhp1YcxKA>