from flask import Flask, render_template, flash, request, redirect, url_for
from ratebait.models import db, User
from ratebait.game.views import game_blueprint
from ratebait.users.views import user_blueprint
from ratebait.admin.views import admin_blueprint
from ratebait.users.forms import RegistratieForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required


### app met standaard template folder ###
app = Flask(__name__, template_folder='ratebait/templates')


### Registreer de blueprint ###
app.register_blueprint(game_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(admin_blueprint)


### CSRF-beveiliging vereist een secret key ###
app.config['SECRET_KEY'] = 'mijngeheimesleutel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


### Database koppeling ###
db.init_app(app)


### Login manager met login redirect wanneer login required ###
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


### ingelogde user tracken  ###
@login_manager.user_loader
def load_user(user_id):
    """ Zoekt userid op in de database"""
    return User.query.get(int(user_id))


### index endpoint ###
@app.route("/")
def index() -> str:
    """Homepage route. Haalt de homepage op"""
    return render_template("home.html")


### Registratie endpoint met form verwerking ###
@app.route("/registratie", methods=["GET", "POST"])
def registratie() -> str:
    """ registratie voor het aanmaken van nieuwe users. Haalt data uit de formulieren op en verwerkt deze in de database"""
    username: str | bool = False
    password: str | bool = False
    email:    str | bool = False

    form = RegistratieForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data       
        existing = User.query.filter_by(username=username).first()
        
        if existing:
            flash("Gebruikersnaam bestaat al!", "danger")
            return redirect(url_for("registratie"))
        if User.query.filter_by(email=email).first():
            flash("Email bestaat al!", "danger")
            return redirect(url_for("registratie"))

        else:
            if User.query.filter_by(id=1).first() is None:
                is_admin = True
            else:
                is_admin = False
            user = User(username,password,email,is_admin)
            db.session.add(user)
            db.session.commit()
            flash("Account aangemaakt!", "success")

            form.username.data = ""
            form.password.data = ""
            form.email.data = "" 
    
    return render_template("registratie.html", form = form, username=username, password=password, email=email)


### login pagina met login form + flashcards ###
@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """controleert de database tegenover de data dat ingevoerd is in het formulier. gebruikt daarna flask-login om de gebruiker in te loggen en te onthouden"""
    form = LoginForm()
    next_page = request.args.get("next")

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Succesvol ingelogd!", "success")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Ongeldige gebruikersnaam of wachtwoord", "danger")
    return render_template("login.html", form=form)


### logout script ###
@app.route("/logout")
@login_required
def logout():
    """ Gebruikt flask-login om de gebruiker uit te loggen en niet meer te onthouden"""
    logout_user()
    flash("Je bent uitgelogd!", "info")
    return redirect(url_for("index"))


### run app + maak database ###
if __name__ == "__main__": 
    # Dit zorgt ervoor dat de tabellen worden aangemaakt als ze nog niet bestaan
    with app.app_context():
        db.create_all()
        print("Database tabellen succesvol aangemaakt!")
    app.run(debug=True)