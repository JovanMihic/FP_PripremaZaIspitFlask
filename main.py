# Flaska-zadatak:
# Koristeći Flask napraviti formu za logovanje za studenta.
# Ako je logovanje uspešno, omogućiti unos osnovnih podataka o studentu.
# Nakon unosa dati prikaz osnovnih podataka i omogućiti editovanje i brisanje podataka.
# Podatke spremiti u tekstualni fajl i uploadovati u odgovoarajući folder.
from flask import Flask, request, render_template, url_for, session
import json
import random
from werkzeug.utils import redirect

app = Flask(__name__)
usersDict = {
    "users": [
        {
            "username": "admin",
            "password": "admin123"
        },
        {
            "username": "miki",
            "password": "miki123"
        }
    ]
}
data = {}
lstr=list('interesantno')
random.shuffle(lstr)
app.secret_key = str(lstr)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def loadUsers():  # upisuje podatke iz users.json u data
    global data
    with open("users.json", 'r') as f:  # with je samo pametan nacin da se otvori falj, zatvara ga kad zavrsi
        data = json.load(f)


def saveUsers():  # upisuje sadrzaja od data u users.json
    global data
    with open("users.json", 'w') as f:
        json.dump(data, f)


# def addUser(newUser):
#     global users
#     '{"username":"admin69","password":"admin123"}'


# addUser({"username":"joca","password":"Lozinka360"})
#
# addUser({"username":"miki","password":"mikikralj"})
# print(usersJSON)
# saveUsers(json.dumps(usersJSON))

@app.route('/')
def index():
    return redirect(url_for('login'))


# @app.route('/jovan')
# def jovan():
#     return 'Hello Jovan!'
#
#
# @app.route('/profile/<username>')
# def username(username):
#     return '<h1>Hello ' + username + '</h1>'
#
#
# @app.route('/post/<int:id>')
# def postId(id):
#     return '<h1>Post id: ' + str(id) + '<h1>'
#

# KOD ZA DODAVANJE NOVOG USERA
# nm = str(request.form['nm'])
# pwd = str(request.form['pwd'])
# usersDict['users'].append({'username':nm,'password':pwd})
# loadUsers()
# data.update(usersDict)  # u data se dodaju podaci iz usersDict
# saveUsers()
# return str(request.form['nm']) + " " + str(request.form['pwd'])
msg = ""


@app.route('/login', methods=['GET', 'POST'])
def login():
    global data
    global usersDict
    global msg

    if request.method == 'GET':
        vrati = render_template('loginForma.html', message=msg)
        msg = ''  # cisto da bi mogla da se posalje poruka
        return vrati
    else:
        session['username'] = request.form['nm']
        nm = str(request.form['nm'])
        pwd = str(request.form['pwd'])
        loadUsers()
        msg = ''
        for user in data['users']:
            if user['username'] == nm and user['password'] == pwd:
                # print(type(user['admin']),user['admin'])
                if user['admin']:
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('unos', username=nm, id=user['id']))
        msg = "Unesite validno ime i lozinku"
        return redirect(url_for('login'))


@app.route('/unos/<username>_<id>', methods=['GET', 'POST'])
def unos(username, id):
    if request.method == 'GET':
        # return render_template('podaciForma.html', usr=username, id=id)
        return '<h1>Ulogovan kao '+session['username']+'</h1>'
    else:
        loadUsers()
        for user in data['users']:
            if user['id'] == int(id):
                user.update({"ime": request.form['ime']})
                user.update({"prezime": request.form['prezime']})
                user.update({"godiste": request.form['godiste']})
        saveUsers()
        return redirect(url_for('prikaz', id=id))
@app.route('/admin')
def admin():
    loadUsers()
    print(session['username'])
    if session['username'] == 'admin':
        return render_template('admin.html',result=data['users'])
    else:
        return "Greska, vi niste administrator"
@app.route('/admin/izmeni/<id>')
def administracija(id):
    loadUsers()
    if session['username'] == 'admin':
        if request.method =='GET':
            return render_template('adminIzmeni.html',result=data['users'],id=int(id))
        else:
            for user in data['users']:
                if user['id'] == int(id):
                    user.update({"id": request.form['i']})
                    user.update({"admin": request.form['admin']})
                    user.update({"username": request.form['username']})
                    user.update({"password": request.form['pass']})

                    user.update({"ime": request.form['ime']})
                    user.update({"prezime": request.form['prezime']})
                    user.update({"godiste": request.form['godiste']})
            saveUsers()
    else:
        return 'Greska, vi niste administator'
@app.route('/prikaz/<id>')
def prikaz(id):
    loadUsers()
    for user in data['users']:
        if user['id'] == int(id):
            username = user['username']
            ime = user['ime']
            prezime = user['prezime']
            godiste = user['godiste']

    return render_template(
        'prikazPodataka.html',
        username=username,
        ime=ime,
        prezime=prezime,
        godiste=godiste,
        id=id
    )


if __name__ == '__main__':
    app.run(debug=True)
