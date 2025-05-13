from django.urls import include, path
from django.views.generic import TemplateView

from .views import APIBackets, APICategoriestList, APIProductstList

urlpatterns = [
    path('products/', APIProductstList.as_view()),
    path('categories/', APICategoriestList.as_view()),
    path('backets/', APIBackets.as_view()),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('swagger/', TemplateView.as_view(template_name='swagger.html'), name='swagger'),
]
