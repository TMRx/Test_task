import unittest
import requests_mock
import pandas as pd
import os
from io import StringIO
from contextlib import redirect_stdout
import main  # Імпортуємо ваш основний файл main.py

class TestNovaposhta(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {
                'RegionDescription': 'Черкаська',
                'CityDescription': 'Черкаси',
                'Description': 'Відділення №1'
            },
            {
                'RegionDescription': 'Львівська',
                'CityDescription': 'Львів',
                'Description': 'Відділення №2'
            }
        ]

    @requests_mock.Mocker()
    def test_nov_api_success(self, mock_request):
        mock_request.post('https://api.novaposhta.ua/v2.0/json/', 
                          json={'success': True, 'data': self.test_data})
        
        result = main.nov_api()
        self.assertEqual(result, self.test_data)

    @requests_mock.Mocker()
    def test_nov_api_error(self, mock_request):
        mock_request.post('https://api.novaposhta.ua/v2.0/json/', 
                          status_code=500)
        
        result = main.nov_api()
        self.assertEqual(result, [])

    @requests_mock.Mocker()
    def test_nov_api_no_data(self, mock_request):
        mock_request.post('https://api.novaposhta.ua/v2.0/json/', 
                          json={'success': True})
        
        result = main.nov_api()
        self.assertEqual(result, [])

    def test_get_exl_success(self):
        filename = 'test_output.xlsx'
        main.get_exl(self.test_data, filename)
        
        self.assertTrue(os.path.exists(filename))
        
        df = pd.read_excel(filename)
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['Область'], 'Київська')
        
        os.remove(filename)

    def test_get_exl_empty_data(self):
        filename = 'test_empty.xlsx'
        
        f = StringIO()
        with redirect_stdout(f):
            main.get_exl([], filename)
        
        self.assertIn("Помилка: No data received", f.getvalue())
        self.assertFalse(os.path.exists(filename))

    @requests_mock.Mocker()
    def test_main_execution(self, mock_request):
        mock_request.post('https://api.novaposhta.ua/v2.0/json/', 
                          json={'success': True, 'data': self.test_data})
        
        f = StringIO()
        with redirect_stdout(f):
            api_data = main.nov_api()
            if api_data:
                main.get_exl(api_data)
        
        self.assertIn("Дані збережено у файл poshta_data.xlsx", f.getvalue())
        self.assertTrue(os.path.exists("poshta_data.xlsx"))
        os.remove("poshta_data.xlsx")

if __name__ == '__main__':
    unittest.main()