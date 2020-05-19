from django.urls import include, path
from .views import register


urlpatterns = [
    path('', include('django.contrib.auth.urls'), name="login"),
    path('register/', register, name='register'),
    path('oauth/', include('social_django.urls', namespace='social')),  # <--

]
