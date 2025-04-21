from django.urls import path  # Asegúrate de importar 'path'
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserDetailView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('update/<int:id>/', UserUpdateView.as_view(), name='update_user'),
    path('delete/<str:username>/', UserDeleteView.as_view(), name='delete_user'),
    path('<int:id>/', UserDetailView.as_view(), name='detail_user'),  # Ruta para obtener un usuario por ID
    path('', UserListView.as_view(), name='list_users'),
]
