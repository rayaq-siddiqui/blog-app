from django.db import models


# Create your models here.
class Post(models.Model):
    # models datafields

    title = models.CharField(max_length=200)

    # ForeignKey allows there to be a many to one relationship
    # ex: an author can have many blogs, but a blog can have only one author
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )

    body = models.TextField()


    # models naming characteristic
    def __str__(self):
        return self.title
