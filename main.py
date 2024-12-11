from flask import Flask, g, request, render_template, redirect, session, flash, get_flashed_messages, jsonify
import sqlite3, random

app = Flask(__name__)

app.secret_key = 'chave_flask'

################################ #Cria a session onde o usuario pode ser acessado de todas routes

@app.context_processor
def inject_usuario_atual():
    usuario_atual = {
        'id': session.get('usuario_id'),
        'nome': session.get('usuario_nome'),
        'email': session.get('usuario_email'),
        'usuario': session.get('usuario_usuario')
    } if 'usuario_id' in session else None
    return {'usuario_atual': usuario_atual}

################################ SQL

# Conectar ao Banco de Dados
def conectar_db():
    conn = sqlite3.connect('bancoDeDados.db')
    return conn

def init_db():
    #cria as tabelas
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
                    sinopseFilme TEXT NOT NULL,
                    videoFilme TEXT NOT NULL,
                    diretorFilme TEXT NOT NULL,
                    duracaoFilme TEXT NOT NULL,
                    FOREIGN KEY (generoFilme) REFERENCES generos(nomeGenero),
                    FOREIGN KEY (diretorFilme) REFERENCES diretores(nomeDiretor)
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
                  sinopseSerie TEXT NOT NULL,
                  videoSerie TEXT NOT NULL,
                  temporadasSerie TEXT NOT NULL,
                  duracaoEpsSerie TEXT NOT NULL,
                  qntEpsTemporada TEXT NOT NULL,
                  FOREIGN KEY (generoSerie) REFERENCES generos(nomeGenero)
                )
                ''')
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS diretores(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nomeDiretor TEXT NOT NULL UNIQUE,
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
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nomeUsuario TEXT NOT NULL,
                   emailUsuario TEXT NOT NULL UNIQUE,
                   usuarioUsuario TEXT NOT NULL,
                   senhaUsuario TEXT NOT NULL
                   )
                   ''')

    conn.commit()
    conn.close()

init_db()

######################## def da barra de pesquisa

def buscar(termo):
    conn = conectar_db()
    cursor = conn.cursor()

    #pesquisa filme
    cursor.execute('SELECT * FROM filmes WHERE tituloFilme LIKE ?', ('%' + termo + '%',))
    filmes_data = cursor.fetchall()

    #pesqusia série
    cursor.execute('SELECT * FROM series WHERE tituloSerie LIKE ?', ('%' + termo + '%',))
    series_data = cursor.fetchall()

    conn.close()

    filmes = [
        {"id": id, "titulo": titulo, "poster": poster, "background": background}
        for (id, titulo, poster, background, _, _, _, _, _, _) in filmes_data
    ]

    series = [
        {"id": id, "titulo": titulo, "poster": poster, "background": background}
        for (id, titulo, poster, background, _, _, _, _, _, _, _) in series_data
    ]

    return filmes, series

################################ Classes de Projetos em POO

class Projeto():
    def __init__(self, id, titulo, poster, background, ano, Genero, sinopse, video):
        self.id = id
        self.titulo = titulo
        self.poster = poster
        self.background = background
        self.ano = ano
        self.genero = Genero #Associação
        self.sinopse = sinopse
        self.video = video

    def calculaDuracaoTotal(self):  # Polimorfismo
        pass

class Filme(Projeto):
    def __init__(self, id, titulo, poster, background, ano, Genero, sinopse, video, Diretor, duracao):
        super().__init__(id, titulo, poster, background, ano, Genero, sinopse, video)
        self.diretor = Diretor  #Associação
        self.duracao = duracao

    def calculaDuracaoTotal(self):  # Polimorfismo
        return self.duracao

