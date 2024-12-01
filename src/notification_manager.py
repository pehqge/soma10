class NotificationManager:
    def __init__(self):
        self.notifications = []
        
    def add_notification(self, notification: str):
        """Adiciona uma notificação à lista."""
        # Insere a nova notificação no início da lista
        self.notifications.insert(0, notification)
        
    def reset(self):
        """Reseta as notificações."""
        
        self.notifications = []