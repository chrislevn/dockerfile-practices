# app.py
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    operation = request.form['operation']

    if operation == 'add':
        result = num1 + num2
        operation_str = '+'
    elif operation == 'subtract':
        result = num1 - num2
        operation_str = '-'
    elif operation == 'multiply':
        result = num1 * num2
        operation_str = 'x'
    elif operation == 'divide':
        if num2 != 0:
            result = num1 / num2
            operation_str = '/'
        else:
            return "Error: Division by zero!"
    else:
        return "Invalid operation!"

    return jsonify(result=result, operation=operation_str, num1=num1, num2=num2)

if __name__ == '__main__':
    load_dotenv()
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
