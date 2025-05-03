from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType

commerce_code = '597055555532'  # Código oficial de pruebas Webpay Plus
api_key = 'X' * 32       # Clave oficial de pruebas Webpay Plus
integration_type = IntegrationType.TEST

options = WebpayOptions(commerce_code, api_key, integration_type)
transaction = Transaction(options)
