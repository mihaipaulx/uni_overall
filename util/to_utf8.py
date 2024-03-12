import json

def to_utf8(data):
  json_data = json.dumps(data)
  utf8_data = json_data.encode('utf-8')
  return utf8_data