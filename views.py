from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from enderecos.models import Enderecos

def escrever_cep(cep): #essa função tem por objetivo gerar a string correta para a formataçao de cep: #####-###
    if '-' in cep: #checa se existe o caracter '-' na string do cep
        return cep
    else:
        return cep[:5]+'-'+cep[5:] #caso não exista o caracter '-', a função adiciona

def analisar_cep (cep): #essa função busca as informações de logradouro, bairro, cidade e uf relacionados ao cep
    if Enderecos.objects.filter(cep = escrever_cep(cep)).exists(): #checa se o cep existe na base de dados
        addr = Enderecos.objects.filter(cep = escrever_cep(cep))[0] #pega o elemento da base de dados relacionado ao cep definido
        new_add = {}
        new_add['cep'] = addr.cep
        new_add['endereco'] = addr.logradouro
        new_add['numero'] = addr.numero
        new_add['complemento'] = addr.complemento
        new_add['bairro'] = addr.bairro
        new_add['cidade'] = addr.cidade
        new_add['uf'] = addr.uf
        new_add['desc'] = addr.descricao
        new_add['required'] = 'required' #aqui, caso a busca pelo cep funcione, seta os campos obrigatórios e o usuário só conseguira submeter o formulário, caso preencha o campo de número
        new_add['readonly_in'] = 'readonly'
        new_add['disable_but'] = 'False' #new_add armazena os parametros para serem passados ao código HTML como context
        
    elif not (cep == '0'): #caso o cep não exista na base de dados
        try:
            addr = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep.replace('-',''))) #procura as informações relacionadas ao cep na API viacep.com.br
            addr = addr.json() #transforma o conteudo .json obtido em um dicionario
            new_add = {}
            try:
                new_add['cep'] = addr['cep']
                new_add['endereco'] = addr['logradouro']
                new_add['numero'] = ''
                new_add['complemento'] = ''
                new_add['bairro'] = addr['bairro']
                new_add['cidade'] = addr['localidade']
                new_add['uf'] = addr['uf']
                new_add['desc'] = ''
                new_add['required'] = 'required'#aqui, caso a busca pelo cep funcione, seta os campos obrigatórios e o usuário só conseguira submeter o formulário, caso preencha o campo de número
                new_add['readonly_in'] = 'readonly' #parametro adicionado na tag HTML 'INPUT', nos campos de entrada de logradouro, bairro, cidade e uf, para que o usuário não os altere: são padrão
                new_add['disable_but'] = ''
            except: #caso haja algum erro na leitura do .json, significa que o CEP foi digitado no formato correto, mas não existe
                new_add['cep'] = cep
                new_add['endereco'] = 'CEP não encontrado'
                new_add['numero'] = 'CEP não encontrado'
                new_add['complemento'] = 'CEP não encontrado'
                new_add['bairro'] = 'CEP não encontrado'
                new_add['cidade'] = 'CEP não encontrado'
                new_add['uf'] = 'CEP não encontrado'
                new_add['desc'] = 'CEP não encontrado'
                new_add['required'] = ''
                new_add['readonly_in'] = 'readonly'
                new_add['disable_but'] = 'disabled' #quando esse parâmetro está em 'disabled' ele não permite que o usuário clique no botão 'submit' e salve as informações no banco de dados
        except:#caso haja algum erro na obtenção do .json, significa que o CEP foi digitado incorretamente
            new_add = {} 
            new_add['cep'] = cep
            new_add['endereco'] = 'CEP inválido'
            new_add['numero'] = 'CEP inválido'
            new_add['complemento'] = 'CEP inválido'
            new_add['bairro'] = 'CEP inválido'
            new_add['cidade'] = 'CEP inválido'
            new_add['uf'] = 'CEP inválido'
            new_add['desc'] = 'CEP inválido'
            new_add['required'] = '' 
            new_add['readonly_in'] = 'readonly'
            new_add['disable_but'] = 'disabled'

    else: #nesse caso, se o valor do CEP for definido como '0', os campos ficarão em branco
        new_add = {}
        new_add['cep'] = ''
        new_add['endereco'] = ''
        new_add['numero'] = ''
        new_add['complemento'] = ''
        new_add['bairro'] = ''
        new_add['cidade'] = ''
        new_add['uf'] = ''
        new_add['desc'] = ''
        new_add['required'] = ''
        new_add['readonly_in'] = 'readonly'
        new_add['disable_but'] = 'disabled'
    return new_add

def analise (elemento): #troca os campos vazios por '-'
    if elemento =='':
        return '-'
    else:
        return elemento


def home(request): #página raiz do app Enderecos
    context = {
        'address': Enderecos.objects.all() #Envia todos os endereços do banco de dados para serem dispostos no HTML
    }
    return render(request, 'enderecos/home.html', context)

def create(request): #página do formulário de criação de novo endereço
    context = {
        'novoend' : analisar_cep ('0') #aqui, coloca os dados padrão como vazios e o botão de 'submit' como desativado 
    }
    if request.method == "POST": #checa se há alguma resposta do formulário
        if request.POST.get('pesquisar'): #checa se a resposta do formulário foi o clique no botão 'Pesquisar'
            cep = request.POST.get('cep') #pega o valor digitado no campo CEP
            cep = escrever_cep(cep) #o escreve como uma string no formato #####-###
            context = {
                'novoend' : analisar_cep (cep) #atualiza os parâmetros do context para preencher os campos que devem ser preenchidos automaticamente com o CEP
            }
        elif request.POST.get('enviar'): #checa se a resposta do formulário foi o clique no botão 'Cadastrar'
            cep = request.POST.get('cep')
            cep = analise(escrever_cep(cep))
            logr = analise(request.POST.get('logradouro'))
            numero = analise(request.POST.get('numero'))
            comp = analise(request.POST.get('complemento'))
            bairro = analise(request.POST.get('bairro'))
            cidade = analise(request.POST.get('cidade'))
            uf = analise(request.POST.get('uf'))
            desc = analise(request.POST.get('desc').capitalize()) #até aqui, pega os valores inseridos em todos os campos e os substituem por '-' caso estejam vazios
            Enderecos.objects.update_or_create(defaults = {'cep': cep, 'logradouro' : logr, 'numero' : numero, 'complemento' : comp, 'bairro' : bairro, 'cidade' : cidade, 'uf' : uf, 'descricao' : desc}, cep = cep) #se já existir um elemento no banco de dados com o cep inserido, ele o atualiza. Caso contrário, cria um novo
            return redirect('endereco-home')#Redireciona o usuário para a página inicial do app
    
    return render(request, 'enderecos/create.html', context) #mantém o usuário na página do formulário