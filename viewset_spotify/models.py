from django.db import models

# Create your models here.

class Usuarios(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.nombre 
    

class Artistas(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='artistas_favoritos')
    artistname = models.CharField(max_length=150)
    
    def __str__(self):
        return self.artistname
        

class Discos(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='discos_favoritos')
    albumname = models.CharField(max_length=150)
    artistname = models.CharField(max_length=150)
    
    def __str__(self):
        return f'{self.albumname} - {self.artistname}'

class Canciones(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='canciones_favoritas')
    songtitle = models.CharField(max_length=150)
    artistname = models.CharField(max_length=150)
    
    def __str__(self):
        return f'{self.songtitle} - {self.artistname}'
    