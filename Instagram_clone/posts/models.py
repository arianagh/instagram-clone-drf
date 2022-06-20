from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Posts(models.Model):
    caption = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='posts/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likers", blank=True, symmetrical=False)

    def __str__(self):
        return f'post{self.pk}---{self.creator}'

    def likes_count(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='authors', on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='posts_comments', on_delete=models.CASCADE)
    created_time = models.DateField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.pk}---{self.author}'
