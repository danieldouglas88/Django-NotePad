from django.db import models

# Create your models here.
class NotePad(models.Model):
    comment = models.TextField()
    initialdate = models.DateField(auto_now=True, editable=False)
    update_date = models.DateField(null = True, blank = True, editable=False)
    username = models.CharField(max_length = 255, editable=False)
    
    def __str__(self):
        return self.comment
    
    class Meta:
        db_table = 'notepad'
        verbose_name_plural = 'notepads'
    