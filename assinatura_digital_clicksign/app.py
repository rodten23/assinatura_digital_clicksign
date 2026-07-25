import json
import os

from pathlib import Path

from datetime import date

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

    return ler_envelope()


def ler_envelope():
    with open(
        './assinatura_digital_clicksign/resposta_envelope.json',
        'r',encoding='utf-8') as open_file:
            dados_envelope = json.load(open_file)
    
    chave_envelope = dados_envelope['data']['id']
    
    return chave_envelope



@app.post('/criar_signatario')
def criar_signatario(envelope=Path('./assinatura_digital_clicksign/resposta_envelope.json')) -> str:

    chave_envelope = ''

    if envelope.is_file():
        chave_envelope = ler_envelope()
        
    else:
        chave_envelope = criar_envelope()
        
    
    criar_signatario_url = f'{base_url}/envelopes/{chave_envelope}/signers'

    body_signatario = json.dumps({
        'data': {
            'type': 'signers',
            'attributes': {
                'name': 'Testador Que Assina',
                'email': 'rodten23@gmail.com',
                'birthday': '2000-01-01',
                'phone_number': '11988776655',
                'has_documentation': True,
                'documentation': '123.480.920-69',
                'refusable': True,
                'group': 1,
                'location_required_enabled': False,
                'communicate_events': {
                    'signature_request': 'email',
                    'signature_reminder': 'email',
                    'document_signed': 'email'                   
                }
            }
        }
    })

    #         'auths': [
    #             'sms'
    #         ],
            
    #         'documentation': '123.480.920-69',
    #         'communicate_by': 'email',
            
    #         'selfie_enabled': 'false',
    #         'handwritten_enabled': 'false',
    #         
    #         'official_document_enabled': 'false',
    #         'liveness_enabled': 'false',
    #         'facial_biometrics_enabled': 'false'
    #     }
    # })

    resposta_signatario = httpx.post(
        url=criar_signatario_url,
        data=body_signatario,
        headers=headers,
        verify=False
    )

    with open(
        './assinatura_digital_clicksign/resposta_signatario.json',
        'w', encoding='utf-8') as response_file:
        json.dump(
            resposta_signatario.json(),
            response_file,
            ensure_ascii=False,
            indent=4
        )

    return ler_signatario()

def ler_signatario():
    with open(
        './assinatura_digital_clicksign/resposta_signatario.json',
        'r',encoding='utf-8') as open_file:
            dados_signatario = json.load(open_file)
        
    chave_signatario = dados_signatario['data']['id']
    nome_signatario = dados_signatario['data']['attributes']['name']
    documento_signatario = dados_signatario['data']['attributes']['documentation']
        
    return {'chave': chave_signatario, 'nome': nome_signatario, 'documento': documento_signatario}


@app.post('/criar_documento')
def criar_documento(
    envelope=Path('./assinatura_digital_clicksign/resposta_envelope.json'),signatario=Path('./assinatura_digital_clicksign/resposta_signatario.json')) -> str:

    chave_envelope = ''
    nome_signatario = ''
    documento_signatario = ''

    if envelope.is_file():
        chave_envelope = ler_envelope()
        
    else:
        chave_envelope = criar_envelope()


    if signatario.is_file():
        nome_signatario = ler_signatario()['nome']
        documento_signatario = ler_signatario()['documento']
        
    else:
        nome_signatario = criar_signatario()['nome']
        documento_signatario = criar_signatario()['documento']
    
    
    criar_documento_url = f'{base_url}/envelopes/{chave_envelope}/documents'

    data_atual = date.today()

    meses = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho','Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    body_documento = json.dumps({
        'data': {
            'type': 'documents',
            'attributes': {
                'filename': 'Contrato_Teste.docx',
                'template': {
                    'key': template_id,
                    'data': {
                        'enterprise': "Empresa Teste Ltda",
                        'signer_name': nome_signatario,
                        'signer_document': documento_signatario,
                        'created_day_contract': data_atual.day,
                        'created_month_contract': meses[data_atual.month],
                        'created_year_contract': data_atual.year
                    },
                    'metadata': {}
                }
            }
        }
    })

    resposta_documento = httpx.post(
        url=criar_documento_url,
        data=body_documento,
        headers=headers,
        verify=False
    )

    with open(
        './assinatura_digital_clicksign/resposta_documento.json',
        'w', encoding='utf-8') as response_file:
        json.dump(
            resposta_documento.json(),
            response_file,
            ensure_ascii=False,
            indent=4
        )

    return ler_documento()


def ler_documento():
    with open(
        './assinatura_digital_clicksign/resposta_documento.json',
        'r',encoding='utf-8') as open_file:
            dados_documento = json.load(open_file)
        
    chave_documento = dados_documento['data']['id']
        
    return chave_documento


@app.post('/qualificar_signatario_documento')
def qualificar_sig_doc(
    envelope=Path('./assinatura_digital_clicksign/resposta_envelope.json'),
    documento=Path('./assinatura_digital_clicksign/resposta_documento.json'),
    signatario=Path('./assinatura_digital_clicksign/resposta_signatario.json')) -> str:
    

    chave_envelope = ''
    chave_documento = ''
    chave_signatario = ''
    
    if envelope.is_file():
        chave_envelope = ler_envelope()      
    else:
        chave_envelope = criar_envelope()

    if documento.is_file():
        chave_documento = ler_documento()                
    else:
        chave_documento = criar_documento()    
    
    if signatario.is_file():
        chave_signatario = ler_signatario()['chave']            
    else:
        chave_signatario = criar_signatario()['chave']

    
    qualificar_sig_doc_url = f'{base_url}/envelopes/{chave_envelope}/requirements'

    body_qualificacao = json.dumps({
        'data': {
            'type': 'requirements',
            'attributes': {
                "action": "agree",
                "role": "sign"
            },
            'relationships': {
                'document': {
                    'data': {
                        'type': 'documents',
                        'id': chave_documento
                    }
                },
                'signer': {
                    'data': {
                        'type': 'signers',
                        'id': chave_signatario
                    }
                }
            }
        }
    })

    resposta_qualificar_sig_doc = httpx.post(
        url=qualificar_sig_doc_url,
        data=body_qualificacao,
        headers=headers,
        verify=False
    )

    with open(
        './assinatura_digital_clicksign/resposta_qualificar_sig_doc.json',
        'w', encoding='utf-8') as response_file:
        json.dump(
            resposta_qualificar_sig_doc.json(),
            response_file,
            ensure_ascii=False,
            indent=4
        )

    return ler_qualificacao()


def ler_qualificacao():
    with open(
        './assinatura_digital_clicksign/resposta_qualificar_sig_doc.json',
        'r',encoding='utf-8') as open_file:
            dados_qualificacao = json.load(open_file)
        
    chave_qualificacao = dados_qualificacao['data']['id']
        
    return chave_qualificacao
