from django.db import models
from django.contrib.auth.models import User

from hall.models import Hall


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hall = models.ManyToManyField(Hall, related_name="admin")

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def __str__(self):
        return f'{self.user.name}-{self.hall.slug}'

    def is_admin(self, hall):
        return hall.slug in self.hall.all()
