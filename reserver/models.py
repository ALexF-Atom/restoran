from django.db import models
from hall.models import Struct, Hall


class Client(models.Model):
    name = models.CharField(
        verbose_name="Имя Клиентв", blank=False, max_length=100)
    email = models.CharField(
        verbose_name="Почта Клиента", blank=False, max_length=100)
    phone = models.CharField(
        verbose_name="Телефон Клиента", blank=False, max_length=100)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{self.name}-{self.phone}'


class Reservation(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    table = models.ForeignKey(
        Struct, on_delete=models.CASCADE, related_name="reserved_table",)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="reserved_client",)
    date = models.DateField(verbose_name="Дата бронирования")

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        constraints = (models.UniqueConstraint(
            fields=['table', 'client', 'date'],
            name='unique_reserv'),)

    def __str__(self):
        return f'{self.client.name}-{self.date}-{self.table}'
