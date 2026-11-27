
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    concluida = models.BooleanField(default=False)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    def marcar_como_concluida(self):
        self.concluida = True
        self.save()

    def is_valid(self):
        return True

    def __str__(self):
        return self.titulo
