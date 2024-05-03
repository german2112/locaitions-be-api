from bson import json_util
import json
import hashlib

def parse_json(data):
    return json.loads(json_util.dumps(data))

def encode_string_to_integer(input: str):
    hashedValue = hashlib.sha256(input.encode()).hexdigest()
    return int(hashedValue[:7], 16)