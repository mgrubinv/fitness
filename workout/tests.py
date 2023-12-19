from django.test import Client, TestCase
from datetime import datetime, timedelta, date
from django.urls import reverse

from .models import User, Trainer, TrainerDetail, Customer, CustomerDetail, CustomerBiometric, MuscleGroup, Exercise, Workout, WorkoutExercise, WorkoutSet

class WorkoutTestCase(TestCase):

    def setUp(self):

        trainer_n = Trainer.objects.create_user(username="TestTrainer", first_name="Test", last_name="Trainer", email="testtrainer@example.com", password="tt", gender="M")
        trainerDet = TrainerDetail.objects.get(user=trainer_n)
        trainerDet.update_trainerdetails(start_year=2001)
        customer_n = Customer.objects.create_user(username="TestCustomer", first_name="Test", last_name="Customer", email="testcustomer@example.com", password="tc", gender="F")
        customerDet = CustomerDetail.objects.get(user=customer_n)
        customerDet.update_customerdetails(trainer_id=str(Trainer.objects.get(username="TestTrainer").id), date_of_birth=date(2023, 12, 30), height=160)
        customerBio = CustomerBiometric.objects.create(customer=customer_n, body_weight=60, muscle_mass=8, body_fat_p=15)

        muscle_n = MuscleGroup.objects.create(muscle="Calves")
        exercise1 = Exercise.objects.create(exercise_name="Calf Raise", muscle=muscle_n)
        exercise2 = Exercise.objects.create(exercise_name="Calf Stretch", muscle=muscle_n)
        workout_n1 = Workout.objects.create(customer=customer_n, scheduled_date=datetime.today().date() + timedelta(days=2))
        workout_n2 = Workout.objects.create(customer=trainer_n, scheduled_date=datetime.today().date())
        workout_n3 = Workout.objects.create(customer=customer_n, scheduled_date=datetime.today().date() - timedelta(days=2))
        workout_ex1 = WorkoutExercise.objects.create(workout=workout_n1, exercise=exercise1, sequence_nr=1)
        workout_ex2 = WorkoutExercise.objects.create(workout=workout_n1, exercise=exercise2, sequence_nr=3)

        workoutset1 = WorkoutSet.objects.create(workout_exercise=workout_ex1, reps=8, weight=10)
        workoutset2 = WorkoutSet.objects.create(workout_exercise=workout_ex1, reps=8, weight=10)
        workoutset3 = WorkoutSet.objects.create(workout_exercise=workout_ex1, reps=8, weight=10)

    def test_trainer_role(self):
        t = Trainer.objects.get(username="TestTrainer")
        self.assertEqual(t.role, "TRAINER")

    def test_customer_role(self):
        c = Customer.objects.get(username="TestCustomer")
        self.assertEqual(c.role, "CUSTOMER")

    def test_update_trainerdetails(self):
        t = Trainer.objects.get(username="TestTrainer")
        self.assertEqual(t.trainerdetail.start_year, 2001)

    def test_update_customerdetails(self):
        c = Customer.objects.get(username="TestCustomer")
        self.assertEqual(c.customerdetail.height, 160)

    def test_get_workout_list(self):
        c = User.objects.get(username="TestCustomer")
        self.assertEqual(len(c.get_workout_list()), 2)

    def test_get_trainer_workout_list(self):
        t = User.objects.get(username="TestTrainer")
        self.assertEqual(len(t.get_trainer_workout_list()), 3)

    def test_get_trainer_customer_list(self):
        t = User.objects.get(username="TestTrainer")
        self.assertEqual(t.get_trainer_customer_list().get(username="TestCustomer").last_name, "Customer")

    def test_get_user_workout_count(self):
        c = User.objects.get(username="TestCustomer")
        self.assertEqual(c.get_user_workout_count(), 2)
    
    def test_get_user_last_workout(self):
        c = User.objects.get(username="TestCustomer")
        self.assertEqual(c.get_user_last_workout().scheduled_date, datetime.today().date() - timedelta(days=2))

    def test_get_user_next_workout(self):
        c = User.objects.get(username="TestCustomer")
        self.assertEqual(c.get_user_next_workout().scheduled_date, datetime.today().date() + timedelta(days=2))
    
    def test_workout_arrange_sequence(self):
        w = Workout.objects.get(scheduled_date=datetime.today().date() + timedelta(days=2))
        self.assertEqual(w.workout_exercises.last().sequence_nr, 3)
        w.arrange_sequence()
        self.assertEqual(w.workout_exercises.last().sequence_nr, 2)

    def test_count_exercises(self):
        w = Workout.objects.get(scheduled_date=datetime.today().date() + timedelta(days=2))
        self.assertEqual(w.count_exercises(), 2)

    def test_get_all_stats_workoutexercise(self):
        we = Workout.objects.get(scheduled_date=datetime.today().date() + timedelta(days=2)).workout_exercises.first()
        self.assertEqual(len(we.get_all_set_stats()), 3)

    def test_rendering_workout_list_trainer(self):
        c = Client()
        c.login(username='TestTrainer', password='tt')
        response = c.get(reverse('workout_list', kwargs={'filter_id':0}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["workout_list"].object_list), 0)

    def test_rendering_workout_list_not_authenticated(self):
        c = Client()
        response = c.get(reverse('workout_list', kwargs={'filter_id':0}))
        self.assertEqual(response["Location"], '/login?next=/workout-list/0')
        self.assertEqual(response.status_code, 302)

    def test_rendering_workout_list_trainer(self):
        c = Client()
        c.login(username='TestTrainer', password='tt')
        response = c.get(reverse('workout_view', kwargs={'workout_id':1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["workout_exercises"]), 2)
