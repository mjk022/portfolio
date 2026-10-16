from django.db import models

class User(models.Model):  # 1
    username = models.CharField(max_length=64)
    useremail = models.EmailField(max_length=64)
    password = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): # 2
        return self.username

    class Meta: # 3
        db_table = 'community_user'
        verbose_name = '커뮤니티 사용자'
        verbose_name_plural = '커뮤니티 사용자'


class Predict(models.Model):
    first = models.FloatField()
    second = models.FloatField()
    third = models.FloatField()
    fourth = models.FloatField()
