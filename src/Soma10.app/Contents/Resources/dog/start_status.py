class StartStatus:
    def __init__(self, code, message, players, local_id):
        super().__init__()
        self.local_id = local_id
        self.code = code
        self.message = message
        self.players = players

    def get_local_id(self):
        return self.local_id

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def get_players(self):
        return self.players
    
    def __str__(self):
        return f'local_id: {self.get_local_id()}\ncode: {self.get_code()}\nmessage: {self.get_message()}\nplayers: {self.get_players()}'
