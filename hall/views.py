from django.shortcuts import redirect
from django.db.models import Q
from django.views.generic import View, ListView
from django.contrib import messages
from .models import Reservation, Table
from .forms import UserReservedForm
from datetime import datetime


class IndexView(View):

    def get(self, request):
        date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        return redirect('tables-view', date=date)

    def post(self, request):
        date = request.POST['date']
        return redirect('tables-view', date=date)


class TablesView(ListView):
    template_name = 'base.html'
    context_object_name = 'all_table'
    model = Table

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['reserved_table'] = tuple(
            Reservation.objects.filter(
                data_reserved=self.kwargs['date']).values_list('table_id'))
        context['form'] = UserReservedForm()
        context['date'] = self.kwargs['date']
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        number_table = request.POST.get('table')
        data_reserved = request.POST.get('data_reserved')
        if not Reservation.objects.filter(
            Q(data_reserved=data_reserved) & Q(table__number=number_table)
                ).exists():
            user_form = UserReservedForm(request.POST)
            if user_form.is_valid():
                user = user_form.save()
            r = Reservation(user=user, table=Table.objects.get(
                number=number_table), data_reserved=data_reserved)
            r.save()
            messages.add_message(request, messages.INFO, "Cтолик забронирован")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Этот столик забронирован")
        return self.get(request)
