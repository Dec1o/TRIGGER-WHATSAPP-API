from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import WhatsAppSession, MessageDispatch
from .serializers import (
    WhatsAppSessionSerializer, 
    MessageDispatchSerializer,
    BulkMessageDispatchSerializer
)
from .utils import generate_qr_code, validate_whatsapp_number, modify_message_with_ai

class WhatsAppSessionViewSet(viewsets.ModelViewSet):
    queryset = WhatsAppSession.objects.all()
    serializer_class = WhatsAppSessionSerializer
    
    @action(detail=False, methods=['post'])
    def create_session(self, request):
        """Cria uma nova sessão do WhatsApp e gera um QR code"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()
        
        # Gerar QR code
        qr_path = generate_qr_code(session.id)
        session.qr_code_path = qr_path
        session.save()
        
        return Response({
            'session_id': session.id,
            'qr_code_url': f"{settings.MEDIA_URL}{qr_path}",
            'message': 'Escaneie o QR code para autenticar o WhatsApp'
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def activate_session(self, request, pk=None):
        """Ativa uma sessão após o QR code ser escaneado"""
        session = self.get_object()
        session.is_active = True
        session.save()
        
        return Response({
            'message': 'Sessão ativada com sucesso',
            'session_id': session.id
        }, status=status.HTTP_200_OK)

class MessageDispatchViewSet(viewsets.ModelViewSet):
    queryset = MessageDispatch.objects.all()
    serializer_class = MessageDispatchSerializer
    
    @action(detail=False, methods=['post'])
    def send_messages(self, request):
        """Envia mensagens para múltiplos números"""
        serializer = BulkMessageDispatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        session_id = serializer.validated_data['session_id']
        phone_numbers = serializer.validated_data['phone_numbers']
        message = serializer.validated_data['message']
        media_type = serializer.validated_data['media_type']
        media_url = serializer.validated_data.get('media_url', '')
        
        # Verificar se a sessão existe e está ativa
        session = get_object_or_404(WhatsAppSession, id=session_id)
        if not session.is_active:
            return Response({
                'error': 'A sessão não está ativa. Escaneie o QR code primeiro.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Criar registros de disparo para cada número
        dispatches = []
        for phone_number in phone_numbers:
            # Modificar a mensagem com IA
            modified_message = modify_message_with_ai(message)
            
            # Criar o registro de disparo
            dispatch = MessageDispatch.objects.create(
                session=session,
                phone_number=phone_number,
                original_message=message,
                modified_message=modified_message,
                media_type=media_type,
                media_url=media_url,
                status='pending'
            )
            dispatches.append(dispatch)
            
            # Iniciar o processamento assíncrono (será implementado nas tarefas)
            # process_message_dispatch.delay(str(dispatch.id))
        
        return Response({
            'message': f'{len(dispatches)} mensagens enfileiradas para envio',
            'dispatch_ids': [str(d.id) for d in dispatches]
        }, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=True, methods=['get'])
    def check_status(self, request, pk=None):
        """Verifica o status de um disparo de mensagem"""
        dispatch = self.get_object()
        return Response({
            'id': dispatch.id,
            'phone_number': dispatch.phone_number,
            'status': dispatch.status,
            'scheduled_time': dispatch.scheduled_time,
            'sent_time': dispatch.sent_time
        }, status=status.HTTP_200_OK)
