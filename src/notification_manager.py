class NotificationManager:
    def __init__(self):
        self.notifications = []
        
    def add_notification(self, notification: str):
        """Adiciona uma notificação à lista."""
        
        # Insere a nova notificação no início da lista
        self.notifications.insert(0, notification)
        
    def notify_turn(self):
        """Notifica o jogador de que é a sua vez."""
        
        self.notifications.insert(0, "É seu turno!")
        
    def remove_turn_notification(self):
        """Remove a notificação de que é a vez do jogador."""
        
        try:
            self.notifications.remove("É seu turno!")
        except ValueError:
            pass