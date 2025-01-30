from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

# Настройки базы данных (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Настройки почтового сервера
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Ваш email
app.config['MAIL_PASSWORD'] = 'your-password'         # Пароль приложения
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)

# Модель данных для хранения заявок
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Создание таблиц
with app.app_context():
    db.create_all()

# Главная страница
@app.route('/')
def home():
    return render_template('index.html')

# Страница услуг
@app.route('/services')
def services():
    return render_template('services.html')

# Страница обратной связи
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Получение данных из формы
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Сохранение данных в базу
        new_request = Request(name=name, email=email, message=message)
        db.session.add(new_request)
        db.session.commit()

        # Отправка письма на email
        try:
            msg = Message('Новая заявка с сайта',
                          recipients=['recipient-email@gmail.com'])  # Укажите email получателя
            msg.body = f"Имя: {name}\nEmail: {email}\nСообщение: {message}"
            mail.send(msg)
        except Exception as e:
            print(f"Ошибка отправки email: {e}")

        return redirect(url_for('thank_you'))
    return render_template('contact.html')

# Страница благодарности
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
