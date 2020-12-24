from django import forms
from hall.models import Hall, Table


class HallForm(forms.ModelForm):
    tables = forms.ModelChoiceField(label='Доступные столы',
                                    queryset=Table.objects.all())

    class Meta:
        model = Hall
        fields = '__all__'
        widgets = {
            'restoran': forms.Select(attrs={'disabled': True}),
            'slug': forms.TextInput(attrs={'type': 'hidden'}),
        }
        labels = {
            'restoran': "Название ресторана"
        }
