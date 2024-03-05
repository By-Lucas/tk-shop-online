import apps.helpers.redis as redis


class Redis:
    def __init__(self) -> None:
        self.r = redis.Redis(
            host='redis-15109.c267.us-east-1-4.ec2.cloud.redislabs.com',
            port=15109,
            password='hi8gjjFxzkWMd8MACOG6iIO8j9AfFSgK'
        )

    def get_tasks(self, key_filter='*'):
        keys = self.r.keys(key_filter)
        values = self.r.mget(keys)
        
        for k, v in zip(keys, values):
            print(k, v)

    def get_task(self, key):
        value = self.r.get(key)
        return value

    def delete_task(self, key):
        result = self.r.delete(key)
        return result
    
    def delete_all_tasks(self):
        self.r.flushdb()


if __name__ == "__main__":
    r = Redis()
    print(r.delete_all_tasks())