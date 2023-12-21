from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)



@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/criar')
def create():
    return render_template('criar.html')

@app.route('/visualizar')
def read():
    return render_template('visualizar.html')

@app.route('/editar')
def update():
    return render_template('editar.html')

@app.route('/deletar')
def delete():
    return render_template('deletar.html')

if __name__ == "__main__":
    app.run(debug=True)
