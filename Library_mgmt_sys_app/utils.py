import json

def validate_schema(self, params, allowed_keys=['name']):
    keys = params.keys()
    key_len = 0
    for key in allowed_keys:
        if key in keys:
            key_len += 1
    if len(keys) != key_len:
        raise ValidationError("Invalid data")

def validateJSON(self, meta_data):
    try:
        data = json.loads(meta_data)
    except Exception as ex:
        self.response['res_str'] = str(ex)
        return send_400(self.response)