# Generated by Django 3.1.3 on 2020-11-04 08:42

from django.db import migrations, models
import django.db.models.deletion
import hall.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField(unique=True, verbose_name='Номер')),
                ('y_coordinate', hall.models.ProcentField(verbose_name='Расположение по вертикали')),
                ('x_coordinate', hall.models.ProcentField(verbose_name='Расположение по горизонтали')),
                ('width', hall.models.ProcentField(verbose_name='Размер по горизонтали')),
                ('length', hall.models.ProcentField(verbose_name='Размер по вертикали')),
                ('shape', models.SmallIntegerField(choices=[(0, 'ellipse'), (1, 'rectangle')], default=1, verbose_name='Форма')),
                ('seats', models.IntegerField(verbose_name='Количество мест')),
            ],
            options={
                'verbose_name': 'Стол',
                'verbose_name_plural': 'Столы',
                'ordering': ['y_coordinate', 'x_coordinate'],
            },
        ),
        migrations.CreateModel(
            name='UserReserved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_reserved', models.DateField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved', to='hall.table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved', to='hall.userreserved')),
            ],
        ),
    ]