from django.core.management.base import BaseCommand
from blog.models import Equipment, Athlete

class Command(BaseCommand):
    help = 'Populates the database with initial gym equipment and athletes'

    def handle(self, *args, **kwargs):
        # Create Equipment
        equipments = [
            Equipment(name='Tapis Roulant 1', status='libre', category='Cardio'),
            Equipment(name='Tapis Roulant 2', status='libre', category='Cardio'),
            Equipment(name='Vélo Elliptique', status='libre', category='Cardio'),
            Equipment('Machine à Pectoraux', status='libre', category='Musculation'),
            Equipment(name='Machine à Quadriceps', status='libre', category='Musculation'),
            Equipment(name='Machine à Abdos', status='libre', category='Musculation'),
            Equipment(name='Rack de Squat', status='libre', category='Musculation'),
            Equipment(name='Banc de Musculation', status='libre', category='Musculation'),
        ]
        Equipment.objects.bulk_create(equipments)

        # Create Athletes
        athletes = [
            Athlete(name='Jean Dupont', fitness_goal='Perte de poids'),
            Athlete(name='Marie Martin', fitness_goal='Musculation'),
            Athlete(name='Pierre Durand', fitness_goal='Cardio'),
            Athlete(name='Sophie Lefebvre', fitness_goal='Fitness général'),
        ]
        Athlete.objects.bulk_create(athletes)

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))