class Serie(Projeto):
    def __init__(self, id, titulo, poster, background, ano, Genero, sinopse, video, temporadas, duracaoEps, qntEps):
        super().__init__(id, titulo, poster, background, ano, Genero, sinopse, video)
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
    def __init__(self, id, nome, email, usuario, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.usuario = usuario
        self.senha = senha

    @classmethod
    def autenticar(cls, usuario, senha): #Def para autenticar usuario no login
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM usuarios
            WHERE usuarioUsuario = ? AND senhaUsuario = ?
            ''', (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return cls(*resultado) #Retorna o obj usuario se autenticado
        return None
        
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'usuario': self.usuario,
            'senha': self.senha
        }


#####################################################################REGISTRO E LOGIN DE USUARIO
################################################### REGISTRO DE USUARIO

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    nome = request.form['nome']
    email = request.form['email']
    usuario = request.form['usuario']
    senha = request.form['senha']

    novo_usuario = Usuario(None, nome, email, usuario, senha)

    conn = conectar_db()
    cursor = conn.cursor()

    #Verifica se o email ou usuario já existem
    cursor.execute('SELECT * FROM usuarios WHERE emailUsuario = ? OR usuarioUsuario = ?', (email, usuario))
    if cursor.fetchone():
        msg = "E-mail ou usuário já cadastrado!"
        return render_template('registro.html', msgUsuarioCadastrado=msg)

    cursor.execute('''
        INSERT INTO usuarios (nomeUsuario, emailUsuario, usuarioUsuario, senhaUsuario)
        VALUES (?, ?, ?, ?)''',
        (novo_usuario.nome, novo_usuario.email, novo_usuario.usuario, novo_usuario.senha))
    
    conn.commit()
    conn.close()

    msgUsuarioCadastrado = "Usuario cadastrado com sucesso!"
    return render_template('registro.html', msgUsuarioCadastrado=msgUsuarioCadastrado)

################################################### PAGINA DE LOGIN DE USUARIO

@app.route('/login')
def login():
    return render_template('login.html')

##########pagina de perfil do usuario

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

##########def que verifica o login

@app.route('/login_user', methods=['POST'])
def login_user():
    usuario = request.form['usuario']
    senha = request.form['senha']

    usuario = Usuario.autenticar(usuario, senha)
    if usuario:
        #Autenticado com sucesso
        session['usuario_id'] = usuario.id #Salva ID na sessão
        session['usuario_nome'] = usuario.nome #Salva nome na sessão
        session['usuario_email'] = usuario.email #Salva email na sessão
        session['usuario_usuario'] = usuario.usuario #Salva usuario do usuario na sessão
        flash("Logado com sucesso!")
        return redirect('/homepage')
    else:
        session['msgUsuarioLogado'] = "Infelizmente o login não funcionou!"
        
    msgUsuarioLogado = session.pop('msgUsuarioLogado', None)  # Retira a mensagem da sessão
    return render_template('login.html', msgUsuarioLogado=msgUsuarioLogado)

################################################### Logout da conta

@app.route('/logout')
def logout():
    session.pop('usuario_atual', None) #Remove o usuario da sessão
    flash("Usuário deslogado com sucesso!", "info")
    session.clear()
    return redirect('/login')

#######################################CADASTRO DE DADOS FILMES/SÉRIES/DIRETORES/GENEROS

@app.route('/cadastro') #Cadastro de dados
def cadastro():
    if 'usuario_id' not in session:
        return redirect('/') #Redireciona pra pagina zero se o usuario nao estiver logado

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM diretores')
    diretores_data = cursor.fetchall()

    cursor.execute('SELECT * FROM generos')
    generos_data = cursor.fetchall() 

    conn.close()

    diretores = [Diretor(id, nome, idade, nacionalidade) for (id, nome, idade, nacionalidade) in diretores_data]

    generos = [Genero(id, name, info) for (id, name, info) in generos_data]

    return render_template('cadastro.html', generos=generos, diretores=diretores)

############ CADASTRO FILME
@app.route('/add_movie', methods=['POST'])  # Pega do HTML
def add_movie():
    titulo = request.form['titulo']
    poster = request.form['poster']
    background = request.form['background']
    ano = request.form['ano']
    genero = request.form['genero']
    sinopse = request.form['sinopse']
    video = request.form['video']
    diretor = request.form['diretor']
    duracao = request.form['duracao']

    novo_filme = Filme(None, titulo, poster, background, ano, genero, sinopse, video, diretor, duracao)  # None pq o id vai ser gerado pelo banco

    # Salva filme no banco SQL
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO filmes (tituloFilme, posterFilme, backgroundFilme, anoFilme, generoFilme, sinopseFilme, videoFilme, diretorFilme, duracaoFilme) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (novo_filme.titulo, novo_filme.poster, novo_filme.background, novo_filme.ano, novo_filme.genero, novo_filme.sinopse, novo_filme.video, novo_filme.diretor, novo_filme.duracao))
    
    cursor.execute('SELECT * FROM diretores')
    diretores_data = cursor.fetchall()

    cursor.execute('SELECT * FROM generos')
    generos_data = cursor.fetchall() 

    diretores = [Diretor(id, nome, idade, nacionalidade) for (id, nome, idade, nacionalidade) in diretores_data]

    generos = [Genero(id, name, info) for (id, name, info) in generos_data]
    
    conn.commit()
    conn.close()

    msgFilmeCadastrado = "Filme cadastrado com sucesso!"
    return render_template('cadastro.html', msgFilmeCadastrado=msgFilmeCadastrado, generos=generos, diretores=diretores)

############ CADASTRO SÉRIE
@app.route('/add_serie', methods=['POST'])
def add_serie():
    titulo = request.form['titulo']
    poster = request.form['poster']
    background = request.form['background']
    ano = request.form['ano']
    genero = request.form['genero']
    sinopse = request.form['sinopse']
    video = request.form['video']
    temporadas = request.form['temporadas']  
    duracaoEps = request.form['duracaoEps']
    qntEps = request.form['qntEps']

    nova_serie = Serie(None, titulo, poster, background, ano, genero, sinopse, video, temporadas, duracaoEps, qntEps)  # O id vai ser gerado pelo banco

    # Salva serie no banco SQL
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO series (tituloSerie, posterSerie, backgroundSerie, anoSerie, generoSerie, sinopseSerie, videoSerie, temporadasSerie, duracaoEpsSerie, qntEpsTemporada) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (nova_serie.titulo, nova_serie.poster, nova_serie.background, nova_serie.ano, nova_serie.genero, nova_serie.sinopse, nova_serie.video, nova_serie.temporadas, nova_serie.duracaoEps, nova_serie.qntEps))
    
    cursor.execute('SELECT * FROM diretores')
    diretores_data = cursor.fetchall()

    cursor.execute('SELECT * FROM generos')
    generos_data = cursor.fetchall() 

    diretores = [Diretor(id, nome, idade, nacionalidade) for (id, nome, idade, nacionalidade) in diretores_data]

    generos = [Genero(id, name, info) for (id, name, info) in generos_data]
    
    conn.commit()
    conn.close()

    msgSerieCadastrada = "Série cadastrada com sucesso!"
    return render_template('cadastro.html', msgSerieCadastrada=msgSerieCadastrada, generos=generos, diretores=diretores)

############ CADASTRO DIRETOR
@app.route('/add_diretor', methods=['POST'])
def add_diretor():
    nome = request.form['nome']
    idade = request.form['idade']
    nacionalidade = request.form['nacionalidade']

    #verificar se o diretor já existe
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM diretores WHERE nomeDiretor = ?', (nome,))
    diretor_existente = cursor.fetchone()

    if diretor_existente:
        msgDiretorCadastrado = "Este diretor já está cadastrado!"
        return render_template('cadastro.html', msgDiretorCadastrado=msgDiretorCadastrado)

    novo_diretor = Diretor(None, nome, idade, nacionalidade)

    #Salva Diretor no banco SQL
    cursor.execute('''
        INSERT INTO diretores (nomeDiretor, idadeDiretor, nacionalidadeDiretor)
        VALUES (?, ?, ?)''',
        (novo_diretor.nome, novo_diretor.idade, novo_diretor.nacionalidade))
    
    cursor.execute('SELECT * FROM diretores')
    diretores_data = cursor.fetchall()

    cursor.execute('SELECT * FROM generos')
    generos_data = cursor.fetchall() 

    diretores = [Diretor(id, nome, idade, nacionalidade) for (id, nome, idade, nacionalidade) in diretores_data]

    generos = [Genero(id, name, info) for (id, name, info) in generos_data]

    conn.commit()
    conn.close()

    msgDiretorCadastrado = "Diretor cadastrado com sucesso!"
    return render_template('cadastro.html', msgDiretorCadastrado=msgDiretorCadastrado, generos=generos, diretores=diretores)

############ CADASTRO GENERO
@app.route('/add_genero', methods=['POST'])
def add_genero():
    name = request.form['name']
    info = request.form['info']
    
    novo_genero = Genero(None, name, info)

    #Salva genero no banco SQL
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO generos (nomeGenero, infoGenero)
        VALUES (?, ?)''',
        (novo_genero.name, novo_genero.info))
    
    cursor.execute('SELECT * FROM diretores')
    diretores_data = cursor.fetchall()

    cursor.execute('SELECT * FROM generos')
    generos_data = cursor.fetchall() 

    diretores = [Diretor(id, nome, idade, nacionalidade) for (id, nome, idade, nacionalidade) in diretores_data]

    generos = [Genero(id, name, info) for (id, name, info) in generos_data]
    
    conn.commit()
    conn.close()

    msgGeneroCadastrado = "Gênero cadastrado com sucesso!"
    return render_template('cadastro.html', msgGeneroCadastrado=msgGeneroCadastrado, generos=generos, diretores=diretores)

