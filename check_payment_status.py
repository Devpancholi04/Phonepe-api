import requests
import hashlib

merchantId = "PGTESTPAYUAT86"
salt_key = "96434309-7796-489d-8924-ab56988a6076"
salt_index = 1

def generate_xverify(merchantTransactionId,salt_key, salt_index):
    global sha256_data
    sha256_data = f'/pg/v1/status/{merchantId}/{merchantTransactionId}{salt_key}'
    print(f"\ndata to hash = {sha256_data}")
    
    hash_data = hashlib.sha256(sha256_data.encode('utf-8')).hexdigest()
    print(f"\nhash data = {hash_data}")
    
    x_verify = f'{hash_data}###{salt_index}'
    print(f"x-verify = {x_verify} ")
    return x_verify

def check_status(merchantId, merchantTransactionId, salt_key):    
    api = f"https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchantId}/{merchantTransactionId}"
    
    x_verify = generate_xverify(transactionId, salt_key, salt_index)
    
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "X-VERIFY" : x_verify,
        "X-MERCHANT-ID": merchantId
        }
    
    respond= requests.get(api ,headers=headers)  
    print(respond.text)    
    
if __name__ == '__main__':
    
    transactionId = 'TXN7641011dev125421456987453'
    
    check_status(merchantId, transactionId, salt_key)