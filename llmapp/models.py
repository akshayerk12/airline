from django.db import models

# Create your models here.
class Airline(models.Model):
    airline=models.CharField(max_length=50)
    From_location=models.CharField(max_length=20)
    To_location=models.CharField(max_length=20)
    seat_type=models.CharField(max_length=10)
    seat_comfort=models.IntegerField()
    cabin_crew=models.IntegerField()
    ground_service=models.IntegerField()
    review=models.TextField()
    result=models.CharField(max_length=5)

    def __str__(self):
        return self.airline
