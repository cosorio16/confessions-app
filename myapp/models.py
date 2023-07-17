from django.db import models
import uuid

# Create your models here.

class usuario(models.Model):
    name = models.TextField(max_length=200)
    enlace = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.name + ' - ' + str (self.id) + ' - ' + str (self.enlace)


class Confesion(models.Model):
    mensaje = models.TextField()
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.mensaje + ' - ' + str (self.usuario)