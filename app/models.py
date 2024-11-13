from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.


class Genres(models.Model):
    genreName=models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.genreName
    

class MovieInfo(models.Model):
    movieTitle = models.CharField(max_length=100)
    movieReleaseDate = models.DateField()
    movieDescription = models.TextField()
    # image=models.URLField()
    image=models.FileField(upload_to='static/uploads',
                            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    trailerUrl = models.URLField()
    createdAt = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genres)

    def __str__(self):
        return self.movieTitle

