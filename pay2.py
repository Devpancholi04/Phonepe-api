import requests
import json
import time
import base64
import hashlib
import webbrowser

#https://stackoverflow.com/questions/78407973/i-am-trying-to-resolve-phonepe-payment-integration-error-in-flutter
api =  "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"
#salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
salt_key = "96434309-7796-489d-8924-ab56988a6076"
salt_index = 1
merchant_id = "PGTESTPAYUAT86"
#environment = "test"


def generate_xverify(payload, salt_key, salt_index):
    global encoded_str
    encode = base64.b64encode(payload)
    print(f'encode : {encode}')
    encoded_str = encode.decode("utf-8")
    print(f"encode : {encoded_str}")
    
    data = f"{encoded_str}/pg/v1/pay{salt_key}"
    print(f"\nData to hash: {data}")
    
    hash_data = hashlib.sha256(data.encode('utf-8')).hexdigest() 
    print(f"\nHash Data: {hash_data}")
    
    x_verify = f'{hash_data}###{salt_index}'
    return x_verify

def payment(transaction_id, user_id,amount, customer_no, callbackUrl):
    payload = {
       "merchantId": merchant_id,
        "merchantTransactionId": transaction_id,
        "merchantUserId": user_id,
        "amount": amount,
        "redirectUrl": "http://annc.com",
        #"redirectUrl": "http://127.0.0.1:5500/redirect.html",
        "redirectMode": "REDIRECT",
        "callbackUrl": callbackUrl,
        "mobileNumber": customer_no,
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }
    
    
    payload_str = json.dumps(payload)
    payload_str = payload_str.encode('utf-8')
    print(f"\nPayload: {payload_str}")
    #print(payload_str)
    xverify = generate_xverify(payload_str, salt_key, salt_index)
    print(f"\nX-VERIFY: {xverify}") 
    #print(xverify)
    
    data = {
        'request' : encoded_str 
        }
    
    headers = {
        "Accept"  : "application/json",
        "Content-Type" : "application/json",
        "X-VERIFY" : xverify
        }
    
    
    retry = 0
    while retry < 5:
            global respond
            respond = requests.post(api, json = data, headers = headers) 
            if respond.status_code == 429:
                retry += 1
                print("retrying...")
                time.sleep(10)
            elif respond.status_code == 200:
                print(respond.json())
                get_url = respond.json()
                #print('\n',get_url)
                redirect = get_url['data']['instrumentResponse']['redirectInfo']['url']
                print(f"redirect_url = {redirect}")
                webbrowser.open(redirect)
                break
            else:
                print(f"error : {respond.status_code}")
                print(respond.text)
                break
    else:
        raise ("unable to process failed in all 5 attemps")
        
    
    
    

if __name__ == "__main__":
    merchantTransactionId = "TXN7641011dev125421456987453"
    user_id = "USER12389745698756231478956"
    amount = 10000
    customer_no = '8120098465'
    callbackUrl = 'http://annc.com'
    #callbackUrl = 'http://127.0.0.1:5500/redirect.html'
    
    try:
        payment(merchantTransactionId, user_id, amount, customer_no, callbackUrl)
        if respond.status_code == 200:
            print("payment success")
        else:
            print("payment Failed")
    except Exception as e:
        print(f'error {e}')
