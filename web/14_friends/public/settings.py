import os

DATA_PREFIX = 'data/'
UPLOAD_PREFIX = 'static/'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg',)
FORM_FIELD_NAMES = {
    'name': 'full_name',
    'photos': 'photos',
}
APP_BASE = os.path.dirname(__file__)
SECRET_KEY = b'\xec\x08\xd1\x98\x86\x07\xf9E\xab6\x7f\xef\xb8\x14\xa1\x8a\xfa\xc8Vz\xceZA"\xe0\x8c[}\xdeE\xee\xfa'
