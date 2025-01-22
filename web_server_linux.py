# app.py
from flask import Flask, render_template, request
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Key
import threading
from functools import lru_cache

app = Flask(__name__)
mouse = MouseController()
keyboard = KeyboardController()

# Performans için mouse hassasiyeti
MOUSE_SENSITIVITY = 2.0  # Mouse hızını artırmak için bu değeri yükseltebilirsiniz

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

# Mouse pozisyonu önbelleği
last_position = None
last_update_time = 0

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
    
    threading.Thread(target=press_key, daemon=True).start()
    return "Başarılı bir şekilde alındı!"

@app.route('/mouse')
def mouse_page():
    return render_template('mouse.html')

@app.route('/keyboard_data', methods=["POST"])
def keyboard_data():
    content = request.form["content"]
    return "OK"

@lru_cache(maxsize=128)
def calculate_movement(x, y):
    """Mouse hareketlerini hesapla ve önbellekle"""
    return (
        int(round(float(x) * MOUSE_SENSITIVITY)),
        int(round(float(y) * MOUSE_SENSITIVITY))
    )

@app.route('/move_mouse', methods=['POST'])
def move_mouse():
    global last_position, last_update_time
    
    try:
        x_movement, y_movement = calculate_movement(
            request.form['x'],
            request.form['y']
        )
        
        current_position = mouse.position
        new_position = (
            current_position[0] + x_movement,
            current_position[1] + y_movement
        )
        
        # Ekran sınırlarını kontrol et
        screen_width = 1920  # Varsayılan ekran genişliği
        screen_height = 1080  # Varsayılan ekran yüksekliği
        
        new_position = (
            max(0, min(screen_width, new_position[0])),
            max(0, min(screen_height, new_position[1]))
        )
        
        mouse.position = new_position
        last_position = new_position
        
        return "Success"
    except Exception as e:
        print(f"Mouse hareketi hatası: {e}")
        return "Error", 500

@app.route('/mouse_click', methods=['POST'])
def mouse_click():
    try:
        button = request.form['button']
        if button == 'left':
            mouse.click(Button.left)
        elif button == 'right':
            mouse.click(Button.right)
        return "Success"
    except Exception as e:
        print(f"Mouse tıklama hatası: {e}")
        return "Error", 500

def init_app():
    """Uygulama başlangıç yapılandırması"""
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    init_app()
    app.run(
        host='0.0.0.0',
        debug=True,
        threaded=True,
        use_reloader=False
    )
