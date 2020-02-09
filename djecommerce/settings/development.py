from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost',
                 'voo.asuscomm.com', 'kirsanov.ga', '192.168.1.4']

INSTALLED_APPS += [
    'debug_toolbar',
    'robokassa'
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

# DEBUG TOOLBAR SETTINGS

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STRIPE_PUBLIC_KEY = ''
STRIPE_SECRET_KEY = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


ROBOKASSA_LOGIN = 'bestboard'
ROBOKASSA_PASSWORD1 = "HZQXfkB5d1Fd1zWj3tR3"
ROBOKASSA_PASSWORD1_T = "rOGKmIVFRbq9o6it01q7"
ROBOKASSA_PASSWORD2 = "MfIgrQP1oEj80o20pluV"
ROBOKASSA_PASSWORD2_T = "oisI4I4HRFk8ZYpKxW81"
ROBOKASSA_USE_POST = True
ROBOKASSA_STRICT_CHECK = True
ROBOKASSA_FIX_PRICE_URL_EXAMPLE = "https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=demo&OutSum=11.00&InvId=&Description=%D0%9E%D0%BF%D0%BB%D0%B0%D1%82%D0%B0%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%20%D0%B2%20%D0%A2%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D0%BE%D0%BC%20%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%D0%B5%20ROBOKASSA&shp_Item=1&Culture=ru&Encoding=utf-8&Receipt=%7B%22sno%22%3A%22osn%22%2C%22items%22%3A%5B%7B%22name%22%3A%22%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F%20%D0%BF%D0%BE%20ROBOKASSA%22%2C%22quantity%22%3A1.0%2C%22sum%22%3A6.0%2C%22tax%22%3A%22vat18%22%7D%2C%7B%22name%22%3A%22%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F%20%D0%BF%D0%BE%20Robo.market%22%2C%22quantity%22%3A1.0%2C%22sum%22%3A5.0%2C%22tax%22%3A%22vat18%22%7D%5D%7D&SignatureValue=3925b771e47d405cbcbb492daa936824"
ROBOKASSA_FLOAT_PRICE_URL_EXAMPLE = "https://auth.robokassa.ru/Merchant/PaymentForm/FormFLS.if?MerchantLogin=demo&InvoiceID=0&Culture=ru&Encoding=utf-8&Description=%D0%9A%D0%BE%D0%BD%D1%81%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5%20%D1%83%D1%81%D0%BB%D1%83%D0%B3%D0%B8&DefaultSum=10&SignatureValue=fc70d74f720d476d5e2c30be8ec6e52c#"

# TODO: Оставить только qiwi 

QIWI_P2P_KEYS_NAME = "BoostedBoardShop"
QIWI_P2P_SERVER_NOTIFY_URL = "http://voo.asuscomm.com/payment/qiwi/result/"
QIWI_P2P_SECRET_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjZmOGYyYzU3LTQxNzgtNDY0YS1iNTE1LWJkMjI2ODYwMmJkNiIsInVzZXJfaWQiOiI3OTIxNDQ0NzM0NCIsInNlY3JldCI6IjAxY2E1MWFhNGYxYTI5NmZhNDM3MzNiYmJmZGRjYWM1ZWJlNWIwYjdmY2MyMTVlNzdjMTE1ZTI2ZDZhNjZiYzAifX0="
QIWI_P2P_PUBLIC_KEY = "2S7mpWSvB93qSAr7uYNu2Vvnd2pTVzxEviw6chKKbG9xyy9pcxcvrmne6c6m7cUabcbN8Gnkjk77SEeN2YVBiZonKCsrsptQcSjQzpTkz1yjffhwH2qVg6eYAkVsfXhGjG2XqZFqqzdpJESEWyRvFSva47eEmWLLpPko6CFLQ3w5aecrzCvWaz7ZKXyZMhrKe5cxCMdAUbwJJ1FGyNF18ctNKSjtpTRnuZ"