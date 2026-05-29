from pathlib import Path
import xml.etree.ElementTree as ET
from config import CONFIG
from core.dataclasses import LocalisationRow

LANGUAGE_DIR: Path = CONFIG["lang_dir"]

def parse_localisations() -> list[LocalisationRow]:
    """
    Парсит ВСЕ .mxml файлы локализаций из папки temp/language.
    Каждый файл — это скомпилированный MBIN с текстовыми строками.
    Возвращает плоский список LocalisationRow.
    """
    if not LANGUAGE_DIR.exists():
        raise FileNotFoundError(f"Папка language не найдена: {LANGUAGE_DIR}")

    result: list[LocalisationRow] = []

    # Обрабатываем файлы в алфавитном порядке для стабильности
    for file_path in sorted(LANGUAGE_DIR.glob("*.mxml")):
        # Из имени файла вида NMS_LOC1_RUSSIAN.mxml вытаскиваем LOC1
        loc_name = file_path.stem.split("_")[1]

        tree = ET.parse(file_path)
        root = tree.getroot()

        # В каждом файле ищем все TkLocalisationEntry — это и есть строки локализации
        for entry in root.findall(".//Property[@value='TkLocalisationEntry']"):
            # ID строки (например, DNT_ATLAS_STATION)
            text_id = entry.find("./Property[@name='Id']").attrib["value"]
            # Сама строка на русском
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