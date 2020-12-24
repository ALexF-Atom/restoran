from django.contrib import admin
from hall.models import Table, Restoran, Hall, Struct
from .models import Admin

admin.site.register(Restoran)
admin.site.register(Hall)
admin.site.register(Admin)


@admin.register(Struct)
class StructAdmin(admin.ModelAdmin):
    model = Struct
    list_display = ('name_table', 'hall')
    list_filter = ('hall',)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    model = Table
    list_display = ('name', 'width', 'length', 'max_seats', 'shape')
