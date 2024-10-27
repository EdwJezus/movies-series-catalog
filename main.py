from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

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
    return render_template('cadastro.html')

################################ Classes de Herança

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
    def __init__(self, nome, idade, nacionalidade):
        self.nome = nome
        self.idade = idade
        self.nacionalidade = nacionalidade

class Genero():
    def __init__(self, name, info):
        self.name = name
        self.info = info

################################ Cadastro integrado com HTML

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

################################################### Listar Filmes e Séries na homepage
@app.route('/homepage') 
def listar_filmes():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM filmes')
    filmes_data = cursor.fetchall()

    cursor.execute('SELECT * FROM series')
    series_data = cursor.fetchall()

    conn.close()

    filmes = [Filme(id, titulo, poster, background, ano, genero, preco, diretor, duracao) for (id, titulo, poster, background, ano, genero, preco, diretor, duracao) in filmes_data]

    series = [Serie(id, titulo, poster, background, ano, genero, preco, temporadas, duracaoEps, qntEps) for (id, titulo, poster, background, ano, genero, preco, temporadas, duracaoEps, qntEps) in series_data]

    return render_template('homepage.html', filmes=filmes, series=series)

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
                      serie_data[9])
        return render_template('projeto.html', serie=serie)

    return "Série não encontrada", 404

#####Debug para ver se está tudo certo
if __name__ == '__main__':
    app.run(debug=True)