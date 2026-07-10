import re
from parse_text import CardTextParser
from pydantic import BaseModel, model_validator

class Card(BaseModel):
    _id: str
    name: str
    mana_cost: str
    mana_value: int
    color: str
    supertype: str | None
    card_type: str
    subtype: str | None
    card_text: str

    
class _CommanderCard(Card):
    
    @model_validator(mode="after")
    def check_legendary(self):
        if self.supertype != "Legendary":
            raise ValueError("CommanderCard must have supertype 'Legendary'")
        return self
    
    @model_validator(mode="after")
    def check_type(self):
        if self.card_type == "Creature":
            return self
        if self.card_type == "Planeswalker" and "can be your commander" in self.card_text:
            return self
        if self.card_type == "Artifact" and self.subtype in ["Vehicle", "Spacecraft"]:
            return self
        if self.card_type == "Enchantment" and self.subtype == "Background":
            return self
        
        raise ValueError("CommanderCard must be 'Creature', valid 'Planeswalker', Vehicle/Spacecraft Artifact, or Background Enchantment")


class CommanderCard(_CommanderCard):
    partner_type: str | None = None
    partner_with: str | None = None
    choose_background: bool = False
    doctor_companion: bool = False

    @model_validator(mode="after")
    def set_partner_flags(self):
        parser = CardTextParser(self.card_text)
        self.partner_type = parser.get_partner_type()
        self.partner_with = parser.get_partner_with()
        self.choose_background = "Choose a Background" in self.card_text
        self.doctor_companion = "Doctor's Companion" in self.card_text
        return self
    

class DeckCommander(BaseModel):
    cards: list[CommanderCard]
    
    @model_validator(mode="after")
    def check_partner(self):
        if len(self.cards) == 2:
            card1, card2 = list(self.cards)
            if (card1.partner_type or card2.partner_type) and (card1.partner_type != card2.partner_type):
                raise ValueError("Partner commanders must have the same partner type")
            if (card1.partner_with or card2.partner_with) and ((card1.partner_with != card2.name) or (card2.partner_with != card1.name)):
                raise ValueError("Partner commanders must reference each other in their 'partner_with' field")
            if (card1.choose_background or card2.choose_background) and (card1.subtype != "Background" and card2.subtype != "Background"):
                raise ValueError("Choose a Background can only be used with a Background commander")
            if (card1.doctor_companion or card2.doctor_companion) and (card1.subtype != "Time Lord Doctor" and card2.subtype != "Time Lord Doctor"):
                raise ValueError("Doctor's Companion can only be used with a Time Lord Doctor commander")
        return self      


class Deck(BaseModel):
    _id: str
    commander: DeckCommander
    main_deck_count: int
    