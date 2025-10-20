import os
import random
import qrcode
import openai
from django.conf import settings
from django.utils import timezone
import time
import uuid
import httpx
from pathlib import Path

# Configuração da OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

def generate_qr_code(session_id):
    """
    Gera um QR code para autenticação do WhatsApp
    Na implementação real, isso seria integrado com a API do WhatsApp
    """
    # Criar diretório para QR codes se não existir
    qr_dir = Path(settings.MEDIA_ROOT) / 'qrcodes'
    qr_dir.mkdir(exist_ok=True, parents=True)
    
    # Gerar um QR code de exemplo (em produção, seria gerado pela API do WhatsApp)
    qr_data = f"whatsapp-session-{session_id}-{uuid.uuid4()}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Salvar o QR code
    qr_path = f"qrcodes/qr_{session_id}.png"
    full_path = Path(settings.MEDIA_ROOT) / qr_path
    img.save(full_path)
    
    return qr_path

def validate_whatsapp_number(phone_number):
    """
    Valida se um número existe no WhatsApp
    Na implementação real, isso seria integrado com a API do WhatsApp
    """
    # Simulação de validação (em produção, seria validado pela API do WhatsApp)
    # Retorna True para 90% dos números para simular números válidos
    return random.random() < 0.9

def modify_message_with_ai(original_message):
    """
    Usa a API da OpenAI para fazer pequenas modificações na mensagem
    mantendo o sentido original
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que faz pequenas modificações em mensagens para evitar detecção de spam, mantendo o sentido original. Altere apenas a estrutura, ordem das palavras ou sinônimos, sem mudar o significado."},
                {"role": "user", "content": f"Modifique esta mensagem mantendo o sentido original: {original_message}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Em caso de erro, retorna a mensagem original
        print(f"Erro ao modificar mensagem com IA: {e}")
        return original_message

def random_delay():
    """
    Gera um atraso aleatório entre 240 e 360 segundos
    """
    return random.randint(240, 360)