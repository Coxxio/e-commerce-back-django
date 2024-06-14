import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Carga todos los fixtures JSON en el directorio src/fixtures/'

    def handle(self, *args, **options):
        # Construye el comando loaddata con todos los archivos JSON en src/fixtures/
        command = 'python manage.py loaddata src/apps/users/fixtures/*.json'
        
        # Ejecuta el comando
        self.stdout.write('Sembrando datos...')
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.stdout.write('Datos sembrados.')
        
        # Imprime la salida y los errores
        if stdout:
            self.stdout.write(stdout.decode('utf-8'))
        if stderr:
            self.stderr.write(stderr.decode('utf-8'))
