from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    FILE_TYPE_CHOICES = [
        ('Photo', 'Photo'),
        ('Video', 'Video'),
    ]

    LOCATION_CHOICES = [
        ('Off-campus', 'Off-campus'),
        ('On-campus', 'On-campus'),
    ]

    EVENT_TYPE_CHOICES = [
        ('Award', 'Award'),
        ('Seminar', 'Seminar'),
        ('Performance', 'Performance'),
        ('Conference', 'Conference'),
        ('Speech', 'Speech'),
        ('Pickup', 'Pickup'),
        ('Cultural', 'Cultural'),
        ('Cultural Experience', 'Cultural Experience'),
        ('Booth', 'Booth'),
        ('Corporate Trip', 'Corporate Trip'),
        ('Others', 'Others'),
    ]

    CAMERA_SHOT_CHOICES = [
        ('Long Shot', 'Long Shot'),
        ('Close Shot', 'Close Shot'),
        ('Medium Shot', 'Medium Shot'),
        (None, 'null'),
    ]

    CAMERA_ANGLE_CHOICES = [
        ('Back', 'Back'),
        ('Front', 'Front'),
        ('Side', 'Side'),
        ('High-angle', 'High-angle'),
        ('Low-angle', 'Low-angle'),
        (None, 'null'),
    ]

    ATMOSPHERE_CHOICES = [
        ('Not recognized', 'Not recognized'),
        ('Positive', 'Positive'),
        ('Joyful', 'Joyful'),
        ('Serious', 'Serious'),
        ('Interactive', 'Interactive'),
        (None, 'null'),
    ]

    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Chinese', 'Chinese'),
        ('Other', 'Other'),
    ]

    RACE_CHOICES = [
        ('IBA', 'IBA'),
        ('IPAI', 'IPAI'),
        ('ITH', 'ITH'),
        ('Other', 'Other'),
    ]

    activity = models.CharField(max_length=200)  # Пользователь может ввести любое название
    description = models.TextField()
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='Photo')
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    camera_shot = models.CharField(max_length=20, choices=CAMERA_SHOT_CHOICES, blank=True, null=True)
    camera_angle = models.CharField(max_length=20, choices=CAMERA_ANGLE_CHOICES, blank=True, null=True)
    atmosphere = models.CharField(max_length=20, choices=ATMOSPHERE_CHOICES, blank=True, null=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='English')
    race = models.CharField(max_length=10, choices=RACE_CHOICES, default='Other')
    date = models.DateField(default='2024-01-01')  # Для указания даты через календарь
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_photos', default=1)


    def __str__(self):
        return self.activity
