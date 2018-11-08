from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy import desc

from app import db, login_manager, app
from app.auth.form import RegistrationForm, UserForm
from app.email import send_email
from app.models import User, Type, Records, History


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login_check():
    form = UserForm()
    if form.validate_on_submit() and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remenber_me.data)
            flash('Logged in successfully.')
            return redirect(request.args.get('next') or url_for('home'))

        flash('Invalid username or password.')
        return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    flag = form.validate_on_submit()
    if flag:
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    )
        db.session.add(user)

        db.session.commit()

        token = user.generate_confirmation_token()

        send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user, token=token)

        flash('账号验证已发送邮箱！')

        return redirect(url_for('login_page'))

    return render_template('auth/register.html', form=form)


@app.route('/auth/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        types = Type.query.all()
        for type in types:
            record = Records(type,current_user)
            db.session.save()

        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('index'))


@app.route('/auth/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('index'))
    return render_template('auth/unconfirmed.html')


@app.route('/auth/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    # 产生加密签名token
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    # 重新发送带token链接的邮件
    flash('A new confirmation email has been sent to you by email.')
    # 出现flash提示
    return redirect(url_for('index'))


@app.route('/auth/home', methods=['GET', 'POST'])
@login_required
def home():
    records = Records.query.filter_by(uid=current_user.id).order_by('tid').all()
    history_score = History.query.filter(History.uid==current_user.id).order_by(desc(History.score)).first()
    history_time = History.query.filter(History.uid==current_user.id).order_by(History.total_time).first()
    return render_template('auth/home.html', records=records, max_score=history_score, min_time=history_time)


@app.route('/login/page', methods=['GET', 'POST'])
def login_page():
    form = UserForm()
    return render_template('auth/login.html', form=form)


@app.route('/register/page', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)


