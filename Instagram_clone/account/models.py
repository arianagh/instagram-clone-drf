from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    age = models.CharField(max_length=50, default='', blank=True)
    bio = models.CharField(max_length=100, default='', null=True, blank=True)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)

    class Meta:
        verbose_name = 'Profile'

    def __str__(self):
        return f'{self.user}'


class FollowerTable(models.Model):
    '''
    ba obj haye in mishe followere on user o grft
    ba obj khode user mishe ba related name following esho grft
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="followers_table", on_delete=models.CASCADE)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", through="FollowerUser")

    def __str__(self):
        return f'{self.user}'

    def follower_count(self):
        if self.follower.count():
            return self.follower.count()
        return 0


class FollowerUser(models.Model):
    Follow_STATUS = [("a", "Accept"), ("p", "Pending")]
    following = models.ForeignKey(FollowerTable, related_name="followers",
                                  on_delete=models.CASCADE)  # on kesi ke dare follow mishe
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followings',
                                 on_delete=models.CASCADE)
    status = models.CharField(choices=Follow_STATUS, max_length=1)

    def __str__(self):
        return f"{self.following.user} - {self.follower}"


