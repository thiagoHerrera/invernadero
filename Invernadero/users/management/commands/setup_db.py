from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Setup database with migrations and superuser'

    def handle(self, *args, **options):
        self.stdout.write('Setting up database...')
        
        # Ejecutar migraciones
        call_command('migrate', '--run-syncdb', verbosity=0)
        
        # Crear superusuario
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@floracore.com', 'floracore2025')
            self.stdout.write('Superuser created')
        
        self.stdout.write('Database setup complete')