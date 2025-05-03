import os
import jwt
import redis
import hvac
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

# Redis für Session-Management
redis_client = redis.Redis(host='redis', port=6379)

# Vault Client für Secrets
vault_client = hvac.Client(
    url=os.environ['VAULT_ADDR'],
    token=os.environ['VAULT_TOKEN']
)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token fehlt!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return f(*args, **kwargs)
        except:
            return jsonify({'message': 'Ungültiger Token!'}), 401
    return decorated

@app.route('/auth/validate', methods=['POST'])
def validate_token():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'valid': False}), 401
    
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'valid': True}), 200
    except:
        return jsonify({'valid': False}), 401

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Validiere Credentials gegen Vault
    try:
        result = vault_client.auth.userpass.login(
            username=username,
            password=password
        )
        if result['auth']:
            # Generiere JWT Token
            token = jwt.encode(
                {'user': username},
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            # Speichere Token in Redis
            redis_client.setex(
                f"token:{username}",
                3600,  # 1 Stunde Gültigkeit
                token
            )
            return jsonify({'token': token}), 200
    except:
        pass
    
    return jsonify({'message': 'Ungültige Credentials'}), 401

@app.route('/auth/logout', methods=['POST'])
@require_auth
def logout():
    token = request.headers.get('Authorization')
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data.get('user')
        # Lösche Token aus Redis
        redis_client.delete(f"token:{username}")
        return jsonify({'message': 'Logout erfolgreich'}), 200
    except:
        return jsonify({'message': 'Fehler beim Logout'}), 400

if __name__ == '__main__':
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.run(host='0.0.0.0', port=8444)