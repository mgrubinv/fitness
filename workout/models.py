from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


# Main User model

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        TRAINER = "TRAINER", "Trainer"
    
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CUSTOMER)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    pic = models.ImageField(upload_to='pics', null=True, blank=True)

    def get_workout_list(self):
        workout_list =  self.workouts.all()
        return workout_list.order_by('-scheduled_date', '-scheduled_time')
    
    def get_trainer_workout_list(self):
        customers = list(self.customer.values_list('user', flat=True))
        customers.append(str(self.id))
        workout_list = Workout.objects.filter(customer__id__in=customers)
        return workout_list.order_by('-scheduled_date', '-scheduled_time')

    def get_trainer_customer_list(self):
        customers = list(self.customer.values_list('user', flat=True))
        customers.append(str(self.id))
        customer_list = User.objects.filter(id__in=customers)
        return customer_list.order_by('last_name')

    def get_user_workout_count(self):
        return  len(self.workouts.all())
    
    def get_user_last_workout(self):
        return self.workouts.filter(scheduled_date__lt=datetime.today()).order_by('-scheduled_date').first()

    def get_user_next_workout(self):
        return self.workouts.filter(scheduled_date__gte=datetime.today()).order_by('scheduled_date').first()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Trainer role proxy class inheriting from User, including TrainerManager and TrainerDetail classes

class TrainerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.TRAINER)    

class Trainer(User):
    trainer = TrainerManager()
    
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.TRAINER
        return super().save(*args, **kwargs)

@receiver(post_save, sender=Trainer)
def create_user_details(sender, instance, created, **kwargs):
    if created and instance.role == "TRAINER":
        TrainerDetail.objects.create(user=instance)

class TrainerDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_year=models.IntegerField(null=True, blank=True)

    def update_trainerdetails(self, start_year):
        if start_year:
            self.start_year = start_year
        self.save()

# Customer role proxy class inheriting from User, including CustomerManager, CustomerDetail and CustomerBiometric classes

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.CUSTOMER)

class Customer(User):
    customer = CustomerManager()
    
    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.CUSTOMER
        return super().save(*args, **kwargs)

@receiver(post_save, sender=Customer)
def create_user_details(sender, instance, created, **kwargs):
    if created and instance.role == "CUSTOMER":
        CustomerDetail.objects.create(user=instance)

class CustomerDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #customer = models.ForeignKey(Customer,on_delete=models.CASCADE, related_name="trainer", null=True)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE, related_name="customer", null=True)
    date_of_birth = models.DateField(auto_now=False, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    def update_customerdetails(self, trainer_id, date_of_birth, height):
        if trainer_id:
            try:
                trainer = Trainer.objects.get(id=str(trainer_id))
            except Trainer.DoesNotExist:
                pass
            self.trainer = trainer

        if date_of_birth:
            self.date_of_birth = date_of_birth

        if height:
            self.height = height

        self.save()



class CustomerBiometric(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="body_stats")
    created_on = models.DateTimeField(auto_now_add=True)
    body_weight = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True)
    body_fat_p = models.FloatField(null=True, blank=True, verbose_name='Body fat')


# The MuscleGroup an Execise trains

class MuscleGroup(models.Model):
    muscle = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.muscle}"


# An Exercise that can be part of a Workout

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=50)
    muscle = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, related_name="exercises")

    def __str__(self):
        return f"{self.exercise_name}"


# A Workout schedule for a specific user and time

class Workout(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)
    workout_title = models.CharField(max_length=50, default='Workout')

    def arrange_sequence(self):
        workout_exercises = self.workout_exercises.order_by('sequence_nr') 
        for r in range(len(workout_exercises)):
            workout_exercises[r].sequence_nr = r + 1
            workout_exercises[r].save()
    
    def count_exercises(self):
        return len(self.workout_exercises.all())


# An Exercise being part of a specific Workout

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="workout_exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="workout_exercises")
    sequence_nr = models.IntegerField()
    
    def get_all_set_stats(self):
        output = {}
        for set in self.workout_sets.all():
            sub = {}
            sub["reps"] = set.reps
            sub["weight"] = set.weight
            output[f'workout-set-{set.id}'] = sub
        return output


# A Set tracking repetitions, weight and number of sets for a specific WorkoutExercise

class WorkoutSet(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name="workout_sets")
    reps = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    @classmethod
    def new_set(cls, workout_exercise, reps, weight):
        new_set = cls(workout_exercise=workout_exercise, reps=reps, weight=weight)
        return new_set

    def update_reps_weight(self, reps, weight):
        self.reps = reps
        self.weight = weight
        self.save()
