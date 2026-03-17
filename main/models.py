from django.db import models
from django.contrib.auth.models import AbstractUser

class Utente(AbstractUser):

    class Livello(models.TextChoices):
        PRINCIPIANTE = 'principiante', 'Principiante'
        INTERMEDIO = 'intermedio', 'Intermedio'
        ESPERTO = 'esperto', 'Esperto'

    foto_profilo = models.ImageField(upload_to='profili/', blank=True, null=True)
    punteggio = models.IntegerField(default=0)
    livello = models.CharField(
        max_length=20,
        choices=Livello.choices,
        default=Livello.PRINCIPIANTE
    )
    flag = models.ManyToManyField('Flag', blank=True)
class Categoria(models.Model):
    nome = models.CharField(max_length=50)


class Sfida(models.Model):
    class Difficolta(models.TextChoices):
        FACILE = 'facile', 'Facile'
        MEDIO = 'medio', 'Medio'
        DIFFICILE = 'difficile', 'Difficile'

    titolo = models.CharField(max_length=100)
    descrizione = models.TextField()
    difficolta = models.CharField(
        max_length=20,
        choices=Difficolta.choices,
        default=Difficolta.FACILE
    )
    p_massimo = models.IntegerField()
    immagine = models.ImageField(upload_to='sfide/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Flag(models.Model):
    chiave = models.CharField(max_length=100)
    sfida = models.ForeignKey(Sfida, on_delete=models.CASCADE)

class Indizio(models.Model):
    testo = models.TextField()
    flag = models.OneToOneField(Flag, on_delete=models.CASCADE)

class Partecipa(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    sfida = models.ForeignKey(Sfida, on_delete=models.CASCADE)
    stato = models.CharField(max_length=20, default='non_iniziata')
    punteggio_ottenuto = models.IntegerField(default=0)

    class Meta:
        unique_together = ('utente', 'sfida')