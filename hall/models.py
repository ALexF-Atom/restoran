from django.db import models
from django.urls import reverse
from datetime import date


class IntervalField(models.FloatField):
    def __init__(self, verbose_name=None, min_value=None,
                 max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.FloatField.__init__(self, verbose_name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"min_value": self.min_value, "max_value": self.max_value}
        defaults.update(kwargs)
        return super(IntervalField, self).formfield(**defaults)


class Restoran(models.Model):
    name = models.CharField(
        verbose_name="Название ресторана", blank=False, max_length=100,
        unique=True)

    class Meta:
        verbose_name = 'restoran'
        verbose_name_plural = 'restorans'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restoran', args=[self.name])


class Table(models.Model):
    SHAPE = (
            (0, 'ellipse'),
            (1, 'rectangle'),
    )
    name = models.CharField(
        verbose_name="Название стола", blank=False, max_length=100)
    width = models.PositiveSmallIntegerField(
            verbose_name="Длина стола по X", blank=False, null=False)
    length = models.PositiveSmallIntegerField(
            verbose_name="Длина стола по Y", blank=False, null=False)
    shape = models.PositiveSmallIntegerField(
            verbose_name="Форма стола", choices=SHAPE)
    max_seats = models.PositiveSmallIntegerField(
        verbose_name="Количество мест")

    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
        constraints = (models.UniqueConstraint(
            fields=['name', 'width', 'length'],
            name='inique_table'),)

    def __str__(self):
        return self.name

    def json(self):
        context = self.__dict__
        context['shape'] = self.get_shape_display()
        del context['_state']
        return context


class Hall(models.Model):
    restoran = models.ForeignKey(
        Restoran, on_delete=models.CASCADE, related_name="halls")
    name = models.CharField(
        verbose_name="Название зала", blank=False, max_length=100)
    width = models.CharField(verbose_name="Длина по X",
                             blank=False, max_length=100)
    length = models.CharField(verbose_name="Длина по Y",
                              blank=False, max_length=100)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Hall'
        verbose_name_plural = 'Halls'
        constraints = (models.UniqueConstraint(
            fields=['restoran', 'name'],
            name='unique_hall'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hall', args=[self.slug, str(date.today())])

    def get_update_url(self):
        return reverse(
            'update_scheme', args=[self.slug])

    def get_delete_url(self):
        return reverse('delete', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = f'{self.restoran.name}-{self.name}'
        super().save(*args, **kwargs)


class Struct(models.Model):
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name="hall_struct")
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="table_struct")
    name_table = models.CharField(
        verbose_name="Название стола", blank=False, max_length=100)
    position_x = IntervalField(
        verbose_name="Позиция по X (%)", min_value=0, max_value=100,
        db_index=False)
    position_y = IntervalField(
        verbose_name="Позиция по Y (%)", min_value=0, max_value=100,
        db_index=False)
    rotate = IntervalField(
        verbose_name="Поворот в градусах", min_value=-360, max_value=360,
        db_index=False, default=0)
    seats = models.PositiveSmallIntegerField(
        verbose_name="Количество мест", blank=True, null=True)

    class Meta:
        verbose_name = 'Struct'
        verbose_name_plural = 'Structs'
        constraints = (models.UniqueConstraint(
                fields=['table', 'name_table', 'position_x', 'position_y'],
                name='unique_table_scheme'),)

    def __str__(self):
        return self.name_table

    def json(self):
        context = self.table.json()
        context.update(self.__dict__)
        del context['_state']
        return context
