from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurando o banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
db = SQLAlchemy(app)

# Modelo do Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

# Rota principal para listar produtos
@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

# Adicionar novo produto
@app.route('/add', methods=['POST'])
def add():
    nome = request.form.get('nome')
    quantidade = request.form.get('quantidade')
    novo_produto = Produto(nome=nome, quantidade=quantidade)
    db.session.add(novo_produto)
    db.session.commit()
    return redirect(url_for('index'))

# Atualizar produto
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    produto = Produto.query.get(id)
    produto.nome = request.form.get('nome')
    produto.quantidade = request.form.get('quantidade')
    db.session.commit()
    return redirect(url_for('index'))

# Deletar produto
@app.route('/delete/<int:id>')
def delete(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Criar o banco de dados antes de rodar o servidor
    db.create_all()
    app.run(debug=True)
