from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Usuarios

from .serializer import (
    UsuariosSerializer,
    ArtistaSerializer,
    DiscosSerializer,
    CancionesSerializer,
)

from .services.spotify import(
    buscar_artista,
    buscar_album,
    buscar_cancion,
)



# Create your views here.

class UsuariosViewset(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all().order_by('id')
    serializer_class = UsuariosSerializer
    lookup_field = 'pk'
    
    # Endpoint para añadir artistas favoritos

    @action(detail=True, methods=['post'])
    def add_artista(self, request, pk=None):
        usuario = self.get_object()
        
        artistname = request.data.get('artistname')        
        if not artistname:
            return Response(
                {'error': 'Hay que proporcionar el nombre de un artista'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        artista = buscar_artista(artistname)
        if not artista:
            return Response(
                {'error': 'No se encontró el artista en Spotify'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = ArtistaSerializer(
            data={'usuario': usuario.id, 'artistname': artista}
            )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)   
    
    
    # Endpoint para añadir discos favoritos
    
    @action(detail=True, methods=['post'])
    def add_disco(self, request, pk=None):
        usuario = self.get_object()
        
        album = request.data.get('album')
        if not album:
            return Response(
                {'error': 'Hay que proporcionar el nombre de un álbum'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resultado = buscar_album(album)
        if not resultado:
            return Response(
                {'error': 'No se encontró el álbum en Spotify'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        albumname, artistname = resultado
        
        serializer = DiscosSerializer(
            data={
                'usuario': usuario.id,
                'albumname': albumname,
                'artistname': artistname
            }
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    # Endpoint para añadir canciones favoritas
    
    @action(detail=True, methods=['post'])
    def add_cancion(self, request, pk=None):
        usuario = self.get_object()

        song = request.data.get('song')
        if not song:
            return Response(
                {'error': 'Hay que proporcionar el nombre de una canción'},
                status=status.HTTP_400_BAD_REQUEST
            )

        resultado = buscar_cancion(song)
        if not resultado:
            return Response(
                {'error': 'No se encontró la canción en Spotify'},
                status=status.HTTP_404_NOT_FOUND
            )

        songtitle, artistname = resultado

        serializer = CancionesSerializer(
            data={
                'usuario': usuario.id,
                'songtitle': songtitle,
                'artistname': artistname
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    # Endpoint para visualizar artistas favoritos    
    @action(detail=True, methods=['get'])
    def ver_artistas(self, request, pk=None):
        usuario = self.get_object()
        artistas = usuario.artistas_favoritos.all()
        serializer = ArtistaSerializer(artistas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # Endpoint para visualizar discos favoritos
    @action(detail=True, methods=['get'])
    def ver_discos(self, request, pk=None):
        usuario = self.get_object()
        discos = usuario.discos_favoritos.all()
        serializer = DiscosSerializer(discos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # Endpoint para visualizar canciones favoritas
    @action(detail=True, methods=['get'])
    def ver_canciones(self, request, pk=None):
        usuario = self.get_object()
        canciones = usuario.canciones_favoritas.all()
        serializer = CancionesSerializer(canciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # Endpoint para borrar artistas favoritos
    @action(detail=True, methods=['delete'])
    def borrar_artista(self, request, pk=None):
        usuario = self.get_object()
        favorito_id = request.query_params.get('favorito_id')
        
        if not favorito_id:
            return Response(
                {'error': 'Hay que proporcionar el ID del artista favorito a borrar'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        qs = usuario.artistas_favoritos.filter(id=favorito_id)
        
        if not qs.exists():
            return Response(
                {'error': f'Artista con ID {favorito_id} no está entre tus favoritos'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        qs.delete()
        return Response({'mensaje': f'Artista con ID {favorito_id} borrado correctamente'}
                        ,status=status.HTTP_200_OK
                        )
    
    # Endpoint para borrar discos favoritos
    @action(detail=True, methods=['delete'])
    def borrar_disco(self, request, pk=None):
        usuario = self.get_object()
        favorito_id = request.query_params.get('favorito_id')
        
        if not favorito_id:
            return Response(
                {'error': 'Hay que proporcionar el ID del álbum favorito a borrar'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        qs = usuario.discos_favoritos.filter(id=favorito_id)
        
        if not qs.exists():
            return Response(
                {'error': f'Álbum con ID {favorito_id} no está entre tus favoritos'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        qs.delete()
        return Response({'mensaje': f'Álbum con ID {favorito_id} borrado correctamente'}
                        ,status=status.HTTP_200_OK
                        )
    
    
    # Endpoint para borrar canciones favoritas
    @action(detail=True, methods=['delete'])
    def borrar_cancion(self, request, pk=None):
        usuario = self.get_object()
        favorito_id = request.query_params.get('favorito_id')
        
        if not favorito_id:
            return Response(
                {'error': 'Hay que proporcionar el ID de la canción favorito a borrar'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        qs = usuario.canciones_favoritas.filter(id=favorito_id)
        
        if not qs.exists():
            return Response(
                {'error': f'Canción con ID {favorito_id} no está entre tus favoritas'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        qs.delete()
        return Response({'mensaje': f'Canción con ID {favorito_id} borrada correctamente'}
                        ,status=status.HTTP_200_OK
                        )
    