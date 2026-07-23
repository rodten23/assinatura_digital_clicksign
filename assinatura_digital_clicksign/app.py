import json
import os

import httpx
from dotenv import load_dotenv

from fastapi import FastAPI, Depends

app = FastAPI()

load_dotenv()

base_url = os.getenv('BASE_URL')
access_token = os.getenv('ACCESS_TOKEN')
template_id = os.getenv('TEMPLATE_ID')

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json'
}

@app.get('/conta')
def testar_conta() -> str:

    testar_conta_url = f'{base_url}/envelopes?access_token={access_token}'

    resposta_conta = httpx.get(
        url=testar_conta_url,
        verify=False)
    
    with open(
        './assinatura_digital_clicksign/resposta_conta.json',
        'w', encoding='utf-8') as response_file:
            json.dump(
                resposta_conta.json(),
                response_file,
                ensure_ascii=False,
                indent=4
            )

    with open(
        './assinatura_digital_clicksign/resposta_conta.json',
        'r',encoding='utf-8') as open_file:
            dados_conta = json.load(open_file)
        
    chave_conta = dados_conta['data'][0]['id']

    return chave_conta


@app.post('/envelopes')
def criar_envelope() -> str:

    criar_envelope_url = f'{base_url}/envelopes'

    body_envelope = json.dumps({
        'data': {
            'type': 'envelopes',
            'attributes': {
                'name': 'Envelope teste',
                'locale': 'pt-BR',
                'auto_close': True,
                'remind_interval': 3,
                'block_after_refusal': True,
                'deadline_at': '2026-10-20T00:00:00.000-03:00'
            }
        }
    })

    resposta_envelope = httpx.post(
            url=criar_envelope_url,
            data=body_envelope,
            headers=headers,
            verify=False
        )

    with open(
        './assinatura_digital_clicksign/resposta_envelope.json',
        'w', encoding='utf-8') as response_file:
        json.dump(
            resposta_envelope.json(),
            response_file,
            ensure_ascii=False,
            indent=4
        )

    with open(
            './assinatura_digital_clicksign/resposta_envelope.json',
            'r',encoding='utf-8') as open_file:
                dados_envelope = json.load(open_file)
    
    chave_envelope = dados_envelope['data']['id']
    
    return chave_envelope

# @app.post('/criar_signatario')
# def creation_signer() -> str:
    
#     creation_signer_url = f'{base_url}/signers?access_token={access_token}'

#     signer_data = json.dumps({
#         'signer': {
#             'email': 'testador@testador.com',
#             'phone_number': '11988776655',
#             'auths': [
#                 'sms'
#             ],
#             'name': 'Testador Que Assina',
#             'documentation': '123.480.920-69',
#             'communicate_by': 'email',
#             'has_documentation': 'true',
#             'selfie_enabled': 'false',
#             'handwritten_enabled': 'false',
#             'location_required_enabled': 'true',
#             'official_document_enabled': 'false',
#             'liveness_enabled': 'false',
#             'facial_biometrics_enabled': 'false'
#         }
#     })

#     signer_response = httpx.post(
#         url=creation_signer_url,
#         data=signer_data,
#         headers=headers,
#         verify=False
#     )

#     with open(
#         './assinatura_digital_clicksign/signer_response.json',
#         'w', encoding='utf-8') as open_file:
#         json.dump(
#             signer_response.json(),
#             open_file,
#             ensure_ascii=False,
#             indent=4
#         )

#     signer_key = signer_response.json()['signer']['key']

#     return signer_key

# @app.post('/criar_contrato')
# def creation_contract() -> str:
    
#     creation_contract_url = f'{base_url}/templates/{template_id}/documents?access_token={access_token}'

#     contract_data = json.dumps({
#         'document': {
#             'path': '/CONTRATOS-TESTES/TIC_YYYYMMDDhhmmss_22233344455.pdf',
#             'template': {
#                 'data': {
#                     'idDiretorio': '1234567',
#                     'nome': 'TIC_YYYYMMDD_CPFgestorQueConvidou',
#                     'descricao': 'Termo de inclusão',
#                     'dataValidade': '',
#                     'extensao': 'pdf',
#                     'tipoArquivo': 293
#           }
#         }
#       }
#     })

#     contract_response = httpx.post(
#         url=creation_contract_url,
#         data=contract_data,
#         headers=headers,
#         verify=False
#     )

#     with open(
#         './assinatura_digital_clicksign/contract_response.json',
#         'w', encoding='utf-8') as open_file:
#         json.dump(
#             contract_response.json(),
#             open_file,
#             ensure_ascii=False,
#             indent=4
#         )

#     contract_key = contract_response.json()['document']['key']

#     return contract_key

# @app.post('/relacionar_contrato')
# def creation_contract(signer_key: str = Depends(creation_signer), contract_key: str = Depends(creation_contract)):
    
#     relate_contract_url = f'{base_url}/lists?access_token={access_token}'

#     relate_contract_data = json.dumps({
#         'list': {
#             'document_key': contract_key,
#             'signer_key': signer_key,
#             'sign_as': 'administrator',
#             'refusable': 'true'
#         }
#     })

#     relate_contract_response = httpx.post(
#         url=relate_contract_url,
#         data=relate_contract_data,
#         headers=headers,
#         verify=False
#     )

#     with open(
#         './assinatura_digital_clicksign/relate_contract_response.json',
#         'w', encoding='utf-8') as open_file:
#         json.dump(
#             relate_contract_response.json(),
#             open_file,
#             ensure_ascii=False,
#             indent=4
#         )

#     relate_contract_url = relate_contract_response.json()['list']['url']

#     return relate_contract_url
