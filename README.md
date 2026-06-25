# 🎬 Catálogo de Filmes e Séries (Flask + SQLite)

Este projeto implementa uma aplicação web para gerenciamento e visualização de filmes e séries utilizando Python, Flask, SQLite, HTML e CSS. O sistema permite cadastro e autenticação de usuários, gerenciamento de conteúdo, busca dinâmica e visualização detalhada de filmes e séries.

---

## 📁 Estrutura do Projeto

```text
.
├── static/
│   └── images/             # Imagens utilizadas pela aplicação
├── templates/              # Páginas HTML da aplicação
├── bancoDeDados.db         # Banco de dados SQLite
├── requirements.txt        # Dependências do projeto
├── main.py                 # Aplicação principal Flask
└── README.md               # Este documento
```

---

## 🎯 Funcionalidades

- Cadastro e login de usuários
- Sistema de sessões com Flask
- Cadastro de filmes, séries, diretores e gêneros
- Edição de registros diretamente pela interface
- Busca por filmes e séries
- Visualização detalhada de informações
- Reprodução de trailers e vídeos
- API para pesquisa de conteúdos
- Seleção aleatória de destaques na página inicial

---

## 🚀 Como Executar

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Iniciar a aplicação

```bash
python main.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

---

## 🧠 Como Funciona

- Os dados são armazenados em um banco de dados SQLite.
- O Flask é responsável pelas rotas, sessões e renderização das páginas.
- O sistema utiliza Programação Orientada a Objetos para representar filmes, séries, usuários, diretores e gêneros.
- A busca é realizada diretamente no banco de dados e pode retornar filmes e séries relacionados ao termo pesquisado.
- O acesso às funcionalidades administrativas é controlado por autenticação de usuário.

---

## 📌 Recursos Implementados

✔ Sistema de autenticação de usuários

✔ CRUD de filmes, séries, diretores e gêneros

✔ Busca dinâmica de conteúdo

✔ API de pesquisa em formato JSON

✔ Controle de sessão e perfil de usuário

✔ Relacionamentos entre entidades utilizando banco de dados relacional

✔ Aplicação desenvolvida utilizando conceitos de Programação Orientada a Objetos

---

## 🎓 Conceitos Aplicados

- Herança
- Polimorfismo
- Associação entre classes
- Encapsulamento
- CRUD com SQLite
- Desenvolvimento Web com Flask
- Sessões e autenticação de usuários

---

## 🧪 Tecnologias Utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Programação Orientada a Objetos (POO)

---

## 📜 Licença

MIT License © Eduardo Jesus
