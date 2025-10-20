from django.db import models
import uuid
from django.utils import timezone

class WhatsAppSession(models.Model):
    """Modelo para armazenar sessões do WhatsApp"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    qr_code_path = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.session_name} - {'Ativo' if self.is_active else 'Inativo'}"

class MessageTemplate(models.Model):
    """Modelo para armazenar templates de mensagens"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MessageDispatch(models.Model):
    """Modelo para armazenar disparos de mensagens"""
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('sent', 'Enviado'),
        ('failed', 'Falhou'),
        ('invalid_number', 'Número Inválido'),
    )
    
    MEDIA_TYPE_CHOICES = (
        ('none', 'Sem Mídia'),
        ('image', 'Imagem'),
        ('audio', 'Áudio'),
        ('video', 'Vídeo'),
        ('document', 'Documento'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(WhatsAppSession, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    original_message = models.TextField()
    modified_message = models.TextField(null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='none')
    media_url = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    scheduled_time = models.DateTimeField(default=timezone.now)
    sent_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.status}"
