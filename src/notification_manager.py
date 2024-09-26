class NotificationManager:
    def __init__(self):
        self.notifications = []
        
    def add_notification(self, notification):
        if len(self.notifications) == 10:
            self.notifications.pop(-1)
            
        self.notifications.insert(0, notification)