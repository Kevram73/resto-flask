import requests

# url = 'http://kevram.pythonanywhere.com/admin/register'
url = 'http://localhost:2000/admin/register'
data = [
    {
        'email': 'eyramativon1@gmail.com',
        'username': 'Eyram Ativon',
    },
    {
        'email': 'info.odyca.immigration@gmail.com',
        'username': 'Charles Hubert',
    },
    {
        'email': 'cb.odyca.immigration@gmail.com',
        'username': 'Madame Christelle',
    },
]


# Send the POST request with JSON data
for datum in data:
    
    response = requests.post(url, json=datum)
    # Check the response
    if response.status_code == 200:
        print('POST request successful!')
    else:
        print('POST request failed. Status code:', response.status_code)
  
