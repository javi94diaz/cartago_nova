

class EventCard:
    def __init__(self, card_id, title, effect):
        self.id = card_id
        self.title = title
        self.effect = effect

    def __repr__(self):
        return f"<EventCard {self.title}>"
    
    def apply_effect(self):
        pass
        