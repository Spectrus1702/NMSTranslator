from dataclasses import dataclass, field

@dataclass
class LocalisationRow:
    loc_name : str
    text_id : str
    text : str