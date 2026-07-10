from datetime import datetime
from pydantic import BaseModel

from game_pieces import Card, Deck

class Player(BaseModel):
    _id: str
    name: str
    decks: list[Deck]
    
class PlayerState(BaseModel):
    player: Player
    current_deck: Deck
    turn_order: int
    current_turn: int = 0
    life_total: int = 40
    cards_in_hand: int = 0
    battlefield: list[Card] = []
    graveyard: list[Card] = []
    exile: list[Card] = []
    cards_in_library: int = 99
    commander_damage: dict[str, int] = {}
    
    def lose_game(self, defeated_by: Player | None, defeated_turn: int | None, defeat_reason: str | None):
        if defeated_by is None:
            defeated_by = Lose(loser=self, defeated_by=self, defeated_turn=defeated_turn, defeat_reason=defeat_reason)
        return Lose(loser=self, defeated_by=defeated_by, defeated_turn=defeated_turn, defeat_reason=defeat_reason)
    
    def win_game(self, win_reason: str | None, winning_turn: int | None):
        return Win(winner=self, win_reason=win_reason, winning_turn=winning_turn)


class Lose(BaseModel):
    loser: Player
    defeated_by: Player
    defeated_turn: int
    defeat_reason: str | None

    
class Win(BaseModel):
    winner: Player
    win_reason: str | None
    winning_turn: int


class GameState(BaseModel):
    _id: str
    date: str
    num_players: int
    variant: str
    players: list[PlayerState]
    current_turn: int
    
    def start_game(self, players: list[PlayerState], variant: str):
        self.date = str(datetime.now().date())
        self.players = players
        self.num_players = len(players)
        self.variant = variant
        self.current_turn = 0
    
    
