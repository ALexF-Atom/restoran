from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation, Table, UserReserved
from .forms import UserReservedForm
from datetime import datetime
import json

def index(request):
    print('index')
    date = datetime.strftime(datetime.now(),'%Y-%m-%d')
    if request.method == 'POST':
        date=request.POST['date']
    return redirect(tables_view, date)

def tables_view(request, date):
    user_form = UserReservedForm()
    all_table = Table.objects.all()
    if request.method == 'POST':
        number_table = request.POST.get('table')
        data_reserved = request.POST.get('data_reserved')
        if not Reservation.objects.filter(data_reserved=data_reserved).filter(table__number=number_table).exists():
            user_form = UserReservedForm(request.POST)
            if user_form.is_valid():
                user = user_form.save()
            r = Reservation(user=user, table=Table.objects.get(number=number_table), data_reserved=data_reserved)
            r.save()
            messages.add_message(request, messages.INFO, "Cтолик забронирован")
        else:
            messages.add_message(request, messages.ERROR, "Этот столик забронирован")
    reserved_table = tuple(Reservation.objects.filter(data_reserved=date).values_list('table_id'))
    context = {'date':date, 'all_table':all_table, 'reserved_table':reserved_table, 'form':user_form}
    return render(request, 'base.html', context )
