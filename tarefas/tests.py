import json
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Tarefa
from .views import listar_tarefas  

class SetupTestCase(TestCase):
    tarefa_id = 0 
    def setUp(self):
        self.cat = Categoria.objects.create(nome="Categoria Teste")
        self.tarefa = Tarefa.objects.create(titulo="Estudar testes no Django", categoria=self.cat, concluida=False)

    

class TarefaTestCase(SetupTestCase):
    # def setUp(self):
    #     self.cat = Categoria.objects.create(nome="Categoria Teste")
    #     self.tarefa = Tarefa.objects.create(titulo="Estudar testes no Django", categoria=self.cat, concluida=False)
    
    def test_criacao_tarefa(self):

        self.assertEqual(self.tarefa.titulo,"Estudar testes no Django")
        
        self.assertEqual(self.tarefa.categoria.nome,"Categoria Teste")

        # #  observe que é possivel criar duas Formas de Teste para um mesmo método
        # # self.assertEqual(self.tarefa.concluida,False) 
        # self.assertFalse(self.tarefa.concluida)    


    def test_marcar_como_concluida(self):
        # Cobre as linhas 19 e 20
        self.tarefa.marcar_como_concluida()
        
        # Recarrega do banco para garantir que o self.save() funcionou
        self.tarefa.refresh_from_db()
        self.assertTrue(self.tarefa.concluida)

    def test_is_valid(self):
        # Cobre a linha 23
        self.assertTrue(self.tarefa.is_valid())
    

class ViewsTestCase(SetupTestCase):

    def test_view_listar_tarefas_retorna_200(self):
        """Simula um GET na rota de listagem e valida o status HTTP e o JSON."""
        url = reverse("listar_tarefas")
        resposta = self.client.get(url)

        # 1. Valida o código de status HTTP
        self.assertEqual(resposta.status_code, 200)

        # 2. Converte a resposta para dicionário Python e valida os dados
        dados = resposta.json()
        self.assertEqual(len(dados["tarefas"]), 1)
        self.assertEqual(dados["tarefas"][0]["titulo"], "Estudar testes no Django")
        self.assertFalse(dados["tarefas"][0]["concluida"]) 
    

    def test_view_criar_tarefa_retorna_200(self):
        """Simula um POST na rota de Criação de Tarefa e retorna o status HTTP e o JSON."""
        url = reverse("criar_tarefa")

        dados_envio = {
            "titulo": "Estudar testes no Django",
            "categoria_id": self.cat.id,
            "concluida": False,
        }

        # Passe os dados convertidos para JSON e especifique o content_type
        resposta = self.client.post(
            url, data=json.dumps(dados_envio), content_type="application/json"
        )

        # 1. Valida o código de status HTTP
        self.assertEqual(resposta.status_code, 200)

        # 2. Converte a resposta para dicionário Python e valida os dados
        dados = resposta.json()
        self.assertEqual(len(dados["tarefas"]), 1)
        self.assertEqual(dados["tarefas"][0]["titulo"], "Estudar testes no Django")
        self.assertFalse(dados["tarefas"][0]["concluida"])

        self.tarefa_id = dados["tarefas"][0]["id"]

    def test_view_atualizar_tarefa_retorna_200(self):
        """Simula a atualização de uma Tarefa e valida o status HTTP e o JSON."""
        # 1. Passa o ID da tarefa existente na URL
        url = reverse("atualizar_tarefa", args=[self.tarefa.id])

        dados_envio = {
            "titulo": "Atualizar Titulo Estudar testes no Django",
            "concluida": True,
        }

        # Se sua rota aceitar PUT/PATCH, troque self.client.post por self.client.put
        resposta = self.client.post(
            url, data=json.dumps(dados_envio), content_type="application/json"
        )

        # 2. Valida o código de status HTTP
        self.assertEqual(resposta.status_code, 200)

        # 3. Valida os campos retornados diretamente no dicionário
        dados = resposta.json()
        self.assertEqual(dados["id"], self.tarefa.id)
        self.assertEqual(dados["titulo"], "Atualizar Titulo Estudar testes no Django")
        self.assertTrue(dados["concluida"])

        # 4. Garante que foi atualizado no banco de dados
        self.tarefa.refresh_from_db()
        self.assertEqual(self.tarefa.titulo, "Atualizar Titulo Estudar testes no Django")
        self.assertTrue(self.tarefa.concluida)
