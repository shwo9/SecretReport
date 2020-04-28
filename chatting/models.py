from django.db import models
from helpline.models import Author
from lawyerAccount.models import Lawyer
from datetime import datetime

# Create your models here.
class Chatting_room(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + "번 방"
    


class Chatting(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE,
    null=True)
    room = models.ForeignKey(Chatting_room, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=datetime.now)
    content = models.TextField()

    def __str__(self):
        return self.content