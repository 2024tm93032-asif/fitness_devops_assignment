"""
ACEest Fitness & Gym Management System - Flask Application
Version: 1.0.0
Author: DevOps Team
Description: Web-based fitness tracking and gym management system
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False

# In-memory data storage (replace with database in production)
users_db = {}
workouts_db = {}

# MET Values for calorie calculation
MET_VALUES = {
    "Warm-up": 3.0,
    "Workout": 6.0,
    "Cool-down": 2.5,
    "Cardio": 8.0,
    "Strength": 5.0,
    "Flexibility": 2.5
}


# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, else show landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        # Simple authentication (replace with proper auth in production)
        if username in users_db and users_db[username]['password'] == password:
            session['user_id'] = username
            session['user_name'] = users_db[username]['name']
            return jsonify({'success': True, 'message': 'Login successful', 'redirect': url_for('dashboard')})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        height = data.get('height')
        weight = data.get('weight')
        
        if not all([username, password, name, age, gender, height, weight]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if username in users_db:
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        # Calculate BMI and BMR
        try:
            height_m = float(height) / 100
            weight_kg = float(weight)
            age_int = int(age)
            bmi = weight_kg / (height_m ** 2)
            
            # Mifflin-St Jeor Equation for BMR
            if gender.lower() == 'male':
                bmr = 10 * weight_kg + 6.25 * float(height) - 5 * age_int + 5
            else:
                bmr = 10 * weight_kg + 6.25 * float(height) - 5 * age_int - 161
            
            users_db[username] = {
                'password': password,
                'name': name,
                'age': age_int,
                'gender': gender,
                'height': float(height),
                'weight': weight_kg,
                'bmi': round(bmi, 2),
                'bmr': round(bmr, 2),
                'registration_date': datetime.now().isoformat()
            }
            
            workouts_db[username] = {
                'Warm-up': [],
                'Workout': [],
                'Cool-down': [],
                'Cardio': [],
                'Strength': [],
                'Flexibility': []
            }
            
            return jsonify({'success': True, 'message': 'Registration successful', 'redirect': url_for('login')})
        
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid numeric values'}), 400
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard view"""
    user_id = session.get('user_id')
    user_info = users_db.get(user_id, {})
    
    # Calculate workout statistics
    workouts = workouts_db.get(user_id, {})
    total_workouts = sum(len(w) for w in workouts.values())
    total_duration = sum(
        w.get('duration', 0) for category in workouts.values() for w in category
    )
    
    # Recent workouts (last 7 days)
    today = datetime.now()
    recent_workouts = []
    for category, workout_list in workouts.items():
        for workout in workout_list:
            workout_date = datetime.fromisoformat(workout.get('timestamp', today.isoformat()))
            if (today - workout_date).days <= 7:
                recent_workouts.append({
                    'category': category,
                    'exercise': workout.get('exercise', 'Unknown'),
                    'duration': workout.get('duration', 0),
                    'date': workout_date.strftime('%Y-%m-%d')
                })
    
    return render_template('dashboard.html', 
                         user=user_info,
                         total_workouts=total_workouts,
                         total_duration=total_duration,
                         recent_workouts=recent_workouts)


@app.route('/workouts')
@login_required
def workouts():
    """Workout logging page"""
    return render_template('workouts.html')


@app.route('/api/workouts', methods=['GET', 'POST'])
@login_required
def api_workouts():
    """API endpoint for workout management"""
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        data = request.get_json()
        category = data.get('category', 'Workout')
        exercise = data.get('exercise')
        duration = data.get('duration')
        
        if not exercise or not duration:
            return jsonify({'success': False, 'message': 'Exercise and duration required'}), 400
        
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError()
        except ValueError:
            return jsonify({'success': False, 'message': 'Duration must be a positive number'}), 400
        
        workout_entry = {
            'exercise': exercise,
            'duration': duration,
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'calories': calculate_calories(category, duration, users_db.get(user_id, {}).get('weight', 70))
        }
        
        if user_id not in workouts_db:
            workouts_db[user_id] = {cat: [] for cat in MET_VALUES.keys()}
        
        if category not in workouts_db[user_id]:
            workouts_db[user_id][category] = []
        
        workouts_db[user_id][category].append(workout_entry)
        
        return jsonify({'success': True, 'message': 'Workout logged successfully', 'workout': workout_entry})
    
    # GET request - return all workouts
    workouts = workouts_db.get(user_id, {})
    return jsonify({'success': True, 'workouts': workouts})