#######################################################################################
################################################### Atualizar dados da tabela pelo HTML
#################### Verifica os registros na database

@app.route('/ver_registros/<string:tabela>')
def ver_registros(tabela):
    if 'usuario_id' not in session:
        return redirect('/') #Redireciona pra pagina zero se o usuario nao estiver logado

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
    if 'usuario_id' not in session:
        return redirect('/') #Redireciona pra pagina zero se o usuario nao estiver logado

    #Acessa o banco
    conn = sqlite3.connect('bancoDeDados.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        #Pega os nomes das colunas
        cursor.execute(f"PRAGMA table_info({tabela})")
        #Armazena as colunas em uma lista
        colunas = [col[1] for col in cursor.fetchall()][1:]  #O [1:] ignora o primeiro elemento, no caso o ID

        #Pega os novos valores atualizados no html
        valores = [request.form[col] for col in colunas]

        #Gera uma string de atualização para o sql
        set_clause = ", ".join([f"{col} = ?" for col in colunas])
        #Atualiza no banco
        query = f"UPDATE {tabela} SET {set_clause} WHERE id = ?"
        cursor.execute(query, valores + [id])
        conn.commit()
        conn.close()
        return redirect(f'/ver_registros/{tabela}')

    #Busca os dados existentes pra preencher o formulário
    cursor.execute(f"SELECT * FROM {tabela} WHERE id = ?", (id,))
    registro = cursor.fetchone()

    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [col[1] for col in cursor.fetchall()]

    conn.close()
    return render_template('editar_registro.html', registro=registro, colunas=colunas, tabela=tabela)

##############################################################################################################
##############################################################################################################
##############################################################################################################
####################################### EXIBIÇÃO FINAL DE PÁGINAS

@app.route('/')
def screen_zero():
    return render_template('screen_zero.html')

################################################### Listar Filmes, Séries, Diretores e Gêneros na homepage
@app.route('/homepage') 
def listar_filmes():
    if 'usuario_id' not in session:
        return redirect('/') #Redireciona pra pagina zero se o usuario nao estiver logado

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

    filmes = [Filme(id, titulo, poster, background, ano, genero, sinopse, video, diretor, duracao) for (id, titulo, poster, background, ano, genero, sinopse, video, diretor, duracao) in filmes_data]

    series = [Serie(id, titulo, poster, background, ano, genero, sinopse, video, temporadas, duracaoEps, qntEps) for (id, titulo, poster, background, ano, genero, sinopse, video, temporadas, duracaoEps, qntEps) in series_data]

    diretores = [Diretor(id, nome, idade, nacionalidade) for (id, nome, idade, nacionalidade) in diretores_data]

    generos = [Genero(id, name, info) for (id, name, info) in generos_data]

    termo = request.args.get('termo', '').lower()
    filmes, series = buscar(termo) #chama a função de busca


    # Selecionar itens aleatórios
    filmes_aleatorios = random.sample(filmes, min(2, len(filmes)))  #maximo de 5 itens ou a quantidade disponível
    series_aleatorias = random.sample(series, min(2, len(series)))

    msgUsuarioLogado = session.pop('msgUsuarioLogado', None)  # Retira a mensagem da sessão
    mensagens = get_flashed_messages()  # Obtém as mensagens flash
    return render_template('homepage.html', filmes=filmes, series=series, diretores=diretores, generos=generos, mensagens=mensagens, termo=termo, filmes_aleatorios=filmes_aleatorios, series_aleatorias=series_aleatorias)

######################################################PAGINAS SEPARADAS PARA VER TODOS FILMES/SÉRIES
################################################### Listar Filmes na aba Filmes.html
@app.route('/filmes') 
def listar_filmes_in_filmes():
    if 'usuario_id' not in session:
        return redirect('/') #Redireciona pra pagina zero se o usuario nao estiver logado

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM filmes')
    filmes_data = cursor.fetchall()

    conn.close()

    filmes = [Filme(id, titulo, poster, background, ano, genero, sinopse, video, diretor, duracao) for (id, titulo, poster, background, ano, genero, sinopse, video, diretor, duracao) in filmes_data]

    return render_template('filmes.html', filmes=filmes)

################################################### Listar Séries na aba Series.html
@app.route('/series')
def listar_series_in_series():
    if 'usuario_id' not in session:
        return redirect('/') #Redireciona pra pagina zero se o usuario nao estiver logado

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM series')
    series_data = cursor.fetchall()

    conn.close()

    series = [Serie(id, titulo, poster, background, ano, genero, sinopse, video, temporadas, duracaoEps, qntEps) for (id, titulo, poster, background, ano, genero, sinopse, video, temporadas, duracaoEps, qntEps) in series_data]

    return render_template('series.html', series=series)

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
                      filme_data[6], filme_data[7], filme_data[8],
                      filme_data[9])
        return render_template('projeto.html', filme=filme)

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
                      serie_data[9], serie_data[10])
        return render_template('projeto.html', serie=serie)

    return "Série não encontrada", 404

