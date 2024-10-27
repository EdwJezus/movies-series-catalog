##from termcolor import cprint  #Biblioteca para personalizar textos
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

################################ SQL

# Conectar ao Banco de Dados
conn = sqlite3.connect('bancoDeDados.db')
cursor = conn.cursor()

def init_db():
  # Criar uma tabela
  cursor.execute('''
                CREATE TABLE IF NOT EXISTS filmes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tituloFilme TEXT NOT NULL,
                    posterFilme TEXT NOT NULL,
                    anoFilme TEXT NOT NULL,
                    generoFilme TEXT NOT NULL,
                    precoFilme TEXT NOT NULL,
                    diretorFilme TEXT NOT NULL,
                    duracaoFilme TEXT NOT NULL
                )
                ''')
  cursor.execute('''
                CREATE TABLE IF NOT EXISTS series(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  tituloSerie TEXT NOT NULL,
                  posterSerie TEXT NOT NULL,
                  anoSerie TEXT NOT NULL,
                  generoSerie TEXT NOT NULL,
                  precoSerie TEXT NOT NULL,
                  temporadasSerie TEXT NOT NULL,
                  duracaoEpsSerie TEXT NOT NULL,
                  qntEpsSerie TEXT NOT NULL
                )
                ''')
  cursor.execute('''
                CREATE TABLE IF NOT EXISTS diretores(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nomeDiretor TEXT NOT NULL,
                  idadeDiretor TEXT NOT NULL,
                  nacionalidadeDiretor TEXT NOT NULL
                  )
                ''')
  cursor.execute('''
                CREATE TABLE IF NOT EXISTS generos(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nomeGenero TEXT NOT NULL,
                  infoGenero TEXT NOT NULL
                )
                ''')
  conn.commit()
  conn.close()


init_db();

@app.route('/')
def index():
  return render_template('index.html')

def conectar_db():
  conn = sqlite3.connect('bancoDeDados.db')
  return conn


################################ Classes de Herança

class Projeto():
  def __init__(self, id, titulo, poster, ano, Genero, preco):
    self.id= id
    self.titulo = titulo
    self.poster = poster
    self.ano = ano
    self.genero = Genero #Associação
    self.preco = preco
  def calculaDuracaoTotal(self): #Polimorfismo
    pass
  def setId(self, id):
    self.id = id
  def setTitulo(self, titulo):
    self.titulo = titulo
  def setPoster(self, poster):
    self.poster = poster
  def setAno(self, ano):
    self.ano = ano
  def setGenero(self, novoGenero):
    self.genero = novoGenero
  def setPreco(self, preco):
    self.creditos = preco
  def getId(self):
    return self.id
  def getTitulo(self):
    return self.titulo
  def getPoster(self):
    return self.poster
  def getAno(self):
    return self.ano
  def getGenero(self):
    return self.genero
  def getPreco(self):
    return self.preco

class Filme(Projeto):
  def __init__(self, id, titulo, poster, ano, Genero, preco, Diretor, duracao):
    super().__init__(id, titulo, poster, ano, Genero, preco)
    self.diretor = Diretor #Associação
    self.duracao = duracao
  def calculaDuracaoTotal(self): #Polimorfismo
    return self.duracao
  def setDiretor(self, novoDiretor):
    self.diretor = novoDiretor
  def getDiretor(self):
    return self.diretor

class Serie(Projeto):
  def __init__(self, id, titulo, poster, ano, Genero, preco, temporadas, duracaoEps, qntEps):
    super().__init__(id, titulo, poster, ano, Genero, preco)
    self.temporadas = temporadas
    self.duracaoEps = duracaoEps
    self.qntEps = qntEps
  def calculaDuracaoTotal(self): #Polimorfismo
    return (self.temporadas * self.duracaoEps * self.qntEps)

################################ Classes de associação

