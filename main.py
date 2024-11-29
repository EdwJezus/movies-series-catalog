from flask import Flask, g, request, render_template, redirect, session, flash
import sqlite3

app = Flask(__name__)

app.secret_key = 'chave_flask'

################################

'''
@app.before_request
def load_logedg_in_user():
    usuario_atual_dict = session.get('usuario_atual')
    if usuario_atual_dict:
        usuario_atual = Usuario(**usuario_atual_dict)
    else:
        usuario_atual = None

    g.usuario_atual = usuario_atual
'''
@app.before_request
def load_logged_in_user():
    usuario_atual_dict = session.get('usuario_atual')
    if usuario_atual_dict:
        g.usuario_atual = Usuario(**usuario_atual_dict)
    else:
        g.usuario_atual = None


################################ SQL

# Conectar ao Banco de Dados
def conectar_db():
    conn = sqlite3.connect('bancoDeDados.db')
    return conn

def init_db():
    # Criar uma tabela
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS filmes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tituloFilme TEXT NOT NULL,
                    posterFilme TEXT NOT NULL,
                    backgroundFilme TEXT NOT NULL,
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
                  backgroundSerie TEXT NOT NULL,
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

init_db()

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', usuario_atual=g.usuario_atual)

################################ Classes de Projetos

class Projeto():
    def __init__(self, id, titulo, poster, background, ano, Genero, preco):
        self.id = id
        self.titulo = titulo
        self.poster = poster
        self.background = background
        self.ano = ano
        self.genero = Genero #Associação
        self.preco = preco

    def calculaDuracaoTotal(self):  # Polimorfismo
        pass

class Filme(Projeto):
    def __init__(self, id, titulo, poster, background, ano, Genero, preco, Diretor, duracao):
        super().__init__(id, titulo, poster, background, ano, Genero, preco)
        self.diretor = Diretor  #Associação
        self.duracao = duracao

    def calculaDuracaoTotal(self):  # Polimorfismo
        return self.duracao

class Serie(Projeto):
    def __init__(self, id, titulo, poster, background, ano, Genero, preco, temporadas, duracaoEps, qntEps):
        super().__init__(id, titulo, poster, background, ano, Genero, preco)
        self.temporadas = temporadas
        self.duracaoEps = duracaoEps
        self.qntEps = qntEps

    def calculaDuracaoTotal(self):  # Polimorfismo
        return self.temporadas * self.duracaoEps * self.qntEps
    
class Diretor():
    def __init__(self, id, nome, idade, nacionalidade):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.nacionalidade = nacionalidade

class Genero():
    def __init__(self, id, name, info):
        self.id = id
        self.name = name
        self.info = info

################################ Classe de Usuario

class Usuario():
    def __init__(self, nome, email, usuario, senha):
        self.nome = nome
        self.email = email
        self.usuario = usuario
        self.senha = senha

    def to_dict(self):
        return {
            'nome': self.nome,
            'email': self.email,
            'usuario': self.usuario,
            'senha': self.senha
        }

################################ Cadastro integrado com HTML

@app.route('/player')
def player():
    return render_template('player.html')

############ REGISTRO DE USUARIO

#novo_usuario = Usuario(None, None, None, None)
#usuario_para_login = Usuario(None, None, None, None)

usuarios_registrados = []

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    nome = request.form['nome']
    email = request.form['email']
    usuario = request.form['usuario']
    senha = request.form['senha']

    novo_usuario = Usuario(nome, email, usuario, senha)
    usuarios_registrados.append(novo_usuario)

    #msgUsuarioRegistrado = "Usuário registrado com sucesso!"
    #return render_template('registro.html', msgUsuarioRegistrado=msgUsuarioRegistrado)
    return redirect('/login')
    
############ LOGIN DE USUARIO

@app.route('/login')
def login():
    return render_template('login.html')

#usuario_atual = None

@app.route('/login_user', methods=['POST'])
def login_user():
    usuario = request.form['usuario']
    senha = request.form['senha']

    usuario_encontrado = None
    for i in usuarios_registrados:
        if i.usuario == usuario and i.senha == senha:
            usuario_encontrado = i
            break

    if usuario_encontrado:
        ##msgUsuarioLogado = "Usuário logado com sucesso!"
        flash("Usuário logado com sucesso!", "success")
        session['usuario_atual'] = usuario_encontrado.to_dict()
        return redirect('/homepage')
    else:
        msgUsuarioLogado = "Infelizmente o login não funcionou!"
    return render_template('login.html', msgUsuarioLogado=msgUsuarioLogado)
        #flash("Infelizmente o login não funcionou!", "danger")
    #return redirect('/login')

'''
    usuario_para_login = Usuario(None, None, usuario, senha)

    if usuario_para_login.usuario == novo_usuario.usuario and usuario_para_login.senha == novo_usuario.senha:
        msgUsuarioLogado = "Usuário logado com sucesso!"
    else:
        msgUsuarioLogado = "Infelizmente o login não funcionou!"
    return render_template('login.html', msgUsuarioLogado=msgUsuarioLogado)
'''

