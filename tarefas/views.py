
import json

from django.http import JsonResponse
from .models import Tarefa, Categoria


def listar_tarefas(request):
    tarefas = Tarefa.objects.all()

    dados = [
        {
            "id": t.id,
            "titulo": t.titulo,
            "concluida": t.concluida
        }
        for t in tarefas
    ]

    return JsonResponse({"tarefas": dados}, status=200)


def criar_tarefa(request):
    dados = json.loads(request.body)

    categoria_body = Categoria.objects.get(
        id=dados["categoria_id"]
    )

    tarefa = Tarefa.objects.create(
        titulo=dados["titulo"],
        categoria=categoria_body,
        concluida=False
    )

    tarefas = [
        {
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "concluida": tarefa.concluida,
            "categoria": tarefa.categoria.id
        }
    ]

    return JsonResponse({"tarefas": tarefas}, status=200)


def atualizar_tarefa(request, id):
    dados = json.loads(request.body)

    tarefa = Tarefa.objects.get(id=id)

    tarefa.titulo = dados["titulo"]
    tarefa.concluida = dados["concluida"]

    tarefa.save()

    return JsonResponse(
        {
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "concluida": tarefa.concluida
        },
        status=200
    )
