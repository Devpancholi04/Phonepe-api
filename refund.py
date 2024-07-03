import requests
import base64
import hashlib
import json

api = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/refund"
salt_key = "96434309-7796-489d-8924-ab56988a6076"
salt_index = 1
merchant_id = "PGTESTPAYUAT86"

def generate_xverify_for_refund(payload, salt_key, salt_index):
    encode = base64.b64encode(payload)
    print(f"encode : {encode}")
    encoded_str = encode.decode("utf8")
    print(f"encoded_str : {encoded_str}")
    
    data = f'{encoded_str}/pg/v1/refund{salt_key}'
    print(f"data to hash : {data}")
    
    hash_data = hashlib.sha256(data.encode('utf-8')).hexdigest() 
    print(f"hashed data : {hash_data}")
    
    x_verify = f'{hash_data}###{salt_index}'
    print(f"X-verify : {x_verify}")
    
    return x_verify, encoded_str

def refund_init(user_id, merchantTransactionId, originalTransactionId):
    payload = {
        "merchantId" : merchant_id,
        "merchantUserId" : user_id,
        "merchantTransactionId" : merchantTransactionId,
        "originalTransactionId" : originalTransactionId,
        "amount" : 10000,
        "callbackUrl" : "http://annc.com"
    }
    
    payload_str = json.dumps(payload)
    payload_str = payload_str.encode('utf-8')
    print(f"\nencoded_payload : {payload_str}")
    
    x_verify, request = generate_xverify_for_refund(payload_str, salt_key, salt_index)
    
    data = {
        "request" : request
        }
    
    headers = {
        "Accept" : "application/json",
        "Content-Type" :"application/json",
        "X-VERIFY" : x_verify
        }
    
    respond = requests.post(api, json = data, headers = headers)
    print()
    print(respond.text)
    
    
if __name__ == "__main__":
    user_id = "USER12389745698756231478956"
    merchant_transaction_Id = "TXN12354498845Dev56843168"
    originalTransactionId = "TXN7641011dev125421456987453"
    
    refund_init(user_id, merchant_transaction_Id, originalTransactionId)
    