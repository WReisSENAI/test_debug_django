
from django.contrib import admin
from django.urls import path
from tarefas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tarefas/', views.listar_tarefas, name='listar_tarefas'),
    path('tarefas/criar/', views.criar_tarefa, name='criar_tarefa'),
    path(
        'tarefas/atualizar/<int:id>/',
        views.atualizar_tarefa,
        name='atualizar_tarefa'
    ),
]
