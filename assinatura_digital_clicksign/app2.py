import httpx
import json

host = 'https://sandbox.clicksign.com'
headers = {'Content-Type': 'application/json',
           'Accept': 'application/json',
           'Connection': 'keep-alive',
           'access_token': '7e9dc98f-3e49-4d90-a7f1-ada90f427b01',
           'doc_key': '10714765-2578-41c8-91cb-13336fda9be5'}

access_token = '7e9dc98f-3e49-4d90-a7f1-ada90f427b01'
doc_key = '10714765-2578-41c8-91cb-13336fda9be5'

payload = {
  "document": {
    "path": "/rod/rodrigo.pdf",
    "template": {
      "data": ''
    }
  }
}

criacao_termo_url = f'https://sandbox.clicksign.com/api/v1/templates/{doc_key}/documents?access_token={access_token} HTTP/1.1'

#response = requests.post(url=criacao_termo_url, json=payload, headers=headers)

response = requests.post(url=criacao_termo_url, json=payload, headers=headers)

print(criacao_termo_url)
print(response.json())
# if __name__ == '__main__':
#     app.run(debug=True)