import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from parse_text import CardTextParser


class TestGetPartnerType:
    def test_no_partner_returns_none(self):
        parser = CardTextParser("Flying\nTrample")
        assert parser.get_partner_type() is None

    def test_generic_partner_returns_partner(self):
        parser = CardTextParser("Partner\nYou may have two commanders.")
        assert parser.get_partner_type() == "Partner"

    def test_partner_dash_extracts_text(self):
        parser = CardTextParser("Partner - Friends Forever\nSome other text")
        assert parser.get_partner_type() == "Friends Forever"

    def test_partner_with_returns_partner(self):
        # "Partner with" has no dash, so get_partner_type returns generic "Partner"
        parser = CardTextParser("Partner with Okaun, Eye of Chaos")
        assert parser.get_partner_type() == "Partner"

    def test_partner_in_multiline_text(self):
        parser = CardTextParser("Flying\nVigilance\nPartner\nYou may have two commanders.")
        assert parser.get_partner_type() == "Partner"

    def test_partner_dash_stops_at_parenthesis(self):
        parser = CardTextParser("Partner - Ability (some reminder text)")
        assert parser.get_partner_type() == "Ability "


class TestGetPartnerWith:
    def test_no_partner_with_returns_none(self):
        parser = CardTextParser("Flying\nTrample")
        assert parser.get_partner_with() is None

    def test_generic_partner_returns_none(self):
        parser = CardTextParser("Partner\nYou may have two commanders.")
        assert parser.get_partner_with() is None

    def test_partner_with_extracts_name(self):
        parser = CardTextParser("Partner with Okaun Eye of Chaos")
        assert parser.get_partner_with() == "Okaun Eye of Chaos"

    def test_partner_with_in_multiline_text(self):
        parser = CardTextParser("Flying\nPartner with Falco Spara Pactweaver\nVigilance")
        assert parser.get_partner_with() == "Falco Spara Pactweaver"
