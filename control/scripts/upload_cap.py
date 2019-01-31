import requests


cookie = {'key': '7fcb3ff5176fb532124b5ac3e4616a04'}
file = 'home.cap'
url = 'https://wpa-sec.stanev.org/?submit'
files = {'file': open(file, 'rb')}

r = requests.post(url, files=files, cookies=cookie)
print(r.content)
