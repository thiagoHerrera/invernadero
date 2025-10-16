from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_configuration'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='riego',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parameters',
            name='ventiladores',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parameters',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
