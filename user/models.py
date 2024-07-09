import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
import uuid
import jwt
from datetime import datetime,timedelta
from django.conf import settings
def generate_user_id():
    return f"USR-{uuid.uuid4().hex[:8].upper()}"

class User(AbstractUser):
    userId = models.CharField(max_length=32, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=32,unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        if not self.userId:
            self.userId = hashlib.sha256(f"{self.firstName}{self.password}".encode()).hexdigest()[:10]
            self.username = self.email
        super().save(*args, **kwargs)
    @property
    def token(self):
        token = jwt.encode(
            {"username":self.username,"exp":datetime.utcnow() +timedelta(hours=24)},settings.SECRET_KEY,algorithm='HS256'
        )
        return token

class Organisation(models.Model):
    orgId = models.CharField(max_length=255, unique=True,default=generate_user_id)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='organisations')
    id = models.CharField(max_length=32,unique=True,primary_key=True,default=generate_user_id)


    def __str__(self):
        return self.name