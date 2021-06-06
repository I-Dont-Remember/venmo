import os
from datetime import datetime
from venmo_api import Client, PaymentPrivacy
# requests is pulled in by venmo_api
import requests

TOKEN_KEY = 'VENMO_ACCESS_TOKEN'
GF_ID_KEY = 'GF_VENMO_USER_ID'
C_ID_KEY = 'C_USER_ID'
IFTTT_WEBHOOK_KEY = 'IFTTT_WEBHOOK'

def main():
    # load the access token from environ
    access_token = os.environ.get(TOKEN_KEY)
    if access_token is None:
        raise ValueError('[!] EVERYTHING IS BROKEN WE CANT GET ACCESSS AHHHHHH')

    venmo_client = Client(access_token=access_token)

    request_for_rent(venmo_client)
    request_for_internet(venmo_client)



def request_for_rent(venmo_client):
    amount = 400.0

    now = datetime.now()
    month_short_notation = now.strftime("%b")
    note = f'{month_short_notation} rent contribution'

    gf_venmo_user_id = os.environ.get(GF_ID_KEY)
    if gf_venmo_user_id is None:
        raise ValueError('[!] AHHHH NO GF USER ID TO CALL WITH LSJFLDSFJ:SDFJL:SJ')

    try:
        venmo_client.payment.request_money(amount, note, target_user_id=gf_venmo_user_id, privacy_setting=PaymentPrivacy.PRIVATE)
        print('Successfully requested for rent $$')
        msg = f'Requested ${amount} rent from GF.'
    except Exception as e:
        print(e)
        msg = '[!] Failed to request $$ for rent from GF'
    notify(msg)


def request_for_internet(venmo_client):
    amount = 40.0

    now = datetime.now()
    month_short_notation = now.strftime("%b")
    if month_short_notation not in ['Jun', 'Jul']:
        print('Quitting because no internet after end of July')
        notify('If you havent already, stop requesting internet from C.')
        return

    note = f'{month_short_notation} Interwebs'

    c_user_id = os.environ.get(C_ID_KEY)
    if c_user_id is None:
        raise ValueError('[!] AHHHH NO C User Id to use...')

    try:
        venmo_client.payment.request_money(amount, note, target_user_id=c_user_id, privacy_setting=PaymentPrivacy.PRIVATE)
        print('Successfully requested for internet $$')
        msg = f'Requested ${amount} Internet from C.'
    except Exception as e:
        print(e)
        msg = '[!] Failed to request $$ for internet from C'
    notify(msg)


def notify(msg):
    # notify with IFTTT webhook
    ifttt_webhook_url = os.environ.get(IFTTT_WEBHOOK_KEY)
    if ifttt_webhook_url is None:
        raise ValueError('[!] Dang, no webhook so cant notify myself :(')
    
    json_data = {
        'value1': msg
    }
    resp = requests.post(ifttt_webhook_url, json=json_data)
    print(resp.status_code)
    if resp.status_code >= 300:
        raise ValueError(f'Webhook resp was {resp.status_code}; not a success. Body: {resp.text}')

main()
