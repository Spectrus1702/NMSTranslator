# core/parsers/loc_parser.py

from pathlib import Path
import xml.etree.ElementTree as ET
from config import CONFIG
from core.models.localisation import LocalisationRow

LANGUAGE_DIR: Path = CONFIG["lang_dir"]

def parse_localisations() -> list[LocalisationRow]:
    """
    Парсит все .mxml файлы локализаций и возвращает плоский список записей.
    """
    if not LANGUAGE_DIR.exists():
        raise FileNotFoundError(f"Папка language не найдена: {LANGUAGE_DIR}")
    result: list[LocalisationRow] = []
    for file_path in sorted(LANGUAGE_DIR.glob("*.mxml")):
        loc_name = file_path.stem.split("_")[1]
        tree = ET.parse(file_path)
        root = tree.getroot()
        for entry in root.findall(".//Property[@value='TkLocalisationEntry']"):
            text_id = entry.find("./Property[@name='Id']").attrib["value"]
            text = entry.find("./Property[@name='Russian']").attrib["value"]
            result.append(
                LocalisationRow(
                    loc_name=loc_name,
                    text_id=text_id,
                    text=text,
                )
            )
    print(f"✓ Загружено: {len(result)} строк локализации")
    return result