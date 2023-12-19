from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json

from django.views.decorators.csrf import csrf_exempt


from .models import User, Customer, Trainer, CustomerDetail, CustomerBiometric, TrainerDetail, Workout, WorkoutExercise, WorkoutSet, Exercise
from .forms import RegisterUserForm, RegisterCustomerForm, RegisterTrainerForm, LoginForm, UserUpdateForm, UserPasswordChangeForm, UserPasswordResetForm, CustomerDetailUpdateForm, TrainerDetailUpdateForm, AddCustomerBiometricForm, AddWorkoutExerciseForm, AddWorkoutForm

# Home view

def index(request):
    return render(request, "workout/index.html")


# User administatration

def register(request, role_select):
    if role_select == 'trainer' or role_select == 'customer':
        if request.method == "POST":
            if role_select == 'trainer':
                form = RegisterTrainerForm(request.POST)
            elif role_select == 'customer':
                form = RegisterCustomerForm(request.POST)
            else:
                messages.error(request, 'User type not valid!')
                return render(request, 'workout/register_select.html')
            
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, 'Registration completed!')
                return redirect('index')
            else:
                messages.error(request, 'Form not valid!')
                return render(request, 'workout/register_form.html', {
                'form': form, 'role_select': role_select
                }) 
        else:
            if role_select == 'trainer':
                form = RegisterTrainerForm()
            else:
                form = RegisterCustomerForm()
            
            return render(request, 'workout/register_form.html', {
                    'form': form, 'role_select': role_select
                })
    else:
        return render(request, 'workout/register_select.html')

def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'workout/login.html', {
                    'form': LoginForm(),
                    'message': "Invalid username and/or password."
                })
        else:
            return render(request, 'workout/login.html', {
                    'form': LoginForm()
                })

@login_required
def change_password(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was updated!')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, "Invalid input. Please try again!")
            return render(request, 'workout/change_password.html', {
                'form': UserPasswordChangeForm(user=request.user)
            })
    else:
        return render(request, 'workout/change_password.html', {
                'form': UserPasswordChangeForm(user=request.user)
            })

@login_required
def password_reset(request):
    if request.method == "POST":
        form = UserPasswordResetForm()
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'workout/password_reset.html', {
                'form': UserPasswordResetForm(), 
                'message': "Invalid input. Please try again!"
            })
    else:
        return render(request, 'workout/password_reset.html', {
                'form': UserPasswordResetForm()
            })

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Profile administration

@login_required
def profile(request, user_id):
    try:
        profile_user = User.objects.get(id=int(user_id))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
    
    if (request.user.role == 'TRAINER' and profile_user in request.user.get_trainer_customer_list()) or (request.user.role == 'CUSTOMER' and profile_user == request.user):

        if profile_user.role == 'TRAINER':
            details_user = TrainerDetail.objects.get(user=int(user_id))
            stats_user = profile_user.get_trainer_customer_list()
        else:
            details_user = CustomerDetail.objects.get(user=int(user_id))
            try:
                stats_user = CustomerBiometric.objects.filter(customer_id=int(user_id))
            except CustomerBiometric.DoesNotExist:
                stats_user = None
    else:    
        messages.error(request, 'Profile does not exist!')
        return redirect('index')        

    return render(request, "workout/profile.html", {
            'profile_user': profile_user, 'details_user': details_user, 'stats_user': stats_user
        })

@login_required
def change_profile(request):
    if request.user.role == 'TRAINER':
        details_obj = TrainerDetail.objects.get(user_id=int(request.user.id))
        details_form_post = TrainerDetailUpdateForm(request.POST, instance=details_obj)
        details_form_re = TrainerDetailUpdateForm(instance=details_obj)
    
    else:
        details_obj = CustomerDetail.objects.get(user_id=int(request.user.id))
        details_form_post = CustomerDetailUpdateForm(request.POST, instance=details_obj)
        details_form_re = CustomerDetailUpdateForm(instance=details_obj)
    
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        
        if user_form.is_valid() and details_form_post.is_valid:
            user_form.save()
            details_form_post.save()
            messages.success(request, 'Your profile was updated!')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, "Invalid input. Please try again!")
            return render(request, 'workout/change_profile.html', {
                'user_form': UserUpdateForm(instance=request.user),
                'details_form': details_form_re
            })
    else:
        return render(request, 'workout/change_profile.html', {
                'user_form': UserUpdateForm(instance=request.user),
                'details_form': details_form_re
            })


