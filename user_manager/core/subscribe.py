import redis

# Connect to local Redis instance
r = redis.Redis(host='localhost', port=6379, db=0)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
channel = 'drawing_help'


def produce_message(channel, message):
    # Use a Redis set to check for duplicates
    if not r.sismember(f"{channel}_set", message):
        # Add the message to the set
        r.sadd(f"{channel}_set", message)
        # Push the message onto the list
        r.rpush(channel, message)
        print(f"Produced message: {message} to channel: {channel}")
    else:
        print(f"Duplicate message: {message} not added to channel: {channel}")


while True:
    message = input("Enter a message: ")
    produce_message(channel, message)
