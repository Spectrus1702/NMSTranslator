from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ====================== Пути ======================
CONFIG = {
    "base_dir": BASE_DIR,
    "data_file": BASE_DIR / "data" / "files.json",
    "translations_dir": BASE_DIR / "data" / "translations",
    "translations_file": BASE_DIR / "data" / "translations" / "user_translations.json",
    "pak_dir": Path(r"C:\Program Files (x86)\Steam\steamapps\common\No Man's Sky\GAMEDATA\PCBANKS"),
    "temp_dir": BASE_DIR / "temp",
    "compiler": BASE_DIR / "tools" / "MBINCompiler.exe",
    "cache_file": BASE_DIR / "temp" / "cache" / "loc_entries.json",
    "lang_dir": BASE_DIR / "temp" / "language",
    "metadata_dir": BASE_DIR / "temp" / "metadata",
}

# ====================== Диалоги ======================

RACE_MAP = {
    "ATLAS": "Atlas",
    "BUI": "Autophag",
    "EXP": "Korvax",
    "TRA": "Gek",
    "WAR": "Vaikin",
    "ALL": "Any",
    "EXPED": "Any",
    "EXPED18": "Any",
    "GUILD": "Any",
    "PIRATES": "Any",
    "PIRATES1": "Any",
    "SENT": "Any",
    "SHOP": "Any",
}

# ====================== Цвета ======================
RACE_COLORS = {
    "Atlas":    {"bg": "#cc4125", "fg": "#e6b8af"},
    "Autophag": {"bg": "#674ea7", "fg": "#d9d2e9"},
    "Korvax":   {"bg": "#3c78d8", "fg": "#c9daf8"},
    "Gek":      {"bg": "#6aa84f", "fg": "#d9ead3"},
    "Vaikin":   {"bg": "#e06666", "fg": "#f4cccc"},
    "Any":      {"bg": "#666666", "fg": "#efefef"},
}

TRANSLATION_STATUS_COLORS = {
    "untranslated": {"bg": "#f4cccc", "fg": "#660000"},
    "translated":   {"bg": "#d9ead3", "fg": "#274e13"},
    "in_progress":  {"bg": "#fff2cc", "fg": "#7f6000"},
}