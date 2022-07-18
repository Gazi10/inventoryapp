from distutils.log import debug
from flask import Flask, render_template, url_for, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from QrBarCode import scan
import inventory_db as i_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

inventory = db.Table('inventory', db.metadata, autoload=True, autoload_with=db.engine)

@app.route('/', methods=['GET', 'POST'])
def index():
    items = db.session.query(inventory).all()
    return render_template('index.html', items=items)

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    return Response(scan(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/delete/<string:title>')
def delete(title):
    i_db.delete(title)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
