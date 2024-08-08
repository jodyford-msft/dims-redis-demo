import redis

# Parse the connection string components
redis_host = 'dims-redis.redis.cache.windows.net'
redis_port = 6380
redis_password = ''
redis_ssl = True

# Initialize Redis client
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    ssl=redis_ssl
)

# Example usage of the Redis client
try:
    redis_client.ping()
    print("Connected to Redis successfully!")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")