# 🚀 API de Automação de WhatsApp com IA

Automatize o envio de mensagens via **WhatsApp** com recursos inteligentes de **IA (OpenAI)**, controle de sessões, intervalos aleatórios e envio assíncrono via **Celery + Redis**.  
Desenvolvida em **Django**, esta API é ideal para escalar comunicações com segurança e evitar bloqueios.

---

### Recursos Principais
- Autenticação via QR Code para sessões do WhatsApp  
- Modificação inteligente de mensagens (OpenAI)  
- Envio assíncrono com **Celery**  
- Intervalos aleatórios entre 240–360s  
- Validação automática de números  
- Integração opcional com APIs não oficiais do WhatsApp  

### Requisitos
- Python 3.11+  
- Redis em execução (`redis-server`)  
- Virtualenv ativo
