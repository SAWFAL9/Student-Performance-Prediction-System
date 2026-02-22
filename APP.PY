# app.py - Student Performance Prediction System

from flask import Flask, render_template, request, jsonify # pyright: ignore[reportMissingImports]

app = Flask(__name__)

def calculate_prediction(study_hours, attendance, previous_score, extra_activities):
    """Calculate predicted score"""
    score = (study_hours * 2.5) + (attendance * 0.5) + (previous_score * 0.8) + (extra_activities * 0.3)
    predicted = min(100, max(0, round(score, 2)))
    return predicted

def get_category(score):
    """Get performance category"""
    if score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Average'
    else:
        return 'Needs Improvement'

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    study_hours = request.form.get('study_hours', '').strip()
    attendance = request.form.get('attendance', '').strip()
    previous_score = request.form.get('previous_score', '').strip()
    extra_activities = request.form.get('extra_activities', '').strip()
    
    errors = []
    
    if study_hours == '':
        errors.append('Study Hours is required!')
    elif not study_hours.replace('.', '').isdigit():
        errors.append('Study Hours must be a number!')
    elif float(study_hours) < 0 or float(study_hours) > 24:
        errors.append('Study Hours must be between 0 and 24!')
    
    if attendance == '':
        errors.append('Attendance is required!')
    elif not attendance.replace('.', '').isdigit():
        errors.append('Attendance must be a number!')
    elif float(attendance) < 0 or float(attendance) > 100:
        errors.append('Attendance must be between 0 and 100!')
    
    if previous_score == '':
        errors.append('Previous Score is required!')
    elif not previous_score.replace('.', '').isdigit():
        errors.append('Previous Score must be a number!')
    elif float(previous_score) < 0 or float(previous_score) > 100:
        errors.append('Previous Score must be between 0 and 100!')
    
    if extra_activities == '':
        errors.append('Extra Activities is required!')
    elif not extra_activities.replace('.', '').isdigit():
        errors.append('Extra Activities must be a number!')
    elif float(extra_activities) < 0 or float(extra_activities) > 168:
        errors.append('Extra Activities must be between 0 and 168!')
    
    if errors:
        return jsonify({'success': False, 'errors': errors})
    
    study_hours = float(study_hours)
    attendance = float(attendance)
    previous_score = float(previous_score)
    extra_activities = float(extra_activities)
    
    predicted_score = calculate_prediction(study_hours, attendance, previous_score, extra_activities)
    category = get_category(predicted_score)
    
    return jsonify({
        'success': True,
        'prediction': predicted_score,
        'category': category
    })

if __name__ == '__main__':
    print("🚀 Starting Student Performance Prediction System")
    print("📡 Server running at http://localhost:5000")
    app.run(debug=True)
    