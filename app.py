import secrets
import string
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  

def generate_password(length=12, use_digits=True, use_uppercase=True, use_lowercase=True, use_special=True):
    chars = ''
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation

    if not chars:
        return "Выберите хотя бы один тип символов"

    return ''.join(secrets.choice(chars) for _ in range(length))

def password_strength(password):
    length = len(password)
    has_digit = any(c.isdigit() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_special = any(c in string.punctuation for c in password)

    types_count = sum([has_digit, has_upper, has_lower, has_special])

    if length < 8:
        return "Очень слабый", "very-weak"
    elif length < 11:
        if types_count >= 3:
            return "Средний", "medium"
        else:
            return "Слабый", "weak"
    elif length < 15:
        if types_count >= 3:
            return "Сильный", "strong"
        else:
            return "Средний", "medium"
    else:
        if types_count >= 3:
            return "Очень сильный", "very-strong"
        else:
            return "Сильный", "strong"

@app.route('/', methods=['GET', 'POST'])
def index():
    password = None
    strength_text = None
    strength_class = None
    if request.method == 'POST':
        length = int(request.form.get('length', 12))
        use_digits = 'digits' in request.form
        use_uppercase = 'uppercase' in request.form
        use_lowercase = 'lowercase' in request.form
        use_special = 'special' in request.form

        password = generate_password(length, use_digits, use_uppercase, use_lowercase, use_special)
        strength_text, strength_class = password_strength(password)

        # Сохраняем в историю (сессия)
        if 'history' not in session:
            session['history'] = []
        session['history'].insert(0, password)
        session['history'] = session['history'][:5]  # храним только последние 5
        session.modified = True

    history = session.get('history', [])
    return render_template('index.html', password=password, strength_text=strength_text,
                           strength_class=strength_class, history=history)

if __name__ == '__main__':
    app.run(debug=True)