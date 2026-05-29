from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class TextFlowEntry:
    """
    Одна реплика внутри AdvancedInteractionFlow.
    Появляется, когда диалог ветвится не через стандартные Options,
    а через кат-сцены или последовательный поток текста.
    """
    index: Optional[str] = None   # Порядковый номер в массиве GcPuzzleTextFlow
    title: Optional[str] = None   # Заголовок реплики (обычно пустой)
    text: Optional[str] = None    # Сам текст, который видит игрок
    mood: Optional[str] = None    # Эмоция/настроение NPC при произнесении


@dataclass
class OptionEntry:
    """
    Вариант ответа игрока в диалоге.
    Описывает кнопку, которую игрок нажимает, чтобы ответить NPC.
    """
    index: Optional[str] = None            # Порядковый номер в массиве Options
    name: Optional[str] = None             # Внутреннее имя опции (не показывается)
    text: Optional[str] = None             # Текст на кнопке ответа
    next_interaction: Optional[str] = None # ID следующего диалога (куда ведёт этот ответ)
    mood: Optional[str] = None             # Эмоция/настроение после выбора


@dataclass
class DialogEntry:
    """
    Одна запись диалога из GcAlienPuzzleEntry.
    Это может быть как простая реплика NPC, так и полноценный диалог с выбором.
    """
    id: str                                          # Уникальный идентификатор диалога (ключ)
    index: Optional[str] = None                      # Индекс в таблице диалогов
    text: Optional[str] = None                       # Текст, который говорит NPC (переведённый)
    text_alien: Optional[str] = None                 # Текст на языке пришельцев (до перевода)
    title: Optional[str] = None                      # Заголовок диалога (редко используется)
    additional_text: List[str] = field(default_factory=list)         # Дополнительный текст (может быть несколько элементов)
    additional_text_alien: List[str] = field(default_factory=list)   # Дополнительный текст на языке пришельцев
    mood: Optional[str] = None                       # Настроение NPC (влияет на анимацию)
    race: Optional[str] = None                       # Раса NPC (Gek/Korvax/Vaikin/Atlas/Autophag)
    progressive_dialogue: Optional[bool] = None      # True — диалог меняется в зависимости от прогресса игрока
    advanced_interaction_flow: List[TextFlowEntry] = field(default_factory=list)  # Сложные сцены/потоки текста
    options: List[OptionEntry] = field(default_factory=list)  # Варианты ответов игрока


@dataclass
class LocalisationRow:
    """
    Одна строка локализации из файлов NMS_LOC*_RUSSIAN.MBIN.
    Хранит текст, который показывается в интерфейсе и субтитрах.
    """
    loc_name: str   # Имя файла локализации (LOC1, LOC4, UPDATE3 и т.д.)
    text_id: str    # Уникальный ID строки (например, DNT_ATLAS_STATION)
    text: str       # Сам текст на русском