from rest_framework import serializers
from .models import Usuarios, Artistas, Discos, Canciones

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['id', 'nombre', 'apellido', 'edad', 'email']
        
        
    def validate_edad(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('La edad debe ser un entero positivo') 
        return value
    
    def validate_nombre(self,value):
        if len(value) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError('El nombre solo debe contener letras')
        return value
    
    def validate_apellido(self,value):
        if len(value) < 2:
            raise serializers.ValidationError('El apellido debe tener al menos 2 caracteres')
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError('El apellido solo debe contener letras')
        return value
    
    def validate_email(self, value):
        id_usuario = self.instance.id if self.instance else None
        if Usuarios.objects.exclude(id=id_usuario).filter(email=value).exists():
            raise serializers.ValidationError('Este email ya está registrado')
        return value
    
class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artistas
        fields = ['id', 'artistname', 'usuario']

    def validate(self, data):
        usuario = data['usuario']
        name = data['artistname']

        if Artistas.objects.filter(usuario=usuario, artistname=name).exists():
            raise serializers.ValidationError('Este artista ya está en tu lista de preferencias')

        return data
    
class DiscosSerializer(serializers.ModelSerializer):
    class Meta:

        model = Discos
        fields = ['id', 'albumname', 'artistname', 'usuario']
            
    def validate(self, data):
        usuario = data['usuario']
        titulo = data['albumname']
        if Discos.objects.filter(usuario=usuario, albumname=titulo).exists():
            raise serializers.ValidationError('Este disco ya está en tu lista de preferencias')
        return data
        
class CancionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canciones
        fields = ['id', 'songtitle', 'artistname', 'usuario']
            
    def validate(self, data):
        usuario = data['usuario']
        titulo = data['songtitle']
                
        if Canciones.objects.filter(usuario=usuario, songtitle=titulo).exists():
            raise serializers.ValidationError('Esta canción ya está en tu lista de preferencias')
                
        return data