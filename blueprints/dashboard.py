from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app import db

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/home')
@login_required
def home():
    return render_template('main.html')

@dashboard.route('/')
@login_required
def index():
    return render_template('main.html')

@dashboard.route('/account/token', methods=['POST'])
@login_required
def generate_token():
    token = current_user.generate_auth_token()
    return render_template('account.html', token=token)

@dashboard.route('/account')
@login_required
def account():
    return render_template('account.html', name=current_user.username)

@dashboard.route('/account/update', methods=['POST'])
@login_required
def update_password():
    new_password = request.form.get('new_password')
    retype_password = request.form.get('retype_password')
    if new_password == retype_password:
        current_user.hash_password(new_password)
        db.commit()
    else:
        flash("Password and retype are not the same")
    return render_template('account.html', password=True)

