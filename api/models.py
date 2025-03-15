from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Product(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(product=self)
        return len(ratings)
    
    def avg_rating(self):
        sum_ratings = 0
        ratings = Rating.objects.filter(product=self)  

        for rating in ratings:
            sum_ratings += rating.stars

        if len(ratings) > 0:
            return sum_ratings / len(ratings)
        else:
            return 0

    def __str__(self):
        return self.title


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'product'),)  
        indexes = [
            models.Index(fields=['user', 'product']),
        ]