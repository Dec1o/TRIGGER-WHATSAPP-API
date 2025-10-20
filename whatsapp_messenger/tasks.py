import time
import random
from celery import shared_task
from django.utils import timezone
from .models import MessageDispatch
from .utils import validate_whatsapp_number, random_delay

@shared_task
def process_message_dispatch(dispatch_id):
    """
    Processa o envio de uma mensagem de forma assíncrona
    """
    try:
        # Buscar o registro de disparo
        dispatch = MessageDispatch.objects.get(id=dispatch_id)
        
        # Atualizar status para processando
        dispatch.status = 'processing'
        dispatch.save()
        
        # Validar se o número existe no WhatsApp
        is_valid = validate_whatsapp_number(dispatch.phone_number)
        if not is_valid:
            dispatch.status = 'invalid_number'
            dispatch.save()
            return f"Número inválido: {dispatch.phone_number}"
        
        # Aplicar atraso aleatório para evitar bloqueios (entre 240s e 360s)
        delay_seconds = random_delay()
        time.sleep(delay_seconds)
        
        # Simular envio da mensagem (em produção, seria integrado com a API do WhatsApp)
        # Aqui você integraria com a API não oficial do WhatsApp
        
        # Atualizar status para enviado
        dispatch.status = 'sent'
        dispatch.sent_time = timezone.now()
        dispatch.save()
        
        return f"Mensagem enviada com sucesso para {dispatch.phone_number}"
    
    except MessageDispatch.DoesNotExist:
        return f"Disparo não encontrado: {dispatch_id}"
    
    except Exception as e:
        # Em caso de erro, atualizar status para falha
        try:
            dispatch = MessageDispatch.objects.get(id=dispatch_id)
            dispatch.status = 'failed'
            dispatch.save()
        except:
            pass
        
        return f"Erro ao processar mensagem: {str(e)}"