from flask import Flask, render_template, request, redirect, url_for
import os
import shutil
import subprocess
import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
STATIC_OUTPUT = 'static/output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_OUTPUT, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Dummy login logic
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Dummy registration logic
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'video' not in request.files:
        return "No file part", 400
    file = request.files['video']
    if file.filename == '':
        return "No selected file", 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    shutil.rmtree(STATIC_OUTPUT, ignore_errors=True)
    os.makedirs(STATIC_OUTPUT, exist_ok=True)

    print("[INFO] Running detection script...")
    subprocess.call(f"python my.py -i {filepath} -y yolo-coco", shell=True)

    frames = sorted(os.listdir('output'), key=lambda x: os.path.getmtime(os.path.join('output', x)))
    if not frames:
        return "No frames detected", 500

    last_frame = frames[-1]
    shutil.copy(f"output/{last_frame}", f"{STATIC_OUTPUT}/{last_frame}")

    with open("accident_log.txt", "r") as f:
        lines = f.readlines()
        last_line = lines[-1] if lines else "Severity: UNKNOWN"
    severity = last_line.split("Severity: ")[-1].split()[0]

    return render_template("result.html", image_path=f"output/{last_frame}", severity=severity)

@app.route('/play', methods=['POST'])
def play_video():
    subprocess.call("python playCrash.py", shell=True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