class Diretor():
  def __init__(self, nome, idade, nacionalidade):
    self.nome = nome
    self.idade = idade
    self.nacionalidade = nacionalidade
  def setNome(self, nome):
    self.nome = nome
  def setIdade(self, idade):
    self.idade = idade
  def setNacionalidade(self, nacionalidade):
    self.nacionalidade = nacionalidade
  def getNome(self):
    return self.nome
  def getIdade(self):
    return self.idade
  def getNacionalidade(self):
    return self.nacionalidade

class Genero():
  def __init__(self, name, info):
    self.name = name
    self.info = info
  def setName(self, name):
    self.name = name
  def setInfo(self, info):
    self.info = info
  def getName(self):
    return self.name
  def getInfo(self):
    return self.info

####################################Classe usuário

class Convidado():
  def __init__(self, creditos):
    self.creditos = creditos
  def calculaCreditos(self, projeto):
    self.creditos = self.creditos - projeto.preco
    return self.creditos
  def maisCreditos(self, dinheiro):
    self.creditos = self.creditos + dinheiro
    return self.creditos
  def getCreditos(self):
    return self.creditos

convidado1 = Convidado(0)  ####### COLOCANDO DINHEIRO


############################################### Cadastro integrado com HTML

############CADASTRO FILME
@app.route('/add_movie', methods=['POST']) #Pega do HTML
def add_movie():
  titulo = request.form['titulo']
  poster = request.form['poster']
  ano = request.form['ano']
  genero = request.form['genero']
  preco = request.form['preco']
  diretor = request.form['diretor']
  duracao = request.form['duracao']

  novo_filme = Filme(titulo, poster, ano, genero, preco, diretor, duracao) #Cria o objeto, istancia

  #Salva filme no banco SQL
  conn = conectar_db()
  cursor = conn.cursor()
  cursor.execute(('INSERT INTO filmes (tituloFilme, posterFilme, anoFilme, generoFilme, precoFilme, diretorFilme, duracaoFilme) VALUES (?, ?, ?, ?, ?, ?, ?)'), (novo_filme.titulo, novo_filme.poster, novo_filme.ano, novo_filme.genero, novo_filme.preco, novo_filme.diretor, novo_filme.duracao))
  conn.commit()
  conn.close()

  return "Filme cadastrado com sucesso!"

############CADASTRO SÉRIE
@app.route('/add_serie', methods=['POST'])
def add_serie():
  titulo = request.form['titulo']
  poster = request.form['poster']
  ano = request.form['ano']
  genero = request.form['genero']
  preco = request.form['preco']
  temporadas = request.form['preco']
  duracaoEps = request.form['duracaoEps']
  qntEps = request.form['qntEps']

  nova_serie = Serie(titulo, poster, ano, genero, preco, temporadas, duracaoEps, qntEps)

  #Salva série no banco SQL
  conn = conectar_db()
  cursor = conn.cursor()
  cursor.execute(('INSERT INTO series (tituloSerie, posterSerie, anoSerie, generoSerie, precoSerie, temporadasSerie, duracaoEpsSerie, qntEpsSerie) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'), (nova_serie.titulo, nova_serie.poster, nova_serie.ano, nova_serie.genero, nova_serie.preco, nova_serie.temporadas, nova_serie.duracaoEps, nova_serie.qntEps))
  conn.commit()
  conn.close()

  return "Série cadastrada com sucesso!"


###################################################### Listar Filmes
"""
###LISTAR FILMES
@app.route('/filmes') ##Pega os filmes do Banco SQL
def listar_filmes():
  conn = conectar_db()
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM filmes')
  filmes_data = cursor.fetchall()
  conn.close()

  filmes = [Filme(titulo, poster, ano, genero, preco, diretor, duracao) for (id, titulo, poster, ano, genero, preco, diretor, duracao) in filmes_data]

  return render_template('filmes.html', filmes=filmes)

if __name__ == '__main__':
    app.run(debug=True)

###LISTAR SÉRIES
@app.route('/filmes')
def listar_series():
  conn = conectar_db()
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM series')
  series_data = cursor.fetchall()
  conn.close()

  series = [Serie(titulo, poster, ano, genero, preco, temporadas, duracaoEps, qntEps) for (id, titulo, poster, ano, genero, preco, temporadas, duracaoEps, qntEps) in series_data]

  return render_template('filmes.html', series=series)
"""


