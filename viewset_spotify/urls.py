from rest_framework import routers
from .views import UsuariosViewset

router = routers.DefaultRouter()
router.register(r'usuarios', UsuariosViewset, basename='usuarios')

urlpatterns = router.urls