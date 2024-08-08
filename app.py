from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pybreaker
import redis
from config import Config

app = Flask(__name__)
config = Config()
app.config.from_object(config)
db = SQLAlchemy(app)

# Initialize Redis client with SSL parameters correctly configured
#redis_url = app.config['REDIS_URL']
redis_client = redis.Redis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    password=app.config['REDIS_PASSWORD'],
    ssl=app.config['REDIS_SSL']
)
#redis_client = redis.Redis.from_url(redis_url, ssl=True)

# Initialize the CircuitBreaker
circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

@app.route('/users', methods=['GET'])
@circuit_breaker
def get_users():
    try:
        users = db.session.execute('SELECT * FROM users').fetchall()
        return jsonify([dict(row) for row in users])
    except pybreaker.CircuitBreakerError:
        cached_users = redis_client.lrange('users', 0, -1)
        return jsonify([user.decode('utf-8') for user in cached_users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_user/<name>', methods=['POST'])
def add_user(name):
    try:
        sql_statement = text('INSERT INTO users (name) VALUES (:name)')
        db.session.execute(sql_statement, {'name': name})
        db.session.commit()
        return jsonify({'message': 'User added successfully'}), 201
    except Exception as e:
        # If the SQL database connection fails, write the user data to Redis
        try:
            redis_client.rpush('users', name)
            return jsonify({'message': 'SQL connection failed. User data written to Redis'}), 201
        except Exception as redis_error:
            return jsonify({'error': str(redis_error)}), 500
        
@app.route('/redis_users', methods=['GET'])
def get_redis_users():
    try:
        cached_users = redis_client.lrange('users', 0, -1)
        return jsonify([user.decode('utf-8') for user in cached_users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/circuit_status', methods=['GET'])
def circuit_status():
    # Retrieve the state of the circuit breaker
    state = circuit_breaker.state
    return jsonify({'state': str(state)}), 200

if __name__ == '__main__':
    app.run(debug=True)

