from django import forms
from .models import User, Customer, CustomerDetail, Trainer, TrainerDetail, CustomerBiometric, WorkoutExercise, Workout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.utils.safestring import mark_safe
from datetime import date


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }

        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. <br>',            
        }
        

class RegisterCustomerForm(RegisterUserForm):

    class Meta(RegisterUserForm.Meta):
        model = Customer

    def __init__(self, *args, **kwargs):
        super(RegisterCustomerForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class RegisterTrainerForm(RegisterUserForm):

    class Meta(RegisterUserForm.Meta):
        model = Trainer

    def __init__(self, *args, **kwargs):
        super(RegisterTrainerForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserUpdateForm(UserChangeForm):

    password = None

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'pic')

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'pic': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }

        labels = {
            'pic': 'Profile Picture',
        }


class CustomerDetailUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomerDetail

        fields = ('date_of_birth', 'height', 'trainer')

        widgets = {
            'date_of_birth': forms.DateInput(format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date',
                    'max': date(date.today().year - 12, date.today().month, date.today().day),
                    'min': date(date.today().year - 100, date.today().month, date.today().day)
              }),
              'height': forms.NumberInput(attrs={'class': 'form-control', 'min': '100', 'step': '0.01'}),
              'trainer': forms.Select(attrs={'class': 'form-control'})
        }

        help_texts = {
            'height': 'Please enter your height in cm only.',
        }
   

class AddCustomerBiometricForm(forms.ModelForm):

    class Meta:
        model = CustomerBiometric

        fields = ('body_weight', 'muscle_mass', 'body_fat_p')

        help_texts = {
            'body_weight': 'Please enter your weigth in kg.',
            'muscle_mass': 'Please enter your lean muscle mass in kg.',
            'body_fat_p': 'Please enter your body fat %.'
        }

        widgets = {
            'body_weight': forms.NumberInput(attrs={'class': 'form-control', 'min': '20', 'max': '300', 'step': '0.01'}),
            'muscle_mass': forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'max': '200', 'step': '0.01'}),
            'body_fat_p': forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'max': '100', 'step': '0.01'})

        }


class TrainerDetailUpdateForm(forms.ModelForm):

    class Meta:
        model = TrainerDetail

        fields = ('start_year',)

        def __init__(self):
            self.fields['start_year'] = [1,2]

        widget = {
            'start_year': forms.Select(attrs={'class': 'form-control'}),
        }






class UserPasswordChangeForm(PasswordChangeForm):
    model = User

    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'



class UserPasswordResetForm(PasswordResetForm):
    model = User


class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'



class AddWorkoutExerciseForm(forms.ModelForm):

    class Meta:

        model = WorkoutExercise

        fields = ('exercise',)

        labels = {
            'exercise': 'Add Exercise'
        }

        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-control'}),
        }


class AddWorkoutForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        
        self.customer_range = kwargs.pop('customer_range')
        super(AddWorkoutForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = self.customer_range


    class Meta:

        model = Workout

        fields = ('customer', 'workout_title', 'scheduled_date', 'scheduled_time')

        labels = {
            'customer': 'Customer',
            'workout_title': 'Workout Title',
            'scheduled_date': 'Date',
            'scheduled_time': 'Time'
        }

        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'workout_title': forms.TextInput(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateInput(format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date',
                    'max': date(date.today().year + 1, date.today().month, date.today().day),
                    'min': date(date.today().year - 1, date.today().month, date.today().day)
              }),
              'scheduled_time': forms.TimeInput(
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a time',
                    'type': 'time',
              })
        }

        