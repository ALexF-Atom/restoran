from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic.edit import BaseUpdateView
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from hall.models import Restoran, Hall, Table, Struct
from .forms import HallForm

import json


@method_decorator(login_required(login_url='/radmin/staff/login/'), name='dispatch')
class IndexView(ListView):
    template_name = 'radmin/index.html'
    model = Restoran
    context_object_name = 'restorans'

    def get_queryset(self):
        user = self.request.user
        print("user", user)
        q = self.model.objects.all()
        return q


class RestoranDetailView(DetailView):
    # отдавать только разрешенные для пользователя
    model = Restoran
    template_name = 'radmin/restoran.html'
    context_object_name = 'restoran'
    slug_field = 'name'
    slug_url_kwarg = 'name'


class CreateSchemeView(CreateView):
    model = Hall
    template_name = 'radmin/create_scheme.html'
    form_class = HallForm

    def get_form(self):
        form = super().get_form()
        form.fields['restoran'].initial = Restoran.objects.get(
            name=self.kwargs['name'])
        form.fields['restoran'].widget.attrs['disabled'] = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tables'] = {tab.id: tab.json() for tab in Table.objects.all()}
        return context

    @property
    def data_xhr(self, *args, **kwargs):
        return json.loads(self.request.body.decode('utf-8'))

    def post(self, request, *args, **kwargs):
        tables = tuple(table for table in self.data_xhr['tables'])
        hall = self.model.objects.create(**self.data_xhr['hall'])
        Struct.objects.bulk_create(
            [Struct(hall_id=hall.id, **t) for t in tables])
        return JsonResponse({'url': reverse(
            'radmin_restoran', args=[self.data_xhr['hall']['restoran_id']])})


class UpdateSchemeView(CreateSchemeView, BaseUpdateView):
    template_name = 'radmin/update_scheme.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_form(self):
        form = super(CreateView, self).get_form()
        form.fields['width'].widget.attrs['disabled'] = True
        form.fields['length'].widget.attrs['disabled'] = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables_scheme'] = [s.json()
                                    for s in self.object.hall_struct.all()]
        return context

    def post(self, request, *args, **kwargs):
        tables = [table for table in self.data_xhr['tables']]
        hall = self.get_object()
        self.get_queryset().filter(pk=hall.id).update(
                                                    **self.data_xhr['hall'])
        for t in tables:
            Struct.objects.update_or_create(
                id=t.pop('struct_id', None),
                defaults={'hall': hall, **t})

        return JsonResponse({'url': reverse(
            'radmin_restoran', args=[self.data_xhr['hall']['restoran_id']])})


class DeleteSchemeView(DeleteView):
    model = Hall
    template_name = 'radmin/hall_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse('radmin_restoran', args=[self.object.restoran.id])
