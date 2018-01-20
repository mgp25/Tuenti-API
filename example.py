from tuenti.tuenti_api import TuentiAPI

phone_number = '' # Format: 34123456789
password = ''
installation_id = ''
appsFlyersKey

tuenti = TuentiAPI(phone_number,
password,
installation_id,
None,
None,
True)

try:
    tuenti.login()
    tuenti.get_sync_info()
except Exception as e:
    tuenti.login()
