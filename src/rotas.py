from flask import flash, request, redirect, url_for, render_template
from app import app, db_connection

#Pagina Inicial 
@app.route('/')
def inicio():
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM NOTAS")
    notas = cursor.fetchall()
    cursor.close()
    
    return render_template('inicio.html', notas = notas)

#Renderiza a pagina de criar nota
@app.route('/nova_nota')
def nova_nota():
    return render_template('criar.html')

#Rota para inserir nova nota 
@app.route('/create', methods = ['POST', 'GET'])
def create():
    if request.method == 'POST':

        titulo_novo = request.form['titulo']
        conteudo_novo = request.form['conteudo']

        if len(titulo_novo) > 30:
            flash('O titulo ultrapassou o limite permitido!')
            return redirect (url_for('editar', id_nota = id_nota))
        if len(conteudo_novo) > 1000:
            flash('O conteudo ultrapassou o limite permitido!')
            return redirect (url_for('editar', id_nota = id_nota))

        else:
            cursor =  db_connection.cursor()
            cursor.execute ('INSERT INTO NOTAS (TITULO_NOTAS, CONTEUDO_NOTAS) VALUES(%s, %s) ', (titulo_novo, conteudo_novo))
            db_connection.commit()

            cursor =  db_connection.cursor()
            cursor.execute('SELECT * FROM NOTAS ORDER BY DATA_NOTA DESC LIMIT 1')
            resultado = cursor.fetchone()

            id_nota = resultado[0]
            flash('Nota criada com sucesso!')
            return redirect(url_for('read', id_nota = id_nota))
    return render_template('criar.html')
        

#Mostra o conteudo da nota que acessada
@app.route('/visualizar/<int:id_nota>')
def read(id_nota):
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM NOTAS WHERE ID_NOTAS = %s' , (id_nota,))
    nota = cursor.fetchone()
    cursor.close()
    return render_template('visualizar.html' , nota = nota)

#Renderiza a pagina editar e pega o id
@app.route('/editar/<int:id_nota>')
def editar(id_nota):
    id_nota = id_nota
    return render_template('editar.html', id_nota = id_nota)

#Rota oculta que atualiza a nota
@app.route('/update', methods = ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_nota =  request.form['id_nota']

        cursor = db_connection.cursor()
        cursor.execute('SELECT * FROM NOTAS WHERE ID_NOTAs = %s', (id_nota,))
        resutado = cursor.fetchone()

        titulo_atual =  resutado[1]
        conteudo_atual = resutado[2]

        titulo_update =  request.form['titulo']
        conteudo_update = request.form['conteudo']
        
        if titulo_update == '':
            titulo_update = titulo_atual
        if conteudo_update == '':
            conteudo_update = conteudo_atual

        if len(titulo_update) > 30:
            flash('O titulo ultrapassou o limite permitido!')
            return redirect (url_for('editar', id_nota = id_nota))
        if len(conteudo_update) > 1000:
            flash('O conteudo ultrapassou o limite permitido!')
            return redirect (url_for('editar', id_nota = id_nota))
        

        cursor.execute('UPDATE NOTAS SET TITULO_notas = %s, CONTEUDO_NOTAS = %s WHERE ID_NOTAS = %s', (titulo_update, conteudo_update, id_nota,))
        db_connection.commit()
        flash ('Edições realizadas com sucesso!')

        return redirect(url_for('read', id_nota = id_nota))
    return redirect (url_for('editar', id_nota = id_nota))

#Renderiza as notas existentes para deletar
@app.route('/deletar')
def delete_pagina():
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM NOTAS')
    notas_deletar = cursor.fetchall()

    return render_template('deletar.html', notas_deletar = notas_deletar)

#Deleta a nota
@app.route('/remove/<int:id_nota>')
def delete(id_nota):
    cursor = db_connection.cursor()
    cursor.execute('DELETE FROM NOTAS WHERE ID_NOTAS = %s', (id_nota,))
    db_connection.commit()
    flash('Exclusão realizada com sucesso!')

    return redirect(url_for('delete_pagina'))
