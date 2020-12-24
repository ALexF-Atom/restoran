from django import forms

from .models import Client, Reservation


class MyChoiceField(forms.ChoiceField):
    def validate(self, value):
        super(forms.ChoiceField, self).validate(value)


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        labels = {
            'name': 'Ваше имя',
            'phone': 'Номер телефона',
            'email': 'Электронный адрес'
        }


class ReservationForm(forms.ModelForm):
    table_id = forms.CharField(
                widget=forms.HiddenInput())
    table_name = forms.CharField(
                widget=forms.TextInput(attrs={"readonly": True}),
                label="Выбранный столик")

    class Meta:
        model = Reservation
        fields = ('date',)
        widgets = {
            'date': forms.TextInput(attrs={'readonly': True}),
        }
        labels = {
            'date': 'Дата бронирования'
        }

    def save(self, commit=True, **kwargs):
        instance = super().save(commit=False)
        instance.client = kwargs['client']
        instance.hall = kwargs['hall']
        instance.table_id = self.cleaned_data['table_id']
        if commit:
            instance.save()
        return instance
