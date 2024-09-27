class NotificationManager:
    def __init__(self):
        self.notifications = []
        
    def add_notification(self, notification: str):
        """Adiciona uma notificação à lista."""
        
        # A interface suporta fisicamente até 10 notificações, então se passar disso, remove a última
        if len(self.notifications) == 10: 
            self.notifications.pop(-1)
            
        # Insere a nova notificação no início da lista
        self.notifications.insert(0, notification)