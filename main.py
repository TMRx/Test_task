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
        data = response.json()
        
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
        
        
        
def get_exl(data, filename="poshta_data.xlsx"):
    try:
        if not data:
            raise ValueError("No data received")
        
        
        rows = []
        for entry in data:
            rows.append({
                "Область": entry.get('RegionDescription', ''),
                "Місто": entry.get('CityDescription', ''),
                "Відділення": entry.get('Description', '')
            })

        
        df = pd.DataFrame(rows)
        df.to_excel(filename, index=False)
        print(f'Дані зебережено у файл {filename}')
        
        
    except ValueError as ve:
        print(f"Помилка: {ve}")
    except KeyError as ke:
        print(f"Помилка: Відсутній ключ у даних - {ke}")
    except pd.errors.EmptyDataError:
        print("Помилка: Дані для збереження порожні.")
    except PermissionError:
        print(f"Помилка: Немає дозволу на запис файлу {filename}. Перевірте права доступу.")
    except Exception as e:
        print(f"Виникла непередбачена помилка: {e}")


if __name__ == '__main__':
    api_data = nov_api()
    if api_data: 
        get_exl(api_data)
    else:
        print("Не вдалося отримати дані з API.")    