############ CADASTRO FILME
@app.route('/add_movie', methods=['POST'])  # Pega do HTML
def add_movie():
    titulo = request.form['titulo']
    poster = request.form['poster']
    background = request.form['background']
    ano = request.form['ano']
    genero = request.form['genero']
    preco = request.form['preco']
    diretor = request.form['diretor']
    duracao = request.form['duracao']

    novo_filme = Filme(None, titulo, poster, background, ano, genero, preco, diretor, duracao)  # None pois o id será gerado pelo banco

    # Salva filme no banco SQL
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO filmes (tituloFilme, posterFilme, backgroundFilme, anoFilme, generoFilme, precoFilme, diretorFilme, duracaoFilme) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
        (novo_filme.titulo, novo_filme.poster, novo_filme.background, novo_filme.ano, novo_filme.genero, novo_filme.preco, novo_filme.diretor, novo_filme.duracao))
    
    conn.commit()
    conn.close()

    ##return "Filme cadastrado com sucesso!"

    msgFilmeCadastrado = "Filme cadastrado com sucesso!"
    return render_template('cadastro.html', msgFilmeCadastrado=msgFilmeCadastrado)

############ CADASTRO SÉRIE
@app.route('/add_serie', methods=['POST'])
def add_serie():
    titulo = request.form['titulo']
    poster = request.form['poster']
    background = request.form['background']
    ano = request.form['ano']
    genero = request.form['genero']
    preco = request.form['preco']
    temporadas = request.form['temporadas']  
    duracaoEps = request.form['duracaoEps']
    qntEps = request.form['qntEps']

    nova_serie = Serie(None, titulo, poster, background, ano, genero, preco, temporadas, duracaoEps, qntEps)  # O id será gerado pelo banco

    # Salva série no banco SQL
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO series (tituloSerie, posterSerie, backgroundSerie, anoSerie, generoSerie, precoSerie, temporadasSerie, duracaoEpsSerie, qntEpsSerie) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (nova_serie.titulo, nova_serie.poster, nova_serie.background, nova_serie.ano, nova_serie.genero, nova_serie.preco, nova_serie.temporadas, nova_serie.duracaoEps, nova_serie.qntEps))
    
    conn.commit()
    conn.close()

    ##return "Série cadastrada com sucesso!"

    msgSerieCadastrada = "Série cadastrada com sucesso!"
    return render_template('cadastro.html', msgSerieCadastrada=msgSerieCadastrada)

############ CADASTRO DIRETOR
@app.route('/add_diretor', methods=['POST'])
def add_diretor():
    nome = request.form['nome']
    idade = request.form['idade']
    nacionalidade = request.form['nacionalidade']

    novo_diretor = Diretor(None, nome, idade, nacionalidade)

    # Salva Diretor no banco SQL
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO diretores (nomeDiretor, idadeDiretor, nacionalidadeDiretor)
        VALUES (?, ?, ?)''',
        (novo_diretor.nome, novo_diretor.idade, novo_diretor.nacionalidade))
    
    conn.commit()
    conn.close()

    msgDiretorCadastrado = "Diretor cadastrado com sucesso!"
    return render_template('cadastro.html', msgDiretorCadastrado=msgDiretorCadastrado)

############ CADASTRO GENERO
@app.route('/add_genero', methods=['POST'])
def add_genero():
    name = request.form['name']
    info = request.form['info']
    
    novo_genero = Genero(None, name, info)

    # Salva genero no banco SQL
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO generos (nomeGenero, infoGenero)
        VALUES (?, ?)''',
        (novo_genero.name, novo_genero.info))
    
    conn.commit()
    conn.close()

    msgGeneroCadastrado = "Gênero cadastrado com sucesso!"
    return render_template('cadastro.html', msgGeneroCadastrado=msgGeneroCadastrado)

################################################### Listar Filmes, Séries, Diretores e Gêneros na homepage
@app.route('/homepage') 
def listar_filmes():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM filmes')
    filmes_data = cursor.fetchall()

    cursor.execute('SELECT * FROM series')
    series_data = cursor.fetchall()

    cursor.execute('SELECT * FROM diretores')
    diretores_data = cursor.fetchall()

    cursor.execute('SELECT * FROM generos')
    generos_data = cursor.fetchall() 

    conn.close()

    filmes = [Filme(id, titulo, poster, background, ano, genero, preco, diretor, duracao) for (id, titulo, poster, background, ano, genero, preco, diretor, duracao) in filmes_data]

    series = [Serie(id, titulo, poster, background, ano, genero, preco, temporadas, duracaoEps, qntEps) for (id, titulo, poster, background, ano, genero, preco, temporadas, duracaoEps, qntEps) in series_data]

    diretores = [Diretor(id, nome, idade, nacionalidade) for (id, nome, idade, nacionalidade) in diretores_data]

    generos = [Genero(id, name, info) for (id, name, info) in generos_data]

    '''

    usuario_atual_dict = session.get('usuario_atual') #Recupera o usuário da sessão
    if usuario_atual_dict:
        usuario_atual = Usuario(**usuario_atual_dict) # Cria o objeto Usuario a partir do dicionário
    else:
        usuario_atual = None

        '''

    ##return render_template('homepage.html', filmes=filmes, series=series)
    return render_template('homepage.html', filmes=filmes, series=series, diretores=diretores, generos=generos, usuario_atual=g.usuario_atual)

