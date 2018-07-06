from tuenti.tuenti_api import TuentiAPI
import datetime, time

###### Your Account Data #########
phone_number = '' # Format: 34123456789
password = ''
installation_id = '' #Format: 0123456789ABCDEF0123456789ABCDF (Required).
appsFlyersKey = '' # Format: 1234567891234-1231231 (Optional).
##################################

##################################
debug = False
dataFolder = None # Sets default folder
##################################

tuenti = TuentiAPI(phone_number,
password,
installation_id,
appsFlyersKey,
None,
debug)

try:
    tuenti.login()

    balance = tuenti.getBalance()[0]['response']

    expiration = balance['subscriptionBundles']['current']['extras'][0]['expiration']
    unbilled = balance['unbilledConsumption']['moneyAmount']['amount']
    remainingData = balance['subscriptionBundles']['current']['main']['counters'][0]['remaining']
    totalData = balance['subscriptionBundles']['current']['main']['counters'][0]['total']
    smsLeft = balance['subscriptionBundles']['current']['main']['counters'][1]['remaining']
    smsTotal = balance['subscriptionBundles']['current']['main']['counters'][1]['total']

    print('Se renueva el: {0}'.format(datetime.datetime.fromtimestamp(expiration).strftime('%d de %B')))
    print('Consumo desde la última factura: {0} €'.format('{:.2f}'.format(unbilled/1000)))
    print('Datos restantes: {0} MB de {1} MB'.format(remainingData, totalData))
    print('SMS restantes: {0} de {1}'.format(smsLeft, smsTotal))
except Exception as e:
    print(e)
