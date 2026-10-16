from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=64)
    contents = models.TextField()
    writer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'boards'
        verbose_name = '커뮤니티 게시판'
        verbose_name_plural = '커뮤니티 게시판'

class Predict(models.Model):
    first = models.FloatField()
    second = models.FloatField()
    third = models.FloatField()
    fourth = models.FloatField()
