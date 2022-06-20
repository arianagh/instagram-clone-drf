from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import RegisterUserAPIView, LoginView, Logout,\
    UserDetailAPIUpdate, Instagram


router = DefaultRouter()
router.register("instagram", Instagram, basename="instagram")

urlpatterns = [

    path('profile/<int:pk>', UserDetailAPIUpdate.as_view(), name="get-details"),
    path('register/', RegisterUserAPIView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls


