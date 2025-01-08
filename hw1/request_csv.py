import requests

file_path = 'data/cars_test.csv'

with open(file_path, 'rb') as f:
    files = {'file': ('filename.csv', f)}

    response = requests.post(
        'http://127.0.0.1:8000/predict_items',
    files=files,
    )

if response.status_code == 200:
    with open('data/csv_predicted.csv','wb') as out_file:
        out_file.write(response.content)
else:
    print(f"Ошибка при получении данных: {response.text}")