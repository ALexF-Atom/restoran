from django.views.generic import ListView, DetailView
from django.db.models import F, Case, When, Value, Exists, CharField, OuterRef
from django.contrib import messages

from .models import Restoran, Hall, Table
from reserver.models import Reservation
from reserver.forms import ClientForm, ReservationForm

from django.http import Http404


def print_html(*args, **kwargs):
    raise Http404(args, kwargs)


class IndexView(ListView):
    template_name = 'hall/restorans.html'
    model = Restoran
    context_object_name = 'restorans'


class RestoranDetailView(DetailView):
    model = Restoran
    template_name = 'hall/restoran.html'
    context_object_name = 'restoran'
    slug_field = 'name'
    slug_url_kwarg = 'name'


class HallDetailView(DetailView):
    model = Hall
    template_name = 'hall/hall.html'
    context_object_name = 'hall'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    client_form_class = ClientForm
    reserver_form_class = ReservationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hall = self.object
        qs_reserv = Reservation.objects.filter(
            table=OuterRef('id'), date=self.kwargs['date'])
        tables = tuple(hall.hall_struct.select_related('table')
                       .annotate(
                        reserved=Case(When(Exists(qs_reserv),
                                      then=Value('busy')),
                                      default=Value('free'),
                                      output_field=CharField()),
                        shape=F('table__shape'),
                        width=F('table__width'),
                        height=F('table__length'))
                       .values('id', 'name_table', 'position_x',
                               'position_y', 'seats', 'shape',
                               'width', 'height', 'reserved')
                       .distinct())

        context['js_tables'] = tables
        context['date'] = self.kwargs['date']
        context['js_board'] = {'width': hall.width, 'height': hall.length}
        context['js_shape'] = {id: value for id, value in Table.SHAPE}

        return context

    def post(self, request, *args, **kwargs):
        post_data = request.POST or None
        client_form = self.client_form_class(post_data, prefix='client')
        reserv_form = self.reserver_form_class(post_data, prefix='reserver')
        if client_form.is_valid() and reserv_form.is_valid():
            reserv_form.save(client=client_form.save(), hall=self.object)
            messages.add_message(request, messages.INFO,
                                 "Столик забронирован. Ждем Вас!")
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        client_form = self.client_form_class(prefix='client')
        reserv_form = self.reserver_form_class(prefix='reserver')
        context = self.get_context_data(client_form=client_form,
                                        reserv_form=reserv_form)
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
