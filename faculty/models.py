from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    image = models.ImageField(upload_to='faculty/', null=True)
    phone = models.IntegerField()
    address = models.TextField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name
