# utils/callback_data.py

import base64

def encode_callback_data(data):
    """Убедитесь, что данные обратного вызова не превышают лимит Telegram и содержат только допустимые символы."""
    return base64.urlsafe_b64encode(data.encode('utf-8')).decode('utf-8')[:64]

def decode_callback_data(data):
    """Декодировать данные обратного вызова, закодированные в base64."""
    return base64.urlsafe_b64decode(data.encode('utf-8')).decode('utf-8')