################################################### Logout

@app.route('/logout')
def logout():
    session.pop('usuario_atual', None) #Remove o usuário da sessão
    flash("Usuário deslogado com sucesso!", "info")
    return redirect('/login')

################################################### Detalhes do Filme na aba projeto.html
@app.route('/filme/<int:id>')
def descricao_filme(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filmes WHERE id = ?', (id,))
    filme_data = cursor.fetchone()
    
    if filme_data:
        filme = Filme(filme_data[0], filme_data[1], filme_data[2],
                      filme_data[3], filme_data[4], filme_data[5],
                      filme_data[6], filme_data[7], filme_data[8])
        return render_template('projeto.html', filme=filme, usuario_atual=g.usuario_atual)

    return "Filme não encontrado", 404

################################################### Detalhes da Série na aba projeto.html
@app.route('/serie/<int:id>')
def descricao_serie(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM series WHERE id = ?', (id,))
    serie_data = cursor.fetchone()
    
    if serie_data:
        serie = Serie(serie_data[0], serie_data[1], serie_data[2],
                      serie_data[3], serie_data[4], serie_data[5],
                      serie_data[6], serie_data[7], serie_data[8],
                      serie_data[9])
        return render_template('projeto.html', serie=serie, usuario_atual=g.usuario_atual)

    return "Série não encontrada", 404

################################################### Listar Filmes na aba Filmes.html
@app.route('/filmes') 
def listar_filmes_in_filmes():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM filmes')
    filmes_data = cursor.fetchall()

    conn.close()

    filmes = [Filme(id, titulo, poster, background, ano, genero, preco, diretor, duracao) for (id, titulo, poster, background, ano, genero, preco, diretor, duracao) in filmes_data]

    return render_template('filmes.html', filmes=filmes, usuario_atual=g.usuario_atual)

################################################### Listar Séries na aba Series.html
@app.route('/series')
def listar_series_in_series():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM series')
    series_data = cursor.fetchall()

    conn.close()

    series = [Serie(id, titulo, poster, background, ano, genero, preco, temporadas, duracaoEps, qntEps) for (id, titulo, poster, background, ano, genero, preco, temporadas, duracaoEps, qntEps) in series_data]

    return render_template('series.html', series=series, usuario_atual=g.usuario_atual)

################################################### Atualizar dados da tabela pelo HTML
################### Verifica os registros na database

@app.route('/ver_registros/<string:tabela>')
def ver_registros(tabela):
    #Acessa o banco
    conn = sqlite3.connect('bancoDeDados.db')
    cursor = conn.cursor()
    #Pega os nomes das colunas
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [col[1] for col in cursor.fetchall()]
    #Pega os dados da tabela
    cursor.execute(f"SELECT * FROM {tabela}") #Pega a tabela especifica
    registros = cursor.fetchall()
    conn.close()
    #Envia tudo
    return render_template('ver_registros.html', registros=registros, colunas=colunas, tabela=tabela)


#################### Edita os registros na database

@app.route('/editar/<string:tabela>/<int:id>', methods=['GET', 'POST'])
def editar_registro(tabela, id):
    #Acessa o banco
    conn = sqlite3.connect('bancoDeDados.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        #Pega os nomes das colunas
        cursor.execute(f"PRAGMA table_info({tabela})")
        #Armazena as colunas em uma lista
        colunas = [col[1] for col in cursor.fetchall()][1:]  #O [1:] Ignora o primeiro elemento, no caso o ID

        #Pega os novos valores atualizados no html
        valores = [request.form[col] for col in colunas]

        #Gera uma string de atualização para o sql
        set_clause = ", ".join([f"{col} = ?" for col in colunas])
        # Atualiza no banco
        query = f"UPDATE {tabela} SET {set_clause} WHERE id = ?"
        cursor.execute(query, valores + [id])
        conn.commit()
        conn.close()
        return redirect(f'/ver_registros/{tabela}')

    # Busca os dados existentes para preencher o formulário
    cursor.execute(f"SELECT * FROM {tabela} WHERE id = ?", (id,))
    registro = cursor.fetchone()

    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [col[1] for col in cursor.fetchall()]

    conn.close()
    return render_template('editar_registro.html', registro=registro, colunas=colunas, tabela=tabela)


#####Debug para ver se está tudo certo
if __name__ == '__main__':
    app.run(debug=True)