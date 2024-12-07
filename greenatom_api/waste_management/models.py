from django.db import models


class Storage(models.Model):
    name = models.CharField(max_length=100)
    plastic_current = models.IntegerField(default=0)
    plastic_max = models.IntegerField(default=0)
    glass_current = models.IntegerField(default=0)
    glass_max = models.IntegerField(default=0)
    bio_waste_current = models.IntegerField(default=0)
    bio_waste_max = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Factory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FromFactoryToStorageDistance(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='storage_distances')
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='factory_distances')
    distance = models.IntegerField(default=0)

    def __str__(self):
        return f'Distance from {self.factory.name} to {self.storage.name}: {self.distance}'