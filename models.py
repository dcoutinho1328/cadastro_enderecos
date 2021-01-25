from django.db import models

class Enderecos(models.Model): #cria a tabela de endereços na base de dados, com os campos descritos abaixo
    cep = models.CharField(max_length=9)
    logradouro = models.TextField()
    numero = models.TextField()
    complemento = models.TextField()
    bairro = models.TextField()
    cidade = models.TextField()
    uf = models.CharField(max_length=3)
    descricao = models.TextField()