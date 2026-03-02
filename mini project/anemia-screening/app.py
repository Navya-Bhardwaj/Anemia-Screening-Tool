from flask import Flask, request, render_template, redirect, url_for, session
import cv2
import numpy as np
from PIL import Image
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'anemia-screening-secret-key-2024'  # Required for session management
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def analyze_image(image_path):
    """
    Analyze the image for potential anemia indicators.
    Uses color analysis: converts to grayscale and checks average brightness.
    Thresholds are arbitrary for demo; in real app, use trained model.
    Returns a dictionary with risk level, message, color, and brightness data.
    """
    # Load image with OpenCV
    image = cv2.imread(image_path)
    if image is None:
        return {
            "risk_level": "Error",
            "message": "Error: Unable to process image.",
            "color": "gray",
            "brightness": 0
        }

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate average brightness
    avg_brightness = np.mean(gray)

    # Simple threshold for pallor detection (lower brightness indicates paler skin/nails)
    # These thresholds are placeholders; real detection requires medical data
    if avg_brightness < 100:
        risk_level = "High Risk"
        message = "High likelihood of anemia detected. Please consult a healthcare professional."
        color = "red"
    elif avg_brightness < 150:
        risk_level = "Moderate Risk"
        message = "Moderate likelihood of anemia. Consider further testing."
        color = "orange"
    else:
        risk_level = "Low Risk"
        message = "Low likelihood of anemia. Image appears normal."
        color = "green"

    return {
        "risk_level": risk_level,
        "message": message,
        "color": color,
        "brightness": float(avg_brightness)
    }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/screening')
def index():
    return render_template('screening.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        result = analyze_image(filepath)
        # Clean up uploaded file
        os.remove(filepath)

        # Store result in session for progress tracking
        if 'results' not in session:
            session['results'] = []
        session['results'].append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'risk_level': result['risk_level'],
            'brightness': result['brightness'],
            'color': result['color']
        })
        session.modified = True

        return render_template('result.html', result=result)

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/progress')
def progress():
    results = session.get('results', [])
    return render_template('progress.html', results=results)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    responses = {
        'precautions': 'Precautions for anemia: Rest when tired, avoid heavy lifting, stay hydrated, avoid caffeine and alcohol, eat iron-rich foods, take supplements as prescribed.',
        'home remedies': 'Home remedies for anemia: Eat iron-rich foods like spinach, lentils, red meat. Include vitamin C foods (citrus, tomatoes) to aid absorption. Drink beetroot juice, pomegranate juice. Avoid tea/coffee with meals.',
        'diet': 'Recommended diet for anemia: Iron-rich foods (spinach, beans, nuts), vitamin C sources (oranges, strawberries), vitamin B12 (eggs, dairy), folate (leafy greens, broccoli). Avoid calcium-rich foods with iron intake.',
        'symptoms': 'Common anemia symptoms: Fatigue, weakness, pale skin, shortness of breath, dizziness, cold hands/feet, irregular heartbeat.',
        'causes': 'Anemia causes: Iron deficiency, vitamin deficiency, chronic diseases, blood loss, bone marrow problems.',
        'treatment': 'Treatment: Depends on cause. May include iron supplements, vitamin B12 injections, blood transfusions, treating underlying conditions.',
        'prevention': 'Prevention: Balanced diet with iron/vitamins, regular check-ups, treat underlying conditions, avoid blood loss.',
        'iron rich foods': 'Iron-rich foods: Red meat, poultry, fish, lentils, beans, tofu, fortified cereals, spinach, raisins.',
        'vitamin c': 'Vitamin C helps iron absorption. Sources: Citrus fruits, bell peppers, strawberries, tomatoes, broccoli.',
        'supplements': 'Supplements: Iron tablets, vitamin B12, folate. Take as prescribed by doctor. May cause constipation or nausea.',
        'exercise': 'Exercise: Light activities like walking are good. Avoid strenuous exercise until anemia improves.',
        'pregnancy': 'During pregnancy: Higher iron needs. Prenatal vitamins, iron-rich diet, regular blood tests.',
        'children': 'In children: Ensure iron-fortified formula, iron-rich foods, vitamin C. Monitor growth and development.',
        'elderly': 'In elderly: May need B12 supplements, check for malabsorption, regular screenings.',
        'default': 'I can help with information about anemia precautions, home remedies, diet recommendations, symptoms, causes, and treatment. What would you like to know?'
    }

    response = responses.get('default')
    for key, value in responses.items():
        if key in user_message:
            response = value
            break

    return {'response': response}

if __name__ == '__main__':
    app.run(debug=True)
