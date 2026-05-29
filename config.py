from pathlib import Path

# Корень всего проекта — папка, где лежит этот файл
BASE_DIR = Path(__file__).resolve().parent

CONFIG = {
    # Абсолютные пути ко всем важным директориям
    "base_dir": BASE_DIR,
    "data_file": BASE_DIR / "data" / "files.json",                    # Список MBIN-файлов для извлечения
    "translations_dir": BASE_DIR / "data" / "translations",           # Папка с пользовательскими переводами
    "translations_file": BASE_DIR / "data" / "translations" / "user_translations.json",  # JSON с переводами
    "pak_dir": Path(r"C:\Program Files (x86)\Steam\steamapps\common\No Man's Sky\GAMEDATA\PCBANKS"),  # Папка с PAK-архивами игры
    "temp_dir": BASE_DIR / "temp",                                    # Временная папка для распакованных файлов
    "compiler": BASE_DIR / "tools" / "MBINCompiler.exe",              # Путь до MBINCompiler
    "cache_file": BASE_DIR / "temp" / "cache" / "loc_entries.json",   # Кеш распарсенных локализаций
    "lang_dir": BASE_DIR / "temp" / "language",                       # Сюда распаковываются файлы локализации
    "metadata_dir": BASE_DIR / "temp" / "metadata",                   # Сюда распаковываются метаданные (диалоги)
}

# Маппинг внутренних кодов рас на человекочитаемые названия
# BUI = Autophag (роботы-автофаги из экспедиции), EXP = Korvax, TRA = Gek, WAR = Vaikin
RACE_MAP = {
    "ATLAS": "Atlas",
    "BUI": "Autophag",
    "EXP": "Korvax",
    "TRA": "Gek",
    "WAR": "Vaikin",
    "ALL": "Any",
    "GUILD": "Any",
    "PIRATES": "Any",
    "PIRATES1": "Any",
    "SENT": "Any",
    "SHOP": "Any",
}

# Цветовая схема для визуального оформления рас (bg — фон, fg — текст)
RACE_COLORS = {
    "Atlas":    {"bg": "#cc4125", "fg": "#e6b8af"},
    "Autophag": {"bg": "#674ea7", "fg": "#d9d2e9"},
    "Korvax":   {"bg": "#3c78d8", "fg": "#c9daf8"},
    "Gek":      {"bg": "#6aa84f", "fg": "#d9ead3"},
    "Vaikin":   {"bg": "#e06666", "fg": "#f4cccc"},
    "Any":      {"bg": "#666666", "fg": "#efefef"},
}

# Цвета для статуса перевода (untranslated — красный, translated — зелёный, in_progress — жёлтый)
TRANSLATION_STATUS_COLORS = {
    "untranslated": {"bg": "#f4cccc", "fg": "#660000"},
    "translated":   {"bg": "#d9ead3", "fg": "#274e13"},
    "in_progress":  {"bg": "#fff2cc", "fg": "#7f6000"},
}