from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='equipment_images/', blank=True, null=True)

    status_choices = [
        ('libre', 'Libre'),
        ('occupé', 'Occupé'),
        ('réservé', 'Réservé'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='libre')

    reservation_datetime = models.DateTimeField(blank=True, null=True)
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    category = models.CharField(
        max_length=50, 
        choices=[('cardio', 'Cardio'), ('musculation', 'Musculation')]
    )

    def __str__(self):
        return self.name

    def clean(self):
        if self.status == 'réservé' and not (self.reserved_by and self.reservation_datetime):
            raise ValidationError("Une réservation nécessite un utilisateur et une date/heure")
        if self.status != 'réservé' and (self.reserved_by or self.reservation_datetime):
            self.reserved_by = None
            self.reservation_datetime = None

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def is_available(self):
        if self.status == 'libre':
            return True
        elif self.status == 'réservé' and self.reservation_datetime:
            if self.reservation_datetime < timezone.now():
                self.status = 'libre'
                self.reserved_by = None
                self.reservation_datetime = None
                self.save()
                return True
        return False

    def get_reservation_info(self):
        """Retourne les informations de réservation formatées"""
        if self.status == 'réservé' and self.reserved_by and self.reservation_datetime:
            return {
                'user': self.reserved_by.username,
                'date': self.reservation_datetime.strftime('%d/%m/%Y'),
                'time': self.reservation_datetime.strftime('%H:%M'),
            }
        return None
    
from django.db import models
from django.utils import timezone

class Athlete(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('O', 'Autre'),
    ]
    current_equipment = models.ForeignKey(
        'Equipment', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='users'
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    equipment_reservation_time = models.DateTimeField(null=True, blank=True)
    objective = models.CharField(max_length=100, blank=True)
    is_using_machine = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    email = models.EmailField(null=True, blank=True)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.current_equipment:
            if self.is_using_machine:
                self.current_equipment.status = 'occupé'
                self.current_equipment.save()
            else:
                self.current_equipment.status = 'libre'
                self.current_equipment.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.current_equipment:
            self.current_equipment.status = 'libre'
            self.current_equipment.save()
        super().delete(*args, **kwargs)