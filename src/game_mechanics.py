from pydantic import BaseModel

class Partner(BaseModel):
    partner_type: str | None = None
    partner_with: str | None = None
    choose_background: bool = False
    doctor_companion: bool = False
    