################################################### Player do video das séries

@app.route('/player/serie/<int:id>')
def playerSerie(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM series WHERE ID = ?', (id,))
    serie_data = cursor.fetchone()

    if serie_data:
        serie = Serie(serie_data[0], serie_data[1], serie_data[2],
                        serie_data[3], serie_data[4], serie_data[5],
                        serie_data[6], serie_data[7], serie_data[8],
                        serie_data[9], serie_data[10])
        return render_template('player.html', serie=serie)
    
################################################### Player do video dos filmes

@app.route('/player/filme/<int:id>')
def playerFilme(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filmes WHERE ID = ?', (id,))
    filme_data = cursor.fetchone()

    if filme_data:
        filme = Filme(filme_data[0], filme_data[1], filme_data[2],
                      filme_data[3], filme_data[4], filme_data[5],
                      filme_data[6], filme_data[7], filme_data[8],
                      filme_data[9])
        return render_template('player.html', filme=filme)
    
##########################################

@app.route('/api/busca', methods=['GET'])
def api_busca():
    termo = request.args.get('termo', '').lower()
    filmes, series = buscar(termo) #chama a função de busca pra dentro da API

    return jsonify({"filmes": filmes, "series": series})

###########################################

@app.route('/resultados')
def resultados():
    if 'usuario_id' not in session:
        return redirect('/') #Redireciona pra pagina zero se o usuario nao estiver logado

    termo = request.args.get('termo', '').lower()  #Obtem o termo da busca da URL
    
    if termo:
        filmes, series = buscar(termo)  #Chama a função de busca pra obter os resultados
    else:
        filmes, series = [], []  #Se não tiver termo retorna uma lista vazia pros filmes e séries
    
    return render_template('resultados.html', filmes=filmes, series=series, termo=termo)

#####Debug para ver se está tudo certo

if __name__ == '__main__':
    app.run(debug=True)