import os

pandora_credentials = {
    'ENCRYPTION_KEY': os.getenv('PANDORA_ENCRYPTION_KEY', '6#26FRL$ZWD'),
    'DECRYPTION_KEY': os.getenv('PANDORA_DECRYPTION_KEY', 'R=U!LH$O2B#'),
    'PARTNER_USER': os.getenv('PANDORA_PARTNER_LOGIN', 'android'),
    'PARTNER_PASSWORD': os.getenv('PANDORA_PARTNER_PASSWORD', 'AC7IBG09A3DTSYM4R41UJWL07VLN8JI7'),
    'DEVICE': os.getenv('PANDORA_DEVICE', 'android-generic'),
    'USERNAME': os.getenv('PANDORA_USER', 'user'),
    'PASSWORD': os.getenv('PANDORA_PASSWORD', 'password')
}
