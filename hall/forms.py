from django import forms
from .models import Reservation, UserReserved

class UserReservedForm(forms.ModelForm):
    class Meta:
        model = UserReserved
        fields = '__all__'
        labels = {
         'name': "Ваше имя",
         'email':"Ваш email",
         }
