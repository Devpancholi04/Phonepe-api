import requests
import json
import time
import hashlib
import pay2 as p


#transactionId = p.merchantTransactionId
merchantId = "PGTESTPAYUAT86"
salt_key = "96434309-7796-489d-8924-ab56988a6076"
salt_index = 1

def generate_xverify(merchantTransactionId,salt_key, salt_index):
    #sha256_data = f'/v3/transaction/{merchantId}/{transactionId}/status{salt_key}'
    sha256_data = f'/pg/v1/status/{merchantId}/{merchantTransactionId}{salt_key}'
    print(f"\ndata to hash = {sha256_data}")
    
    hash_data = hashlib.sha256(sha256_data.encode('utf-8')).hexdigest()
    print(f"\nhash data = {hash_data}")
    
    x_verify = f'{hash_data}###{salt_index}'
    print(f"x-verify = {x_verify} ")
    return x_verify

def check_status(payload, merchantId, transactionId, salt_key):    
    api = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchantId}/{merchantTransactionId}"
    
    x_verify = generate_xverify(transactionId, salt_key, salt_index)
    
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "X-VERIFY" : x_verify,
        "X-MERCHANT-ID": merchantId
        }
    
    respond= requests.get(api,json = payload, headers=headers)
    respond.raise_for_status()
    print(respond.text)
    
#print(transactionId)

#print(api)

if __name__ == '__main__':
    transactionId = 'TXN7641011dev125421456987453'
    
    check_status(p.payload, merchantId, transactionId, salt_key)