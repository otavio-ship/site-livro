from flask import Flask, render_template, request, flash, redirect, url_for
import fdb

app = Flask(__name__)
app.secret_key = 'qualquercoisa'

# Configurações do banco de dados
host = 'localhost'
database = r'C:\Users\Aluno\Desktop\BANCO\BANCO.fdb'
user = 'SYSDBA'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Listagem de livros
@app.route('/livro')
def livro():
    cursor = con.cursor()
    cursor.execute("SELECT ID_LIVRO, TITULO, AUTOR, ANO_PUBLICACAO FROM LIVRO")
    livros = cursor.fetchall()
    cursor.close()
    return render_template('livros.html', livros=livros)

# Formulário de novo livro
@app.route('/novo')
def novo():
    return render_template('novo.html', titulo="Novo Livro")

# Formulário de novo usuário
@app.route('/novousuario')
def novousuario():
    return render_template('novousuario.html', titulo="Novo Usuário")

# Criação de novo livro
@app.route('/criar', methods=["POST"])
def criar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    cursor = con.cursor()
    try:
        cursor.execute('SELECT 1 FROM LIVRO WHERE TITULO = ?', (titulo,))
        if cursor.fetchone():
            flash('Esse livro já está cadastrado.')
            return redirect(url_for('novo'))

        cursor.execute('INSERT INTO LIVRO (TITULO, AUTOR, ANO_PUBLICACAO) VALUES (?, ?, ?)',
                       (titulo, autor, ano_publicacao))
        con.commit()
        flash('O livro foi cadastrado com sucesso.')
    finally:
        cursor.close()

    return redirect(url_for('livro'))

# Criação de novo usuário
@app.route('/criarusuario', methods=["POST"])
def criarusuario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    cursor = con.cursor()
    try:
        cursor.execute('SELECT 1 FROM USUARIOS WHERE EMAIL = ?', (email,))
        if cursor.fetchone():
            flash('Esse usuário já está cadastrado.')
            return redirect(url_for('novousuario'))

        cursor.execute('INSERT INTO USUARIOS (NOME, EMAIL, SENHA) VALUES (?, ?, ?)',
                       (nome, email, senha))
        con.commit()
        flash('Usuário cadastrado com sucesso.')
    finally:
        cursor.close()

    return redirect(url_for('usuarios'))

# Edição de livro
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = con.cursor()
    cursor.execute("SELECT ID_LIVRO, TITULO, AUTOR, ANO_PUBLICACAO FROM LIVRO WHERE ID_LIVRO = ?", (id,))
    livro = cursor.fetchone()
    cursor.close()

    if not livro:
        flash("Livro não encontrado.")
        return redirect(url_for('livro'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano_publicacao = request.form['ano_publicacao']

        cursor = con.cursor()
        cursor.execute("UPDATE LIVRO SET TITULO = ?, AUTOR = ?, ANO_PUBLICACAO = ? WHERE ID_LIVRO = ?",
                       (titulo, autor, ano_publicacao, id))
        con.commit()
        cursor.close()
        flash("Livro atualizado com sucesso.")
        return redirect(url_for('livro'))

    return render_template('editar.html', livro=livro, titulo='Editar Livro')

# Edição de usuário
@app.route('/editarusuario/<int:id>', methods=['GET', 'POST'])
def editarusuario(id):
    cursor = con.cursor()
    cursor.execute("SELECT ID_USUARIO, NOME, EMAIL, SENHA FROM USUARIOS WHERE ID_USUARIO = ?", (id,))
    usuario = cursor.fetchone()
    cursor.close()

    if not usuario:
        flash("Usuário não encontrado.")
        return redirect(url_for('usuarios'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        cursor = con.cursor()
        cursor.execute("UPDATE USUARIOS SET NOME = ?, EMAIL = ?, SENHA = ? WHERE ID_USUARIO = ?",
                       (nome, email, senha, id))
        con.commit()
        cursor.close()
        flash("Usuário atualizado com sucesso.")
        return redirect(url_for('usuarios'))

    return render_template('editarusuario.html', usuario=usuario, titulo='Editar Usuário')



# Deletar livro
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    cursor = con.cursor()
    cursor.execute("DELETE FROM LIVRO WHERE ID_LIVRO = ?", (id,))
    con.commit()
    cursor.close()
    flash("Livro excluído com sucesso.")
    return redirect(url_for('livro'))

# Deletar usuário
@app.route('/deletarusuario/<int:id>', methods=['POST'])
def deletarusuario(id):
    cursor = con.cursor()
    cursor.execute("DELETE FROM USUARIOS WHERE ID_USUARIO = ?", (id,))
    con.commit()
    cursor.close()
    flash("Usuário excluído com sucesso.")
    return redirect(url_for('usuarios'))

# Listagem de usuários
@app.route('/usuarios')
def usuarios():
    cursor = con.cursor()
    cursor.execute("SELECT ID_USUARIO, NOME, EMAIL, SENHA FROM USUARIOS")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('usuarios.html', usuarios=usuarios)

# Abrir tela de login
@app.route('/abrirlogin')
def abrirlogin():
    return render_template('login.html')

# Login de usuário
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    cursor = con.cursor()
    try:
        cursor.execute('SELECT 1 FROM USUARIOS WHERE EMAIL = ? AND SENHA = ?', (email, senha))
        if cursor.fetchone():
            flash('Login realizado com sucesso.')
            return redirect(url_for('usuarios'))
        else:
            flash('Email ou senha incorretos.')
            return redirect(url_for('abrirlogin'))
    finally:
        cursor.close()

# Roda o app
if __name__ == '__main__':
    app.run(debug=True)