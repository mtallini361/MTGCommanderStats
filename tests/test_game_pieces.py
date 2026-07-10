import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from pydantic import ValidationError
from game_pieces import CommanderCard, DeckCommander


def make_commander(name="Test Commander", card_text="", subtype=None, card_type="Creature", **kwargs):
    return CommanderCard(
        name=name,
        mana_cost="{3}{G}",
        mana_value=4,
        color="G",
        supertype="Legendary",
        card_type=card_type,
        subtype=subtype,
        card_text=card_text,
        **kwargs,
    )


def make_deck_commander(cards):
    return DeckCommander(cards=cards)


class TestDeckCommanderSingleCommander:
    def test_single_commander_is_valid(self):
        make_deck_commander([make_commander()])


class TestDeckCommanderGenericPartner:
    def test_two_generic_partners_is_valid(self):
        card1 = make_commander(name="Ishai, Ojutai Dragonspeaker", card_text="Partner\nYou may have two commanders.")
        card2 = make_commander(name="Reyhan, Last of the Abzan", card_text="Partner\nYou may have two commanders.")
        make_deck_commander([card1, card2])

    def test_mismatched_partner_types_raises(self):
        card1 = make_commander(name="Ishai, Ojutai Dragonspeaker", card_text="Partner\nYou may have two commanders.")
        card2 = make_commander(name="Bjorna, Nightfall Alchemist", card_text="Partner - Friends Forever\nYou may have two commanders.")
        with pytest.raises(ValidationError, match="same partner type"):
            make_deck_commander([card1, card2])


class TestDeckCommanderPartnerWith:
    def test_correct_partner_with_pair_is_valid(self):
        card1 = make_commander(name="Okaun, Eye of Chaos", card_text="Partner with Zndrsplt, Eye of Wisdom")
        card2 = make_commander(name="Zndrsplt, Eye of Wisdom", card_text="Partner with Okaun, Eye of Chaos")
        make_deck_commander([card1, card2])

    def test_partner_with_wrong_card_raises(self):
        card1 = make_commander(name="Okaun, Eye of Chaos", card_text="Partner with Zndrsplt, Eye of Wisdom")
        card2 = make_commander(name="Ishai, Ojutai Dragonspeaker", card_text="Partner")
        with pytest.raises(ValidationError, match="reference each other"):
            make_deck_commander([card1, card2])

    def test_one_sided_partner_with_raises(self):
        card1 = make_commander(name="Okaun, Eye of Chaos", card_text="Partner with Zndrsplt, Eye of Wisdom")
        card2 = make_commander(name="Bebop, Skull & Crossbones", card_text="Partner with Rocksteady, Mutant Marauder")
        with pytest.raises(ValidationError, match="reference each other"):
            make_deck_commander([card1, card2])


class TestDeckCommanderChooseBackground:
    def test_choose_background_with_background_card_is_valid(self):
        card1 = make_commander(name="Erinis, Gloom Stalker", card_text="Choose a Background")
        card2 = make_commander(
            name="Folk Hero",
            card_text="Background\n(You may have two commanders.)",
            card_type="Enchantment",
            subtype="Background",
        )
        make_deck_commander([card1, card2])

    def test_choose_background_without_background_raises(self):
        card1 = make_commander(name="Erinis, Gloom Stalker", card_text="Choose a Background")
        card2 = make_commander(name="Atraxa, Praetors Voice", card_text="", subtype="Angel Horror")
        with pytest.raises(ValidationError, match="Background"):
            make_deck_commander([card1, card2])


class TestDeckCommanderDoctorCompanion:
    def test_doctor_companion_with_time_lord_doctor_is_valid(self):
        card1 = make_commander(
            name="The Tenth Doctor",
            card_text="Legendary",
            subtype="Time Lord Doctor",
        )
        card2 = make_commander(name="Rose Tyler", card_text="Doctor's Companion\n(You can have two commanders.)")
        make_deck_commander([card1, card2])

    def test_doctor_companion_without_time_lord_doctor_raises(self):
        card1 = make_commander(name="Rose Tyler", card_text="Doctor's Companion\n(You can have two commanders.)")
        card2 = make_commander(name="Atraxa, Praetors Voice", card_text="", subtype="Angel Horror")
        with pytest.raises(ValidationError, match="Time Lord Doctor"):
            make_deck_commander([card1, card2])
