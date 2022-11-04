import requests

response = requests.delete('http://127.0.0.1:5000/adverts/2',
                         json={'title': 'test-title1111',
                               'discription': 'Test-test-test 12-45-56 1111',
                               'owner': 'Test Testov 111'}
                         )
print(response.text)
