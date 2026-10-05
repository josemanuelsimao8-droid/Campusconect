from flask import Blueprint, render_template, request



views = Blueprint('views', __name__)


@views.route('/')
def homepage():
    return render_template('homepage.html')


@views.route('/login')
def login():
    return render_template('login.html')

@views.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_notice = None
    if request.method == 'POST':
        signup_notice = 'O cadastro ainda não está conectado ao armazenamento de contas.'
    return render_template('signup.html', signup_notice=signup_notice)