@login_required
def add_body_stats(request, customer_id):
    try:
        profile_user = User.objects.get(id=int(customer_id))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
    
    if profile_user.role == 'CUSTOMER':
        if (request.user.role == 'TRAINER' and profile_user in request.user.get_trainer_customer_list()) or (request.user.role == 'CUSTOMER' and profile_user == request.user):
        
            if request.method == "POST":
                form = AddCustomerBiometricForm(request.POST)
                form.instance.customer_id = str(customer_id)
                if form.is_valid:
                    form.save()
                    messages.success(request, 'The record was added!')
                    return redirect('profile', user_id=customer_id)
                else:
                    messages.error(request, "Invalid input. Please try again!")
                    return render(request, 'workout/add_body_stats.html', {
                    'form': AddCustomerBiometricForm(request.POST), 'customer_id': customer_id
                    })
            else:
                return render(request, 'workout/add_body_stats.html', {
                'form': AddCustomerBiometricForm(), 'customer_id': customer_id
                })

        else:    
            messages.error(request, 'Profile does not exist!')
            return HttpResponseRedirect(reverse('profile', args=[customer_id]))
    
    else:    
        messages.error(request, 'Not a customer profile!')
        return HttpResponseRedirect(reverse('profile', args=[customer_id]))



# Workout views

@login_required
def workout_list(request, filter_id):
    
    if request.user.role == 'TRAINER':
        try:
            trainer = request.user
            workout_list = trainer.get_trainer_workout_list()
            customer_range = trainer.get_trainer_customer_list()
            initial_value = {'customer': ''}
        except User.DoesNotExist:
            messages.error(request, 'Customer does not exist!')
            return redirect('index')
    
    elif request.user.role == 'CUSTOMER':
        try:
            customer = request.user
            workout_list = customer.get_workout_list()
            customer_range = User.objects.filter(id=request.user.id)    
            initial_value = {'customer': customer}
        except User.DoesNotExist:
            messages.error(request, 'Customer does not exist!')
            return redirect('index')
    
    else:
        messages.error(request, 'Customer does not exist!')
        return redirect('index')
   
    if request.method == "POST":
        form = AddWorkoutForm(request.POST, customer_range=customer_range)
        if form.is_valid():
            form.save()

        elif request.POST.get('customer'):
            filter_id = request.POST.get('customer')
            return redirect('workout_list',filter_id=filter_id)

        else:
            messages.error(request, "Invalid input. Please try again!")

    if filter_id != 0:
        workout_list = workout_list.filter(customer__id=int(filter_id))

    paginator = Paginator(workout_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'workout/workout_list.html', {
            'workout_list': page_obj,
            'customer_range': customer_range, 
            'new_workout_form': AddWorkoutForm(initial=initial_value, customer_range=customer_range)
            })


@login_required
def workout_view(request, workout_id):
    try:
        workout = Workout.objects.get(id=int(workout_id))
    except Workout.DoesNotExist:
        messages.error(request, 'Workout does not exist!')
        return redirect('index')
    
    if request.user.role == 'CUSTOMER':
        if workout.customer == request.user:
            customer_range = User.objects.filter(id=request.user.id)
        else:
            messages.error(request, 'Workout does not exist!')
            return redirect('workout_list')
            
    elif request.user.role == 'TRAINER':
        if workout.customer in request.user.get_trainer_customer_list():
            customer_range = request.user.get_trainer_customer_list()

        else:
            messages.error(request, 'Workout does not exist!')
            return redirect('workout_list')
    
    else:
        messages.error(request, 'Workout does not exist!')
        return redirect('workout_list')

    if request.method == "POST":
        update_workout_form = AddWorkoutForm(request.POST, instance=workout, customer_range=customer_range)
        add_exercise_form = AddWorkoutExerciseForm(request.POST)
        if update_workout_form.is_valid():
            update_workout_form.save()
        elif add_exercise_form.is_valid():
            add_exercise_form.instance.workout_id = str(workout_id)
            add_exercise_form.instance.sequence_nr = int(len(workout.workout_exercises.all())) + 1
            add_exercise_form.save()
        else:
            messages.error(request, "Invalid input. Please try again!")

    workout_exercises = workout.workout_exercises.order_by('sequence_nr')
    
    try:
        new_workout = Workout.objects.get(id=int(workout_id))
    except Workout.DoesNotExist:
        messages.error(request, 'Workout does not exist!')
        return redirect('index')
    return render(request, 'workout/workout_view.html', {
            'workout': workout,
            'workout_details': AddWorkoutForm(instance=new_workout, customer_range=customer_range),
            'workout_exercises': workout_exercises,
            'new_exercise_form': AddWorkoutExerciseForm(),
            'workout_id': workout_id
            })



def delete_workout_exercise(request, exercise_id):
    try:
        exercise = WorkoutExercise.objects.get(id=int(exercise_id))
    except WorkoutExercise.DoesNotExist:
        return JsonResponse({
            "error": "Index error."
            }, status=400)   
    workout = exercise.workout
    to_update = range(exercise.sequence_nr, workout.count_exercises())
    to_update_dict = {}

    for ex in workout.workout_exercises.all():
        if ex.sequence_nr > exercise.sequence_nr:
            to_update_dict[f'{ex.sequence_nr - 1}'] = f'workout-exercise-{ex.id}'


    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("delete_exercise") is not None:
            if data["delete_exercise"] == "true":
                exercise.delete()
                workout.arrange_sequence()
                
                return JsonResponse({
                        "deleted": f'workout-exercise-{exercise_id}',
                        "update": to_update_dict
                        }, status=201)
            else:
                return JsonResponse({
                    "error": "Wrong input."
                    }, status=400)
        else:
            return JsonResponse({
                "error": "Wrong input."
                }, status=400)
    else:
        return JsonResponse({
            "error": "PUT request required."
            }, status=400)   