@app.route('/filmes') ##Pega os filmes do Banco SQL
def listar_filmes():
  conn = conectar_db()
  cursor = conn.cursor()

  cursor.execute('SELECT * FROM filmes')
  filmes_data = cursor.fetchall()

  cursor.execute('SELECT * FROM series')
  series_data = cursor.fetchall()

  conn.close()

  filmes = [Filme(id, titulo, poster, ano, genero, preco, diretor, duracao) for (id, titulo, poster, ano, genero, preco, diretor, duracao) in filmes_data]

  series = [Serie(id, titulo, poster, ano, genero, preco, temporadas, duracaoEps, qntEps) for (id, titulo, poster, ano, genero, preco, temporadas, duracaoEps, qntEps) in series_data]

  return render_template('filmes.html', filmes=filmes, series=series)

###################################################

@app.route('/projeto/<int:id>') ##Pega os filmes do Banco SQL
def descricao_projeto(id):
  conn = conectar_db()
  cursor = conn.cursor()

  cursor.execute('SELECT * FROM filmes WHERE id = ?', (id,))
  filme_data = cursor.fetchone()

  cursor.execute('SELECT * FROM series WHERE id = ?', (id,))
  serie_data = cursor.fetchone()

  conn.close()

  filme = None
  serie = None

  # Se o filme foi encontrado
  if filme_data:
    filme = [Filme(titulo=filme_data[1], poster=filme_data[2], ano=filme_data[3], genero=filme_data[4], preco=filme_data[5], diretor=filme_data[6], duracao=filme_data[7])]

  # Se a série foi encontrada
  if serie_data:
    serie = [Serie(titulo=serie_data[1], poster=serie_data[2], ano=serie_data[3], genero=serie_data[4], preco=serie_data[5], temporadas=serie_data[6], duracaoEps=serie_data[7], qntEps=serie_data[8])]

  return render_template('projeto.html', filme=filme, serie=serie)

if __name__ == '__main__':
    app.run(debug=True)

##""""

