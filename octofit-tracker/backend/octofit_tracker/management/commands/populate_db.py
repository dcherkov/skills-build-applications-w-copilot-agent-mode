from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from djongo import models as djongo_models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for custom collections
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email for users
        db.users.create_index('email', unique=True)

        # Teams
        marvel = {'name': 'Team Marvel', 'description': 'Superheroes from Marvel Universe'}
        dc = {'name': 'Team DC', 'description': 'Superheroes from DC Universe'}
        marvel_id = db.teams.insert_one(marvel).inserted_id
        dc_id = db.teams.insert_one(dc).inserted_id

        # Users
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_id},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Activities
        activities = [
            {'user_id': user_ids[0], 'activity': 'Web swinging', 'duration': 30},
            {'user_id': user_ids[1], 'activity': 'Suit upgrade', 'duration': 45},
            {'user_id': user_ids[2], 'activity': 'Lasso training', 'duration': 60},
            {'user_id': user_ids[3], 'activity': 'Detective work', 'duration': 50},
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {'user_id': user_ids[0], 'workout': 'Wall climbing', 'reps': 20},
            {'user_id': user_ids[1], 'workout': 'Iron suit flight', 'reps': 15},
            {'user_id': user_ids[2], 'workout': 'Amazonian strength', 'reps': 25},
            {'user_id': user_ids[3], 'workout': 'Martial arts', 'reps': 30},
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {'user_id': user_ids[0], 'points': 100},
            {'user_id': user_ids[1], 'points': 90},
            {'user_id': user_ids[2], 'points': 110},
            {'user_id': user_ids[3], 'points': 95},
        ]
        db.leaderboard.insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
