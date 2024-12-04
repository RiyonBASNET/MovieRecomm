from django.db import models
from django.db.models import Avg
from django.core.validators import FileExtensionValidator, MinValueValidator,MaxValueValidator

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

    rating = models.FloatField(default=0.0)

    def update_rating(self):
        from userspage.models import Review
        # Compute the average rating for this movie
        avg_rating = Review.objects.filter(movie=self).aggregate(Avg('rating'))['rating__avg']
        self.rating = avg_rating if avg_rating is not None else 0.0
        self.save()

    def __str__(self):
        return self.movieTitle