"""

################################### Listas

filmes = []
series = []
diretores = []
generos = []
alugueis = []

################################### Pré-Cadastro
DRAMA = Genero('DRAMA', 'CONSISTE EM SEQUENCIAS EMOCIONANTES.')

ACAO = Genero('AÇÃO', 'CONSISTE EM SEQUENCIAS DE ADRENALINA.')

COMEDIA = Genero('COMEDIA', 'CONSISTE EM SEQUENCIAS DE HUMOR')
#####
COPPOLA = Diretor('FRANCIS FORD COPPOLA', 84, 'AMERICANO')

WINDING = Diretor('NICOLAS WINDING REFN', 53, 'DINAMARQUÊS')

RIDLEY = Diretor('RIDLEY SCOTT', 85, 'BRITÂNICO')
#####
GODFATHER = Filme('O PODEROSO CHEFÃO', 1972, DRAMA, 24.99, COPPOLA, 175)

DRIVE = Filme('DRIVE', 2011, ACAO, 22.99, WINDING, 100)

BLADERUNNER = Filme('BLADE RUNNER', 1982, DRAMA, 23.99, RIDLEY, 117)
#####
THEOFFICE = Serie('THE OFFICE', 2005, COMEDIA, 30.99, 9, 25, 20)

BREAKINGBAD = Serie('BREAKING BAD', 2008, DRAMA, 24.99, 5, 50 , 13)

SEVERANCE = Serie('SEVERANCE', 2022, DRAMA, 24.99, 1, 50, 9)
####
generos.append(DRAMA)
generos.append(ACAO)
generos.append(COMEDIA)
diretores.append(COPPOLA)
diretores.append(WINDING)
diretores.append(RIDLEY)
filmes.append(GODFATHER)
filmes.append(DRIVE)
filmes.append(BLADERUNNER)
series.append(THEOFFICE)
series.append(BREAKINGBAD)
series.append(SEVERANCE)


############################################### Menu

print('''
⣶⡄⠀⣶⠀⢰⣶⣶⡆⠠⣶⣶⣶⡆⢰⣶⣶⣦⠀⣶⠀⠀⠀⣶⡆⠐⣶⠀⣰⡖
⣿⣷⡀⣿⠀⣸⣇⣀⡀⠀⠀⣿⠀⠀⢸⣇⣀⡀⠀⣿⠀⠀⠀⣿⡇⠀⠹⣷⡿⠁
⣿⡿⣷⣿⠀⣿⡟⠛⠁⠀⠀⣿⠀⠀⢸⡏⠉⠁⠀⣿⠀⠀⠀⣿⡇⠀⢠⣿⣇⠀
⣿⡇⢻⣿⠀⣿⣷⣶⡆⠀⠀⠿⠀⠀⠸⠇⠀⠀⠀⣿⣶⣶⠀⣿⡇⢀⣿⠋⢿⡆
⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
''')
print('')
print('==========NETFLIX=========')
print('')
print('        Bem Vindo!')

msg_continuar = 'Tecle ENTER para continuar.'

login = 'n'
while login != '3': #Loop Inicial para login
  print('')
  print('==========================')
  print('===========MENU===========')
  print('==========================')
  print('1) Entrar como Operador')
  print('2) Entrar como Convidado')
  print('--------------------------')
  print('3) Finalizar Programa')
  print('==========================')
  print('')
  login = input('O que deseja fazer? (1/2/3) ')

#################################################### Modo Operador

############################################## Login operador

  if login == '1': #Loop do login de operador
    print('')
    print('===================')
    print('=======LOGIN=======')
    print('===================')
    op_user = input('Digite o usuario: ')
    op_senha = input('Digite a senha: ')
    print('===================')
    print('')
    
    #Verifica se o usuario e senha de operador estão corretos
    if op_user == 'operador01' and op_senha == 'senha123':
      print('Login efetuado com sucesso!')
      print('Seja bem vindo operador!')

############################################## Menu

      quest = 'n'
      while quest != '5': #Loop das opções do Operador

        print('')
        print('======================')
        print('=======OPERADOR=======')
        print('======================')
        print('1) Cadastrar Filme')
        print('2) Cadastrar Série')
        print('----------------------')
        print('3) Cadastrar Diretor')
        print('4) Cadastrar Genêro')
        print('----------------------')
        print('5) Sair')
        print('======================')
        print('')

        mensagem = '***obs: Já existem alguns genêros, diretores, filmes e séries pré-cadastrados. Porém se você deseja adicionar mais algum, basta cadastra-lo no modo operador.'
        cprint('\033[1m\033[3m' + mensagem, 'white', 'on_grey')
        
        print('')
        quest = input('O que deseja fazer? ')
        print('')

###################################################### Cadastro
############################################## Cadastrar Filme

        if quest == '1':
          print('========================')
          print('  FILMES JÁ CADASTRADOS ')
          print('========================')
          for i in filmes:
            print(f'- {i.getTitulo()}')
          print('========================')
          print('')

          print('- Cadastrando novo filme.')
          try:
            titulo1 = input('Titulo: ').upper()
            ano1 = int(input('Ano: '))
            diretor1 = ''
            preco1 = float(input('Preço: $ '))
            duracao1 = int(input('Duracao em minutos: '))
            
            print('')
            print('===========')
            print('  GENÊROS  ')
            print('===========')
            for g in generos:
              print(f'- {g.getName()}')
            print('===========')
            #Parte para selecionar gênero pela associação
            genero_nome1 = input('Gênero: ').upper()
  
            genero_associado1 = None
            for genero in generos:
              if genero.getName() == genero_nome1:
                genero_associado1 = genero
                break
  
            if genero_associado1:
              filme1 = Filme(titulo1, ano1, genero_associado1, preco1, diretor1,
                             duracao1)
  
              print('============')
              print(' DIRETORES')
              print('============')
              for d in diretores:
                print(f'- {d.getNome()}')
              print('============')
  
              diretor_nome = input('Diretor: ').upper()
              #Parte para selecionar Diretor pela associação
              diretor_associado = None
              for diretor in diretores:
                if diretor.getNome() == diretor_nome:
                  diretor_associado = diretor
                  break
  
              if diretor_associado:
                filme1 = Filme(titulo1, ano1, genero_associado1, preco1,
                               diretor_associado, duracao1)
                filmes.append(filme1)
                print('')
                print('O filme foi cadastrado com sucesso!')
                cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
                input('')
              else: #Else pra caso o diretor não seja encontrado
                print('Diretor não encontrado.')
                print('Filme NÃO cadastrado.')
                cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
                input('')
            else: #Else pra caso o gênero não seja encontrado
              print('Genêro não encontrado.')
              print('Filme NÃO cadastrado.')
              cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
              input('')

          except ValueError: #Except para erro de digitação
            print('')
            print('Você digitou algo errado.')
            input('Tecle ENTER para voltar e tentar novamente.')

############################################## Cadastrar Serie

        elif quest == '2':
          print('========================')
          print('  SÉRIES JÁ CADASTRADAS ')
          print('========================')
          for s in series:
            print(f'- {s.getTitulo()}')
          print('========================')
          print('')

          print('- Cadastrando nova série.')
          try:
            titulo2 = input('Titulo: ').upper()
            ano2 = int(input('Ano: '))
            preco2 = float(input('Preço: $ '))
            temporadas = int(input('Quantidade de Temporadas: '))
            qntEps = int(input('Quantidade de episodios por temporada: '))
            duracaoEps = int(input('Duracao dos episodios em minutos: '))
  
            print('')
            print('===========')
            print('  GENÊROS  ')
            print('===========')
            for g in generos:
              print(f'- {g.getName()}')
            print('===========')
            #Parte para selecionar gênero pela associação
            genero_nome = input('Genêro: ').upper()
            print('')
  
            genero_associado = None
            for genero in generos:
              if genero.getName() == genero_nome:
                genero_associado = genero
                break
  
            if genero_associado:
              serie1 = Serie(titulo2, ano2, genero_associado, preco2, temporadas,
                             duracaoEps, qntEps)
              series.append(serie1)
              print('')
              print('A série foi cadastrada com sucesso!')
              cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
              input('')
            else: #Else pra caso o Gênero não seja encontrado
              print("Gênero não encontrado.")
              print('Série NÃO cadastrada.')
              cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
              input('')

          except ValueError: #Except para erro de digitação
            print('')
            print('Você digitou algo errado.')
            input('Tecle ENTER para voltar e tentar novamente.')

############################################## Cadastrar Diretor

        elif quest == '3':
          print('========================')
          print('DIRETORES JÁ CADASTRADOS')
          print('========================')
          for d in diretores:
            print(f'- {d.getNome()}')
          print('========================')
          print('')
          try:
            nome = input('Nome do diretor: ').upper()
            idade = int(input('Idade: '))
            nacionalidade = input('Nacionalidade: ').upper()
            diretor1 = Diretor(nome, idade, nacionalidade)
            diretores.append(diretor1)
            print('')
            print('O Diretor foi cadastrado com sucesso!')
            cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
            input('')
          except ValueError: #Except para erro de digitação
            print('')
            print('Você digitou algo errado.')
            input('Tecle ENTER para voltar e tentar novamente.')

############################################## Cadastrar Genero

        elif quest == '4':
          print('========================')
          print(' GENÊROS JÁ CADASTRADOS')
          print('========================')
          for g in generos:
            print(f'- {g.getName()}')
          print('========================')
          print('')
          name = input('Genêro: ').upper()
          info = input('Informações do genêro: ').upper()
          genero1 = Genero(name, info)
          generos.append(genero1)
          print('')
          print('O Genêro foi cadastrado com sucesso!')
          cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
          input('')

############################################## Sair do modo operador

        elif quest == '5':
          print('')
          print('Saiu do modo operador.')
          print('')

############################################## Erro Comando Inválido

        else:
          print('')
          print('Comando Inválido! digite de 1 a 5 para a opção desejada.')
          cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
          input('')

############################################## Login incorreto

    else:
      print('')
      print('Login incorreto!')
      print('')
      dica_operador = '***obs: O usuário correto é "operador01" e a senha é "senha123"'
      cprint('\033[1m\033[3m' + dica_operador, 'white', 'on_grey')
      print('')
      cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
      input('')

######################################################################
######################################################################
######################################################################
############################################ Modo Convidado

  elif login == '2': #Inicia Loop Login Convidado
    print('')
    convidado_user = input('Digite o usuário: ')
    convidado_senha = input('Digite sua senha: ')
    print('')

    print('Logado com sucesso.')
    print(f'Bem vindo {convidado_user}!')

    quest2 = 'n'
    while quest2 != '7': #Loop das opções do convidado
      print('')
      print('======================')
      print('=======CONVIDADO======')
      print('======================')
      print('1) Pesquisar Filme')
      print('2) Pesquisar Série')
      print('----------------------')
      print('3) Pesquisar Diretor')
      print('4) Pesquisar Genêro')
      print('----------------------')
      print('5) Ver Carteira')
      print('6) Ver Aluguéis')
      print('----------------------')
      print('7) Sair do modo usuário')
      print('======================')

      print('')
      mensagem = '***obs: Já existem alguns, genêros, diretores, filmes e séries pré-cadastrados. Porém se você deseja adicionar mais algum, basta cadastra-lo.'
      cprint('\033[1m\033[3m' + mensagem, 'white', 'on_grey')
      print('')
      
      quest2 = input('O que deseja fazer? ')

################################################## Pesquisa
############################################## Pesquisar Filme

      if quest2 == '1':
        print('========================')
        print('      LISTA FILMES      ')
        print('========================')
        for i in filmes:
          print(f'- {i.getTitulo()}')
        print('========================')

        #Input para achar o filme desejado na lista de filmes pelo seu Titulo
        escolhe_filme = input(
            'Qual filme deseja saber informações? (digite o titulo) ').upper()
        print('')
        filme_escolhido = None
        for filme in filmes:
          if filme.getTitulo() == escolhe_filme:
            filme_escolhido = filme
            break
        if filme_escolhido:
          #Se achar o filme printa a suas informações
          print('')
          print(f'Titulo: {filme_escolhido.getTitulo()}')
          print(f'Ano: {filme_escolhido.getAno()}')
          print(f'Genero: {filme_escolhido.genero.getName()}')
          print(f'Diretor: {filme_escolhido.diretor.getNome()}')
          print(
              f'Duração total: {filme_escolhido.calculaDuracaoTotal()} Minutos'
          )
          print(f'Preço aluguel do filme: $ {filme_escolhido.getPreco():.2f}')
          print('')
          
          ################### Alugar série
          aluguel = input('Deseja alugar o filme? (s/n) ')
          if aluguel == 's':
            #If para verificar se o convidado tem dinheiro suficiente
            if (filme_escolhido.getPreco()) <= (convidado1.getCreditos()):
              alugueis.append(filme_escolhido)
              print('')
              print('Filme alugado com sucesso!')
              #Metodo para alugar filme e subtrair o valor em questão da carteira
              print(f'Valor atual em sua carteira: $ {convidado1.calculaCreditos(filme_escolhido):.2f}')
              cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
              input('')
            else: #Else se o convidador não tiver dinheiro o suficiente
              print('')
              print('Você não tem créditos suficientes para alugar esse filme!')
              print('Para colocar mais créditos, acesse a opção 5) Ver Carteira.')
              cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
              input('')
          ###########################
        
        else: #Else se o filme não for encontrado
          print("Filme não encontrado.")
          cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
          input('')

############################################## Pesquisar Serie

      elif quest2 == '2':
        print('========================')
        print('      LISTA SÉRIES      ')
        print('========================')
        for s in series:
          print(f'- {s.getTitulo()}')
        print('========================')

        #Input para achar a série desejada na lista de séries pelo seu Titulo
        escolhe_serie = input(
            'Qual série você deseja saber informações? ').upper()
        print('')
        serie_escolhida = None
        for serie in series:
          if serie.getTitulo() == escolhe_serie:
            serie_escolhida = serie
            break
        if serie_escolhida:
          #Se achar a série printa a suas informações
          print('')
          print(f'Titulo: {serie_escolhida.getTitulo()}')
          print(f'Ano: {serie_escolhida.getAno()}')
          print(f'Genero: {serie_escolhida.genero.getName()}')
          print(
              f'Duração total: {serie_escolhida.calculaDuracaoTotal()} Minutos'
          )
          print(f'Preço aluguel da série: $ {serie_escolhida.getPreco():.2f}')
          print('')
          
          ################ Alugar Série
          aluguel2 = input('Deseja alugar a série? (s/n) ')
          if aluguel2 == 's':
            #If para verificar se o convidado tem dinheiro suficiente
            if (serie_escolhida.getPreco()) <= (convidado1.getCreditos()):
              alugueis.append(serie_escolhida)
              print('')
              print('Série alugada com sucesso!')
              #Metodo para alugar série e subtrair o valor em questão da carteira
              print(f'Valor atual em sua carteira: $ {convidado1.calculaCreditos(serie_escolhida):.2f}')
              cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
              input('')
            else: #Else se o convidador não tiver dinheiro o suficiente
              print('')
              print('Você não tem créditos suficientes para alugar essa série!')
              print('Para colocar mais créditos, acesse a opção 5) Ver Carteira.')
              cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
              input('')
          #########################
        
        else: #Else se a série não for encontrada
          print("Série não encontrada.")
          cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
          input('')

############################################## Pesquisar Diretor

      elif quest2 == '3':
        print('========================')
        print('        DIRETORES       ')
        print('========================')
        for d in diretores:
          print(f'- {d.getNome()}')
        print('========================')

        #Input para achar o diretor desejado na lista de diretores pelo seu Nome
        escolhe_diretor = input(
            'Digite o nome do diretor que deseja saber detalhes: ').upper()
        diretor_escolhido = None
        for diretor in diretores:
          if diretor.getNome() == escolhe_diretor:
            diretor_escolhido = diretor
            break
        if diretor_escolhido:
          #Se achar o diretor printa a suas informações
          print('')
          print(f'Nome: {diretor_escolhido.getNome()}')
          print(f'Idade: {diretor_escolhido.getIdade()}')
          print(f'Nacionalidade: {diretor_escolhido.getNacionalidade()}')
          print('')
          
          ######## Projetos do diretor #######
          projetos_diretor = [
              projeto.getTitulo() for projeto in filmes
              if isinstance(projeto, Filme)
              and projeto.getDiretor() == diretor_escolhido
          ]
          if projetos_diretor:
            print('=======================')
            print('       PROJETOS ')
            print('=======================')
            for projeto in projetos_diretor:
              print(f'- {projeto}')
            print('=======================')
            cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
            input('')
          else: #Else se o diretor não tiver nenhum projeto associado
            print('Nenhum projeto associado a este diretor encontrado.')
            cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
            input('')
          ################################
        
        else: #Else se o diretor não for encontrado
          print("Diretor não encontrado.")
          cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
          input('')

############################################## Pesquisar Genero

      elif quest2 == '4':
        print('======================')
        print('        GÊNEROS  ')
        print('======================')
        for g in generos:
          print(f'- {g.getName()}')
        print('======================')

        #Input para achar o gênero desejado na lista de genêros pelo seu Nome
        escolhe_genero = input(
            'Digite o nome do genêro que deseja saber detalhes: ').upper()
        genero_escolhido = None
        for genero in generos:
          if genero.getName() == escolhe_genero:
            genero_escolhido = genero
            break
        if genero_escolhido:
          #Se achar o gênero printa a suas informações
          print('')
          print(f'Nome: {genero_escolhido.getName()}')
          print(f'Informações: {genero_escolhido.getInfo()}')
          print('')
          
          ###### Projetos do genêro ########
          projetos_genero = [
              projeto.getTitulo()
              for projeto in filmes if projeto.getGenero() == genero_escolhido
          ] + [
              projeto.getTitulo()
              for projeto in series if projeto.getGenero() == genero_escolhido
          ]
          if projetos_genero:
            print('=======================')
            print('        PROJETOS       ')
            print('=======================')
            for projeto in projetos_genero:
              print(f'- {projeto}')
            print('=======================')
            cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
            input('')
          else: #Else se o genêro não tiver projetos associados
            print('Nenhum projeto associado a este gênero encontrado.')
            cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
            input('')
          ################################### 
        
        else: #Else se o gênero não for encontrado
          print("Gênero não encontrado.")
          cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
          input('')

############################################## Ver Carteira

      elif quest2 == '5':
        print(f'Valor atual em sua carteira: $ {convidado1.getCreditos():.2f}')
        print('')
        add_money = input('Deseja adicionar mais dinheiro? (s/n) ')
        if add_money == 's':
          print('')
          try:
            money = float(input('Quanto dinheiro deseja adicionar? $ '))
            print('')
            verifica_senha = input('***Digite a senha do login para aprovar a transação: ')
            #If verifica se a senha do convidado está correta
            if verifica_senha == convidado_senha:
              convidado1.maisCreditos(money) #Metodo para adicionar creditos
              print('')
              print('-----------------------------------------')
              print(f'Você adicionou $ {money:.2f} na sua carteira!')
              print(f'O valor atual em sua carteira é de $ {convidado1.getCreditos():.2f}')
              print('')
              cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
              input('')
            else: #Else se a senha do convidado estiver incorreta
              print('')
              print('Senha incorreta!')
              print('')
              cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
              input('')
          except ValueError: #Except algo for digitado errado
            print('')
            print('Você digitou algo errado.')
            print('É importante notar que você deve escrever valores decimais com PONTO e não VIRGULA.')
            print('')
            input('Tecle ENTER para voltar e tentar novamente.')
  
############################################## Alugueis

      elif quest2 == '6':
        #Printa os filmes e séries já alugados pelo convidado
        print('========================')
        print('        ALUGUÉIS        ')
        print('========================')
        for a in alugueis:
          print(f'- {a.getTitulo()}')
        print('========================')
        cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
        input('')

############################################## Fim programa

      elif quest2 == '7':
        print('Saiu do modo convidado!')
        print('')

############################################## Erro Comando Inválido

      else:
        print('')
        print('Comando Inválido! digite de 1 a 7 para a opção desejada.')
        cprint('\033[1m\033[3m' + msg_continuar, 'white', 'on_grey')
        input('')

############################################## Fim programa total

  elif login == '3':
    print('')
    print('''
⣶⡄⠀⣶⠀⢰⣶⣶⡆⠠⣶⣶⣶⡆⢰⣶⣶⣦⠀⣶⠀⠀⠀⣶⡆⠐⣶⠀⣰⡖
⣿⣷⡀⣿⠀⣸⣇⣀⡀⠀⠀⣿⠀⠀⢸⣇⣀⡀⠀⣿⠀⠀⠀⣿⡇⠀⠹⣷⡿⠁
⣿⡿⣷⣿⠀⣿⡟⠛⠁⠀⠀⣿⠀⠀⢸⡏⠉⠁⠀⣿⠀⠀⠀⣿⡇⠀⢠⣿⣇⠀
⣿⡇⢻⣿⠀⣿⣷⣶⡆⠀⠀⠿⠀⠀⠸⠇⠀⠀⠀⣿⣶⣶⠀⣿⡇⢀⣿⠋⢿⡆
⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
    ''')
    print('')
    print('Obrigado por utilizar.')
    print('Programa Encerrado!')


"""