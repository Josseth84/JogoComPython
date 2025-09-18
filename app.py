from flask import Flask, render_template, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_segura'  # Substitua por uma chave segura

# Configuração do banco PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jose_user:sua_senha_segura@localhost/jogocompython'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de dados
class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(50))
    scenario_id = db.Column(db.Integer)
    choice = db.Column(db.String(10))
    response_time = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    justificativa = db.Column(db.Text)
    sugestao = db.Column(db.Text)
    criterio = db.Column(db.Text)

# Rota de início (gera player_id)
@app.route('/inicio')
def inicio():
    session['player_id'] = str(uuid.uuid4())
    return redirect('/fase1')

# Rotas das fases
@app.route('/')
def index():
    return '<h1>Bem-vindo ao Jogo de Comunicação!</h1>'

@app.route('/fase1')
def fase1():
    return render_template('fase1.html')

@app.route('/fase2')
def fase2():
    return render_template('fase2.html')

@app.route('/fase3', methods=['GET', 'POST'])
def fase3():
    if request.method == 'POST':
        choice = request.form['choice']
        justificativa = request.form.get('justificativa', '')
        player_id = session.get('player_id')
        timestamp = datetime.now()

        nova_resposta = Resposta(
            player_id=player_id,
            scenario_id=3,
            choice=choice,
            response_time=0,
            timestamp=timestamp,
            justificativa=justificativa
        )
        db.session.add(nova_resposta)
        db.session.commit()

        return redirect('/fase4')
    return render_template('fase3.html')

@app.route('/fase4', methods=['GET', 'POST'])
def fase4():
    if request.method == 'POST':
        choice = request.form['choice']
        sugestao = request.form.get('sugestao', '')
        player_id = session.get('player_id')
        timestamp = datetime.now()

        nova_resposta = Resposta(
            player_id=player_id,
            scenario_id=4,
            choice=choice,
            response_time=0,
            timestamp=timestamp,
            sugestao=sugestao
        )
        db.session.add(nova_resposta)
        db.session.commit()

        return redirect('/fase5')
    return render_template('fase4.html')

@app.route('/fase5', methods=['GET', 'POST'])
def fase5():
    if request.method == 'POST':
        choice = request.form['choice']
        criterio = request.form.get('criterio', '')
        player_id = session.get('player_id')
        timestamp = datetime.now()

        nova_resposta = Resposta(
            player_id=player_id,
            scenario_id=5,
            choice=choice,
            response_time=0,
            timestamp=timestamp,
            criterio=criterio
        )
        db.session.add(nova_resposta)
        db.session.commit()

        return redirect('/conclusao')
    return render_template('fase5.html')

# Rota de conclusão
@app.route('/conclusao')
def conclusao():
    player_id = session.get('player_id')
    respostas = Resposta.query.filter_by(player_id=player_id).all()

    def gerar_perfil(escolhas):
        empaticas = escolhas.count('B')
        resistentes = escolhas.count('A') + escolhas.count('C')
        if empaticas > resistentes:
            return "Colaborador com atitude inclusiva"
        elif empaticas == resistentes:
            return "Colaborador em transição"
        else:
            return "Colaborador com resistência à inclusão"

    escolhas = [r.choice for r in respostas]
    perfil = gerar_perfil(escolhas)

    return render_template('conclusao.html', perfil=perfil, respostas=respostas)

# Rota para receber resposta via JSON (API externa, se usada)
@app.route('/resposta', methods=['POST'])
def receber_resposta():
    data = request.get_json()
    print('Resposta recebida:', data)

    nova_resposta = Resposta(
        player_id=data.get('player_id'),
        scenario_id=data.get('scenario_id'),
        choice=data.get('choice'),
        response_time=data.get('response_time')
    )
    db.session.add(nova_resposta)
    db.session.commit()

    score = 10 if data.get('choice') == 'C' else 5 if data.get('choice') == 'B' else 0
    return jsonify({'score': score})

# Inicialização
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)