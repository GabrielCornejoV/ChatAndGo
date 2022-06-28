from flask import Flask  # importar Flask
from flask_session import Session

app = Flask(__name__) # crea una instancia de Flask
#app.secret_key = "#_b3lt@3x1m2022/05yEsmUysegurA" # crea una llave secreta
app.config['SECRET_KEY'] = '#_b3lt@3x1m2022/05yEsmUysegurA'
app.config['SESSION_TYPE'] = 'filesystem'



