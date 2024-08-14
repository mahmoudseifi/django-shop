import requests
import json


class NovinoPay:
    _payment_request_url = "https://api.novinopay.com/payment/ipg/v2/request"
    _payment_verification_url = "https://api.novinopay.com/payment/ipg/v2/verification"
    _callback_url = "https://localhost/Callback"

    def __init__(self, merchant_id):
        self.merchant_id = merchant_id
        
    def payment_request(self, amount):
        payload = {
        "merchant_id": self.merchant_id,
        "amount": str(amount),
        "callback_url": self._callback_url
        }
        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }

        response = requests.post(self._payment_request_url, headers=headers, data=json.dumps(payload))
    
        return response.json()
    
    def payment_verification(self, amount, authority):
        payload = {
        "merchant_id": self.merchant_id,
        "amount": str(amount),
        "authority": authority
        }
        headers = {
        'Content-Type': 'application/json'
        }
        
        response = requests.post(self._payment_verification_url, headers=headers, data=json.dumps(payload))

        return response.json()



if __name__ == "__main__":
    novinopay = NovinoPay(merchant_id="Test")
    
    response = novinopay.payment_request(10000)
    print(response)
    
    input("generate payment url")
    print(response["data"]["payment_url"])
    
    input("generate verification url")
  
    response = novinopay.payment_verification(10000, response["data"]["authority"] )
    print(response)