"""
Unit Tests for ACEest Fitness Application
Test Suite covers all Flask routes and business logic
"""

import pytest
import json
from app import app, users_db, workouts_db, calculate_calories, get_weekly_stats, generate_diet_plan


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            # Clear databases before each test
            users_db.clear()
            workouts_db.clear()
            yield client


@pytest.fixture
def authenticated_client(client):
    """Create authenticated test client"""
    # Register a test user
    test_user = {
        'username': 'testuser',
        'password': 'testpass123',
        'name': 'Test User',
        'age': 25,
        'gender': 'male',
        'height': 175,
        'weight': 70
    }
    
    response = client.post('/register',
                          data=json.dumps(test_user),
                          content_type='application/json')
    
    # Login
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    response = client.post('/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    return client


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test health check returns 200"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'version' in data
        assert 'timestamp' in data


class TestAuthentication:
    """Test user authentication"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        user_data = {
            'username': 'newuser',
            'password': 'password123',
            'name': 'New User',
            'age': 30,
            'gender': 'female',
            'height': 165,
            'weight': 60
        }
        
        response = client.post('/register',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'newuser' in users_db
        
        # Verify user data
        user = users_db['newuser']
        assert user['name'] == 'New User'
        assert user['age'] == 30
        assert 'bmi' in user
        assert 'bmr' in user
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields"""
        user_data = {
            'username': 'incomplete',
            'password': 'pass'
        }
        
        response = client.post('/register',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_register_duplicate_username(self, client):
        """Test registration with existing username"""
        user_data = {
            'username': 'duplicate',
            'password': 'password123',
            'name': 'User One',
            'age': 25,
            'gender': 'male',
            'height': 175,
            'weight': 70
        }
        
        # Register first time
        client.post('/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Try to register again
        response = client.post('/register',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'already exists' in data['message']
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register user first
        user_data = {
            'username': 'loginuser',
            'password': 'loginpass',
            'name': 'Login User',
            'age': 28,
            'gender': 'male',
            'height': 180,
            'weight': 75
        }
        
        client.post('/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Login
        login_data = {
            'username': 'loginuser',
            'password': 'loginpass'
        }
        
        response = client.post('/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        login_data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        
        response = client.post('/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_logout(self, authenticated_client):
        """Test user logout"""
        response = authenticated_client.get('/logout', follow_redirects=False)
        assert response.status_code == 302  # Redirect


class TestWorkouts:
    """Test workout management"""
    
    def test_add_workout_success(self, authenticated_client):
        """Test adding a workout"""
        workout_data = {
            'category': 'Workout',
            'exercise': 'Running',
            'duration': 30
        }
        
        response = authenticated_client.post('/api/workouts',
                                           data=json.dumps(workout_data),
                                           content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'workout' in data
        assert data['workout']['exercise'] == 'Running'
        assert data['workout']['duration'] == 30
        assert 'calories' in data['workout']
    
    def test_add_workout_missing_fields(self, authenticated_client):
        """Test adding workout with missing fields"""
        workout_data = {
            'category': 'Workout'
        }
        
        response = authenticated_client.post('/api/workouts',
                                           data=json.dumps(workout_data),
                                           content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_add_workout_invalid_duration(self, authenticated_client):
        """Test adding workout with invalid duration"""
        workout_data = {
            'category': 'Workout',
            'exercise': 'Swimming',
            'duration': -10
        }
        
        response = authenticated_client.post('/api/workouts',
                                           data=json.dumps(workout_data),
                                           content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_get_workouts(self, authenticated_client):
        """Test retrieving workouts"""
        # Add some workouts first
        workouts = [
            {'category': 'Warm-up', 'exercise': 'Stretching', 'duration': 10},
            {'category': 'Workout', 'exercise': 'Cycling', 'duration': 45},
            {'category': 'Cool-down', 'exercise': 'Walking', 'duration': 5}
        ]
        
        for workout in workouts:
            authenticated_client.post('/api/workouts',
                                    data=json.dumps(workout),
                                    content_type='application/json')
        
        # Get all workouts
        response = authenticated_client.get('/api/workouts')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'workouts' in data
    
    def test_workout_summary(self, authenticated_client):
        """Test workout summary statistics"""
        # Add workouts
        workouts = [
            {'category': 'Cardio', 'exercise': 'Running', 'duration': 30},
            {'category': 'Strength', 'exercise': 'Push-ups', 'duration': 15},
            {'category': 'Cardio', 'exercise': 'Cycling', 'duration': 20}
        ]
        
        for workout in workouts:
            authenticated_client.post('/api/workouts',
                                    data=json.dumps(workout),
                                    content_type='application/json')
        
        # Get summary
        response = authenticated_client.get('/api/workouts/summary')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'summary' in data
        
        summary = data['summary']
        assert summary['total_workouts'] == 3
        assert summary['total_duration'] == 65
        assert 'by_category' in summary
        assert 'weekly_stats' in summary


class TestPages:
    """Test page rendering"""
    
    def test_index_page(self, client):
        """Test index page"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_login_page(self, client):
        """Test login page"""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_register_page(self, client):
        """Test register page"""
        response = client.get('/register')
        assert response.status_code == 200
    
    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication"""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login
    
    def test_dashboard_authenticated(self, authenticated_client):
        """Test dashboard with authentication"""
        response = authenticated_client.get('/dashboard')
        assert response.status_code == 200
    
    def test_workouts_page(self, authenticated_client):
        """Test workouts page"""
        response = authenticated_client.get('/workouts')
        assert response.status_code == 200
    
    def test_progress_page(self, authenticated_client):
        """Test progress page"""
        response = authenticated_client.get('/progress')
        assert response.status_code == 200
    
    def test_diet_page(self, authenticated_client):
        """Test diet page"""
        response = authenticated_client.get('/diet')
        assert response.status_code == 200


class TestHelperFunctions:
    """Test helper functions"""
    
    def test_calculate_calories(self):
        """Test calorie calculation"""
        # Test with known values
        calories = calculate_calories('Workout', 60, 70)
        expected = 6.0 * 70 * 1  # MET * weight * hours
        assert calories == expected
        
        # Test warm-up
        calories = calculate_calories('Warm-up', 30, 60)
        expected = 3.0 * 60 * 0.5
        assert calories == expected
    
    def test_generate_diet_plan(self):
        """Test diet plan generation"""
        # Test for normal BMI
        plan = generate_diet_plan(2000, 22)
        assert 'protein' in plan
        assert 'carbs' in plan
        assert 'fats' in plan
        assert 'recommendations' in plan
        assert len(plan['recommendations']) > 0
        
        # Verify macro calculations
        assert plan['protein'] > 0
        assert plan['carbs'] > 0
        assert plan['fats'] > 0
        
        # Test for underweight
        plan_underweight = generate_diet_plan(2000, 17)
        assert any('calorie' in rec.lower() for rec in plan_underweight['recommendations'])
        
        # Test for overweight
        plan_overweight = generate_diet_plan(2000, 27)
        assert any('processed' in rec.lower() or 'protein' in rec.lower() 
                  for rec in plan_overweight['recommendations'])


class TestBMICalculation:
    """Test BMI and BMR calculations during registration"""
    
    def test_bmi_calculation(self, client):
        """Test BMI is calculated correctly"""
        user_data = {
            'username': 'bmitest',
            'password': 'pass123',
            'name': 'BMI Test',
            'age': 30,
            'gender': 'male',
            'height': 175,  # 1.75m
            'weight': 70    # 70kg
        }
        
        client.post('/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        user = users_db['bmitest']
        expected_bmi = 70 / (1.75 ** 2)
        assert abs(user['bmi'] - expected_bmi) < 0.1
    
    def test_bmr_calculation_male(self, client):
        """Test BMR calculation for male"""
        user_data = {
            'username': 'bmrmale',
            'password': 'pass123',
            'name': 'BMR Male',
            'age': 30,
            'gender': 'male',
            'height': 180,
            'weight': 75
        }
        
        client.post('/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        user = users_db['bmrmale']
        # Mifflin-St Jeor: 10*weight + 6.25*height - 5*age + 5
        expected_bmr = 10 * 75 + 6.25 * 180 - 5 * 30 + 5
        assert abs(user['bmr'] - expected_bmr) < 1
    
    def test_bmr_calculation_female(self, client):
        """Test BMR calculation for female"""
        user_data = {
            'username': 'bmrfemale',
            'password': 'pass123',
            'name': 'BMR Female',
            'age': 25,
            'gender': 'female',
            'height': 165,
            'weight': 60
        }
        
        client.post('/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        user = users_db['bmrfemale']
        # Mifflin-St Jeor: 10*weight + 6.25*height - 5*age - 161
        expected_bmr = 10 * 60 + 6.25 * 165 - 5 * 25 - 161
        assert abs(user['bmr'] - expected_bmr) < 1


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_workout_list(self, authenticated_client):
        """Test with no workouts"""
        response = authenticated_client.get('/api/workouts/summary')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['summary']['total_workouts'] == 0
        assert data['summary']['total_duration'] == 0
    
    def test_multiple_workouts_same_category(self, authenticated_client):
        """Test adding multiple workouts in same category"""
        for i in range(5):
            workout_data = {
                'category': 'Cardio',
                'exercise': f'Exercise {i}',
                'duration': 10 + i
            }
            
            response = authenticated_client.post('/api/workouts',
                                               data=json.dumps(workout_data),
                                               content_type='application/json')
            assert response.status_code == 200
        
        # Verify all workouts are stored
        response = authenticated_client.get('/api/workouts')
        data = json.loads(response.data)
        assert len(data['workouts']['Cardio']) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=app', '--cov-report=html'])
