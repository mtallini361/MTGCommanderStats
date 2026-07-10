import re
from game_mechanics import Partner
    

class CardTextParser:
    _PARTNER =  re.compile(r"Partner(?:\s*-\s*([^\(\)\n]+))?")
    _PARTNER_WITH = re.compile(r"Partner with ([^\n]+)")
    
    def __init__(self, card_text: str):
        self.card_text = card_text
        
    def get_partner_type(self) -> str | None:
        match = self._PARTNER.search(self.card_text)
        if not match:
            return None
        return match.group(1) if match.group(1) else "Partner"
    
    def get_partner_with(self) -> str | None:
        match = self._PARTNER_WITH.search(self.card_text)
        if not match:
            return None
        return match.group(1)