# app.py
from flask import Flask, render_template, request
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key
import threading

app = Flask(__name__)
mouse = MouseController()
keyboard = KeyboardController()

# Klavye tuşlarını tanımlama
key_mapping = {
    'up': Key.up,
    'down': Key.down,
    'left': Key.left,
    'right': Key.right,
    'E': 'e',
    'Enter': Key.enter,
    'Back': Key.backspace,
    'Exit': Key.delete
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ajax', methods=['POST'])
def ajax():
    data = request.form['button_value']
    print(f"Gelen veri: {data}")
    
    def press_key():
        if data in key_mapping:
            key = key_mapping[data]
            if isinstance(key, str):
                keyboard.press(key)
                keyboard.release(key)
            else:
                keyboard.press(key)
                keyboard.release(key)
    
    # Klavye işlemlerini ayrı bir thread'de çalıştır
    threading.Thread(target=press_key).start()
    return "Başarılı bir şekilde alındı!"

@app.route('/mouse')
def mouse_page():
    return render_template('mouse.html')

@app.route('/keyboard_data', methods=["POST"])
def keyboard_data():
    content = request.form["content"]
    return "OK"

@app.route('/move_mouse', methods=['POST'])
def move_mouse():
    x_movement = float(request.form['x'])
    y_movement = float(request.form['y'])
    x_movement = int(round(x_movement))
    y_movement = int(round(y_movement))
    
    current_position = mouse.position
    new_position = (current_position[0] + x_movement, current_position[1] + y_movement)
    mouse.position = new_position
    return "Başarılı bir şekilde alındı!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
