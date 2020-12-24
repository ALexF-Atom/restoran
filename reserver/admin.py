from django.contrib import admin
from .models import Client, Reservation


admin.site.register(Client)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_filter = ('date', 'hall')
    list_display = ('hall', 'table', 'date', 'client')
