from django.urls import path, include

from . import views

app_name = 'documentos'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),

    path('bodega/', views.BodegaListView.as_view(), name='list_bodega'),
    path('bodega/nueva/', views.BodegaCreateView.as_view(), name='create_bodega'),
    path('bodega/ver/<uuid:pk>', views.BodegaDetailView.as_view(), name='detail_bodega'),
    path('bodega/actualizar/<uuid:pk>', views.BodegaUpdateView.as_view(), name='update_bodega'),
    path('bodega/eliminar/<uuid:pk>', views.BodegaDeleteView.as_view(), name='delete_bodega'),

]


    




    
    