from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email

class Station(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, unique=True)  # Optional: For station codes
    location = models.CharField(max_length=200, blank=True, null=True)  # Optional: to store location details

    def __str__(self):
        return self.name




class Train(models.Model):
    train_number = models.CharField(max_length=20, unique=True)
    train_name = models.CharField(max_length=100)
    origin = models.ForeignKey(Station, related_name='origin_trains', on_delete=models.CASCADE)
    destination = models.ForeignKey(Station, related_name='destination_trains', on_delete=models.CASCADE)
    stations = models.ManyToManyField(Station, through='TrainStation')

    def __str__(self):
        return f"{self.train_number} - {self.train_name}"

class TrainStation(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    stop_number = models.IntegerField()
    platform_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ('train', 'station')  # Ensures each train-stop combination is unique

    def __str__(self):
        return f"{self.train} - {self.station} - Platform: {self.platform_number}"



