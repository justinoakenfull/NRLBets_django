from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    credits = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    def __str__(self):
        return self.user.username
    def get_credits(self):
        return self.credits
    def add_credits(self, amount):
        if amount > 0:
            self.credits += amount
        self.save()
    def remove_credits(self, amount):
        if amount > 0:
            if self.credits - amount < 0:
                self.credits = 0
            else:
                self.credits -= amount
        self.save()
    def set_credits(self, amount):
        if amount > 0:
            self.credits = amount
        self.save()
    