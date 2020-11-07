from django.db import models


class ProcentField(models.IntegerField):

    def __init__(self, verbose_name=None, name=None,
                 min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"min_value": self.min_value, "max_value": self.max_value}
        defaults.update(kwargs)
        return super(ProcentField, self).formfield(**defaults)


class Table(models.Model):

    SHAPES = (
        (0, "ellipse"), (1, "rectangle")
    )

    number = models.CharField(verbose_name="Номер", unique=True, max_length=10)
    y_coordinate = ProcentField(
        verbose_name="Расположение по вертикали", min_value=0, max_value=100)
    x_coordinate = ProcentField(
        verbose_name="Расположение по горизонтали", min_value=0, max_value=100)
    width = ProcentField(verbose_name="Размер по горизонтали",
                         min_value=1, max_value=100)
    length = ProcentField(verbose_name="Размер по вертикали",
                          min_value=1, max_value=100)
    # get_shape_display
    shape = models.SmallIntegerField(
        verbose_name="Форма", default=1, choices=SHAPES)
    seats = models.IntegerField(verbose_name="Количество мест")

    class Meta:
        ordering = ["y_coordinate", "x_coordinate"]
        verbose_name = "Стол"
        verbose_name_plural = "Столы"

    def __str__(self):
        return f"{self.number}"

    def get_style_css(self):
        return (f"display: inline-block; width:{self.width}%; height:{self.length}%;")


class UserReserved(models.Model):

    name = models.CharField(verbose_name="Имя", max_length=100)
    email = models.EmailField(verbose_name="Почта",)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return " ".join(("Клиент", self.name, self.email))


class Reservation(models.Model):
    class Meta:
        unique_together = ['table', 'data_reserved']

    user = models.ForeignKey(
        'UserReserved', on_delete=models.CASCADE, related_name='reserved')
    table = models.ForeignKey(
        'Table',  on_delete=models.CASCADE, related_name='reserved')
    data_reserved = models.DateField()

    def __str__(self):
        return f'бронь столика {self.table} {self.data_reserved} на имя {self.user.name}'
