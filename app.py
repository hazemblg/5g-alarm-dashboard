from flask import Flask, render_template, request, jsonify, redirect, session
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object('config.Config')

# Mock user data (until database is ready)
MOCK_USERS = {
    'admin': {
        'password': 'admin123',
        'role': 'admin',
        'email': 'admin@orange.com',
        'full_name': 'Administrator'
    },
    'operator': {
        'password': 'operator123',
        'role': 'operator',
        'email': 'operator@orange.com',
        'full_name': 'Operator'
    },
    'hazemblg': {
        'password': 'hazem1234',
        'role': 'admin',
        'email': 'hazem.benbelgacem@enetcom.u-sfax.tn',
        'full_name': 'Hazem Ben Belgacem'
    }
}

# Configuration
STREAMLIT_URL = 'http://localhost:8501'
JWT_SECRET = app.config['JWT_SECRET_KEY']
JWT_ALGORITHM = 'HS256'

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        # Already logged in, redirect to Streamlit
        return redirect(STREAMLIT_URL)
    return redirect('/login')

@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect(STREAMLIT_URL)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# API Endpoints
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate credentials
        if username in MOCK_USERS and MOCK_USERS[username]['password'] == password:
            user = MOCK_USERS[username]

            # Store in Flask session
            session['user_id'] = username
            session['role'] = user['role']
            session['email'] = user['email']
            session['full_name'] = user['full_name']

            # Generate JWT token for Streamlit
            token = jwt.encode({
                'username': username,
                'email': user['email'],
                'role': user['role'],
                'full_name': user['full_name'],
                'exp': datetime.utcnow() + timedelta(hours=8)
            }, JWT_SECRET, algorithm=JWT_ALGORITHM)

            # Return Streamlit URL with token
            streamlit_url_with_token = f"{STREAMLIT_URL}/?token={token}"

            return jsonify({
                'success': True,
                'message': 'Login successful',
                'redirect_url': streamlit_url_with_token,
                'user': {
                    'username': username,
                    'role': user['role'],
                    'full_name': user['full_name']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500


@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@app.route('/api/verify-token', methods=['POST'])
def api_verify_token():
    """Endpoint for Streamlit to verify JWT tokens"""
    try:
        data = request.get_json()
        token = data.get('token')

        if not token:
            return jsonify({'success': False, 'message': 'No token provided'}), 401

        # Decode and verify token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        return jsonify({
            'success': True,
            'user': {
                'username': payload.get('username'),
                'email': payload.get('email'),
                'role': payload.get('role'),
                'full_name': payload.get('full_name')
            }
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚨 DRS Alarms - Flask Authentication Server")
    print("="*60)
    print("\n📡 Login Server: http://localhost:5000")
    print("📊 Dashboard (Streamlit): http://localhost:8501")
    print("\n👤 Test Credentials:")
    print("   Admin: admin / admin123")
    print("   Operator: operator / operator123")
    print("   Hazem: hazemblg / hazem1234")
    print("\n" + "="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