def move_up_workout_exercise(request, exercise_id):
    try:
        exercise = WorkoutExercise.objects.get(id=int(exercise_id))
    except WorkoutExercise.DoesNotExist:
        return JsonResponse({
            "error": "Index error."
            }, status=400)   
    workout = exercise.workout
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("move_up") is not None:
            if data["move_up"] == "true":
                try:
                    current_seq = exercise.sequence_nr
                    prev_exercise = workout.workout_exercises.get(sequence_nr=int(current_seq - 1))
                    prev_exercise.sequence_nr = prev_exercise.sequence_nr + 1
                    prev_exercise.save()
                    exercise.sequence_nr = exercise.sequence_nr - 1
                    exercise.save()
                except:
                    return JsonResponse({
                        "moved": "false"
                        }, status=201)  

                return JsonResponse({
                        "moved": "true",
                        "moved_up_ex": f'workout-exercise-{exercise.id}',
                        "moved_up_seq": f'{exercise.sequence_nr}',
                        "moved_down_ex": f'workout-exercise-{prev_exercise.id}',
                        "moved_down_seq": f'{prev_exercise.sequence_nr}',
                        }, status=201)
            else:
                return JsonResponse({
                    "error": "Wrong input."
                    }, status=400)
        else:
            return JsonResponse({
                "error": "Wrong input."
                }, status=400)
    else:
        return JsonResponse({
            "error": "PUT request required."
            }, status=400)   


def move_down_workout_exercise(request, exercise_id):
    try:
        exercise = WorkoutExercise.objects.get(id=int(exercise_id))
    except WorkoutExercise.DoesNotExist:
        return JsonResponse({
            "error": "Index error."
            }, status=400)   
    workout = exercise.workout
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("move_down") is not None:
            if data["move_down"] == "true":
                current_seq = exercise.sequence_nr
                try:
                    next_exercise = workout.workout_exercises.get(sequence_nr=int(current_seq + 1))
                    next_exercise.sequence_nr = next_exercise.sequence_nr - 1
                    next_exercise.save()
                    exercise.sequence_nr = exercise.sequence_nr + 1
                    exercise.save()
                except:
                    return JsonResponse({
                        "moved": "false"
                        }, status=201)   
                
                return JsonResponse({
                        "moved": "true",
                        "moved_down_ex": f'workout-exercise-{exercise.id}',
                        "moved_down_seq": f'{exercise.sequence_nr}',
                        "moved_up_ex": f'workout-exercise-{next_exercise.id}',
                        "moved_up_seq": f'{next_exercise.sequence_nr}',
                        }, status=201)
            else:
                return JsonResponse({
                    "error": "Wrong input."
                    }, status=400)
        else:
            return JsonResponse({
                "error": "Wrong input."
                }, status=400)
    else:
        return JsonResponse({
            "error": "PUT request required."
            }, status=400)   
    


def update_workout_sets(request, exercise_id):
    try:
        exercise = WorkoutExercise.objects.get(id=int(exercise_id))
    except WorkoutExercise.DoesNotExist:
        return JsonResponse({
            "error": "Index error."
            }, status=400)   
    sets = exercise.workout_sets.all()
    if request.method == "PUT":
        data = json.loads(request.body)
        for key in data:
            try:
                reps = data[key]["reps"]
                weight = data[key]["weight"]
                workout_set = sets.get(id=int(key.strip('workout-set-')))
                if reps != "0" or weight != "0":
                    workout_set.update_reps_weight(reps, weight)
                else:
                    workout_set.delete()
            except WorkoutSet.DoesNotExist:
                return JsonResponse({
                    "error": "Index error."
                     }, status=400)   
        updated = exercise.get_all_set_stats()    
        return JsonResponse({
                    "updated": updated
                    }, status=201)       
    else:
        return JsonResponse({
            "error": "PUT request required."
            }, status=400)   


def add_workout_set(request, exercise_id):
    try:
        exercise = WorkoutExercise.objects.get(id=int(exercise_id))
    except WorkoutExercise.DoesNotExist:
        return JsonResponse({
            "error": "Index error."
            }, status=400)   
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("reps") is not None and data.get("reps") is not None:
            new_set = WorkoutSet.new_set(exercise, data["reps"], data["weight"])
            new_set.save()
            updated = exercise.get_all_set_stats()    
            return JsonResponse({
                "updated": updated
                }, status=201)    
        else:
            return JsonResponse({
                "error": f'Wrong input .{data["reps"]} {data["weight"]}'
                }, status=400)
    else:
        return JsonResponse({
            "error": "PUT request required."
            }, status=400)   

    
    