@app.route('/api/workouts/summary')
@login_required
def workout_summary():
    """Get workout summary statistics"""
    user_id = session.get('user_id')
    workouts = workouts_db.get(user_id, {})
    
    summary = {
        'total_workouts': 0,
        'total_duration': 0,
        'total_calories': 0,
        'by_category': {},
        'weekly_stats': get_weekly_stats(user_id)
    }
    
    for category, workout_list in workouts.items():
        category_duration = sum(w.get('duration', 0) for w in workout_list)
        category_calories = sum(w.get('calories', 0) for w in workout_list)
        
        summary['total_workouts'] += len(workout_list)
        summary['total_duration'] += category_duration
        summary['total_calories'] += category_calories
        
        summary['by_category'][category] = {
            'count': len(workout_list),
            'duration': category_duration,
            'calories': category_calories
        }
    
    return jsonify({'success': True, 'summary': summary})


@app.route('/progress')
@login_required
def progress():
    """Progress tracking page"""
    return render_template('progress.html')


@app.route('/diet')
@login_required
def diet():
    """Diet guidance page"""
    user_id = session.get('user_id')
    user_info = users_db.get(user_id, {})
    
    # Calculate daily calorie needs
    bmr = user_info.get('bmr', 1800)
    activity_multiplier = 1.55  # Moderate activity
    daily_calories = round(bmr * activity_multiplier)
    
    diet_plan = generate_diet_plan(daily_calories, user_info.get('bmi', 22))
    
    return render_template('diet.html', user=user_info, daily_calories=daily_calories, diet_plan=diet_plan)


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200


# Helper functions

def calculate_calories(category, duration_minutes, weight_kg):
    """Calculate calories burned based on MET values"""
    met = MET_VALUES.get(category, 4.0)
    calories = met * weight_kg * (duration_minutes / 60)
    return round(calories, 2)


def get_weekly_stats(user_id):
    """Get workout statistics for the last 7 days"""
    workouts = workouts_db.get(user_id, {})
    today = datetime.now()
    weekly_data = {(today - timedelta(days=i)).strftime('%Y-%m-%d'): 0 for i in range(6, -1, -1)}
    
    for category, workout_list in workouts.items():
        for workout in workout_list:
            workout_date = datetime.fromisoformat(workout.get('timestamp', today.isoformat()))
            date_key = workout_date.strftime('%Y-%m-%d')
            if date_key in weekly_data:
                weekly_data[date_key] += workout.get('duration', 0)
    
    return weekly_data


def generate_diet_plan(daily_calories, bmi):
    """Generate basic diet recommendations"""
    protein_ratio = 0.30
    carbs_ratio = 0.40
    fats_ratio = 0.30
    
    plan = {
        'protein': round(daily_calories * protein_ratio / 4),  # 4 cal/g
        'carbs': round(daily_calories * carbs_ratio / 4),
        'fats': round(daily_calories * fats_ratio / 9),  # 9 cal/g
        'recommendations': []
    }
    
    if bmi < 18.5:
        plan['recommendations'].append('Focus on nutrient-dense, high-calorie foods')
        plan['recommendations'].append('Include healthy fats and complex carbs')
    elif 18.5 <= bmi < 25:
        plan['recommendations'].append('Maintain balanced diet with all macros')
        plan['recommendations'].append('Stay hydrated and eat regular meals')
    else:
        plan['recommendations'].append('Reduce processed foods and added sugars')
        plan['recommendations'].append('Increase protein and fiber intake')
    
    return plan


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
