from django.db import models
from django.contrib.auth.models import User
from app.models import MovieInfo
from django.core.validators import FileExtensionValidator
import os

def user_image_upload_to(instance, filename):
    # Define the file path based on the username
    # This will save the image as: static/profile_images/username.jpg (or any other extension)
    file_extension = filename.split('.')[-1]
    return os.path.join('static/profile_images', f'{instance.user.username}.{file_extension}')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio =  models.TextField(blank=True,null=True)
    userImage = models.FileField(upload_to=user_image_upload_to,
                            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','gif'])], blank=True, null=True)
    favorite_movies=models.ManyToManyField(MovieInfo, blank=True, related_name="favorated_by")

    def __str__(self):
        return f"{self.user.username}'s Profile"

class WatchList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.movieTitle}'
    

class Review(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField(default=1)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.movieTitle}"

    class Meta:
        unique_together = ('user', 'movie')
    

# class Favorite(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.movie.movieTitle}"
    
#     class Meta:
#         unique_together = ('user', 'movie')  # Ensures a user can't favorite the same movie twice

