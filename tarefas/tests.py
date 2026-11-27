
import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Categoria, Tarefa


class TarefaViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.categoria = Categoria.objects.create(
            nome="Estudos"
        )

        self.tarefa = Tarefa.objects.create(
            titulo="Estudar Python",
            categoria=self.categoria,
            concluida=False
        )

    def test_listar_tarefas(self):
        response = self.client.get(reverse('listar_tarefas'))

        self.assertEqual(response.status_code, 200)

        dados = response.json()

        self.assertEqual(len(dados['tarefas']), 1)
        self.assertEqual(dados['tarefas'][0]['titulo'], 'Estudar Python')
        self.assertEqual(dados['tarefas'][0]['id'], self.tarefa.id)
        self.assertFalse(dados['tarefas'][0]['concluida'])

    def test_listar_tarefas_vazio(self):
        Tarefa.objects.all().delete()

        response = self.client.get(reverse('listar_tarefas'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'tarefas': []})

    def test_criar_tarefa(self):
        dados = {
            'titulo': 'Aprender Django',
            'categoria_id': self.categoria.id
        }

        response = self.client.post(
            reverse('criar_tarefa'),
            data=json.dumps(dados),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        resposta = response.json()

        self.assertEqual(len(resposta['tarefas']), 1)

        tarefa = Tarefa.objects.get(titulo='Aprender Django')

        self.assertEqual(tarefa.categoria.id, self.categoria.id)
        self.assertFalse(tarefa.concluida)

        self.assertEqual(resposta['tarefas'][0]['id'], tarefa.id)
        self.assertEqual(resposta['tarefas'][0]['categoria'], self.categoria.id)

    def test_atualizar_tarefa(self):
        dados = {
            'titulo': 'Estudar Django',
            'concluida': True
        }

        response = self.client.put(
            reverse('atualizar_tarefa', args=[self.tarefa.id]),
            data=json.dumps(dados),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        resposta = response.json()

        self.assertEqual(resposta['id'], self.tarefa.id)
        self.assertEqual(resposta['titulo'], 'Estudar Django')
        self.assertTrue(resposta['concluida'])

        self.tarefa.refresh_from_db()

        self.assertEqual(self.tarefa.titulo, 'Estudar Django')
        self.assertTrue(self.tarefa.concluida)
