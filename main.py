import requests
import pandas as pd


API_KEY = '83c88a6c30f00a4eadc0f2d2245b07db'


def nov_api():
    url = "https://api.novaposhta.ua/v2.0/json/"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "apiKey": API_KEY,
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  
        
        if 'data' in data:
            return data['data']
        else:
            print('No data found in response')
            return []

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return []
    except ValueError:
        print("Error parsing JSON response")
        return []
        
        
        
def get_exl():
    pass 


if __name__ == '__main__':
    nov_api()
    get_exl()