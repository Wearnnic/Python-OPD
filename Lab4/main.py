from flask import Flask, request, render_template
import math

app = Flask(__name__)

def find_roots(a, b, c):
    discr = b**2 - 4*a*c
    if discr > 0:
        x1 = (-b + math.sqrt(discr)) / (2*a)
        x2 = (-b - math.sqrt(discr)) / (2*a)
        return f"Два корня: x1 = {x1:.2f}, x2 = {x2:.2f}"
    elif discr == 0:
        x = -b / (2*a)
        return f"Один корень: x = {x:.2f}"
    else:
        return "Корней нет"

@app.route('/', methods=['GET', 'POST'])
def quadratic_solver():
    result = None
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            c = float(request.form['c'])
            if a == 0:
                result = "Коэффициент a не должен быть равен нулю."
            else:
                result = find_roots(a, b, c)
        except ValueError:
            result = "Пожалуйста, введите корректные числовые значения."
    return render_template('templates.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
