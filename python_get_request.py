import requests

resp = requests.get('https://jsonplaceholder.typicode.com/users')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /companies {}'.format(resp.status_code))
for todo_item in resp.json():
    print('{} {}'.format(todo_item['id'], todo_item['summary']))
