# app.py

from flask import Flask, render_template, request
import keyboard  
import pydirectinput


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ajax', methods=['POST'])
def ajax():
    data = request.form['button_value']
    print(f"Gelen veri: {data}")
    
    # Klavye olaylarına göre işlem yap
    if data == 'up':
        keyboard.press_and_release('up')
    elif data == 'down':
        keyboard.press_and_release('down')
    elif data == 'left':
        keyboard.press_and_release('left')
    elif data == 'right':
        keyboard.press_and_release('right')
    elif data == 'E':
        keyboard.press_and_release('e')
    elif data == 'Enter':
        keyboard.press_and_release('enter')
    elif data == "Back":
        keyboard.press_and_release('backspace')
    elif data == "Exit":
        keyboard.press_and_release('')
    print(data)
    
    return "Başarılı bir şekilde alındı!"

@app.route('/mouse')
def mouse():
    return render_template('mouse.html')


@app.route('/keyboard_data', methods=["POST"])
def keyboard_data():
    content = request.form["content"]


@app.route('/move_mouse', methods=['POST'])
def move_mouse():
    x_movement = float(request.form['x'])
    y_movement = float(request.form['y'])

    x_movement = int(round(x_movement))
    y_movement = int(round(y_movement))

    pydirectinput.moveRel(x_movement, y_movement)

    return "Başarılı bir şekilde alındı!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
