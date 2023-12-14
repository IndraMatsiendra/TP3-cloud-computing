import usermodule
import redis
import os
import json
from time import sleep
from datetime import datetime


class Context:
    def __init__(self):
        self.host = os.environ.get('REDIS_HOST')
        self.port = int(os.environ.get('REDIS_PORT'))
        self.input_key = os.environ.get('REDIS_INPUT_KEY')
        self.output_key = os.environ.get('REDIS_OUTPUT_KEY')
        self.function_getmtime = os.path.getmtime('usermodule.py')
        self.last_execution = None
        self.env = {}
        
context = Context()
redis_db = redis.Redis(host=context.host, port=context.port)
old_input = redis_db.get(os.environ.get('REDIS_INPUT_KEY'))
while True:
    new_input = redis_db.get(os.environ.get('REDIS_INPUT_KEY'))
    if new_input != old_input:
        old_input = new_input
        context.function_getmtime = os.path.getmtime('usermodule.py')
        context.last_execution = datetime.now()
        output = usermodule.handler(json.loads(new_input.decode('utf-8')), context)
        output_json = json.dumps(output)
        redis_db.set(os.environ.get('REDIS_OUTPUT_KEY'), output_json)
    sleep(5)