import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, List

from config import CONFIG
from core.dataclasses import TextFlowEntry, OptionEntry, DialogEntry


class DialogParser:
    """
    Парсер диалогов из скомпилированных MBIN → MXML файлов.
    Извлекает GcAlienPuzzleEntry — записи диалогов с NPC.
    """

    def __init__(self) -> None:
        self.metadata_dir = Path(CONFIG["metadata_dir"])

    def _get_text(self, element: Optional[ET.Element]) -> Optional[str]:
        """
        Извлекает значение атрибута 'value' у XML-элемента.
        Если элемент не найден (None) — возвращает None, а не падает.
        """
        if element is None:
            return None
        return element.get("value")

    def _get_complex_value(self, element: Optional[ET.Element], sub_name: str) -> Optional[str]:
        """
        Для составных типов вроде Mood и Race.
        В XML они выглядят как:
            <Property name="Mood">
                <Property name="Mood" value="Friendly" />
            </Property>
        Эта функция заходит в родительский Property и ищет дочерний с именем sub_name.
        """
        if element is None:
            return None
        for child in element:
            if child.get("name") == sub_name:
                return child.get("value")
        return None

    def _get_list_values(self, element: Optional[ET.Element], tag_name: str) -> List[str]:
        """
        Для составных типов, которые являются списками строк (List<NMSString0x20A>).
        В XML они выглядят как:
            <Property name="AdditionalText">
                <Property name="AdditionalText" value="Текст 1" _index="0" />
                <Property name="AdditionalText" value="Текст 2" _index="1" />
            </Property>
        Эта функция собирает ВСЕ значения из дочерних Property с именем tag_name.
        """
        values = []
        if element is None:
            return values
        for item in element.findall(f".//Property[@name='{tag_name}']"):
            val = item.get("value")
            if val is not None:  # value может быть пустой строкой, поэтому проверяем на None
                values.append(val)
        return values

    def _parse_text_flow(self, element: ET.Element) -> Optional[TextFlowEntry]:
        """
        Парсит один GcPuzzleTextFlow — реплику внутри AdvancedInteractionFlow.
        Это текстовый блок, который показывается последовательно в рамках одной сцены.
        """
        return TextFlowEntry(
            index=element.get("_index"),
            title=self._get_text(element.find(".//Property[@name='Title']")),
            text=self._get_text(element.find(".//Property[@name='Text']")),
            mood=self._get_complex_value(element.find(".//Property[@name='Mood']"), "Mood"),
        )

    def _parse_option(self, element: ET.Element) -> Optional[OptionEntry]:
        """
        Парсит один GcAlienPuzzleOption — вариант ответа игрока.
        Это кнопка с текстом, которая ведёт к следующему диалогу.
        """
        return OptionEntry(
            index=element.get("_index"),
            name=self._get_text(element.find(".//Property[@name='Name']")),
            text=self._get_text(element.find(".//Property[@name='Text']")),
            next_interaction=self._get_text(element.find(".//Property[@name='NextInteraction']")),
            mood=self._get_complex_value(element.find(".//Property[@name='Mood']"), "Mood"),
        )

    def _parse_dialog_entry(self, element: ET.Element) -> Optional[DialogEntry]:
        """
        Парсит ОДИН GcAlienPuzzleEntry в DialogEntry.
        Собирает все поля: текст, расу, настроение, варианты ответов,
        дополнительные тексты и флаги.
        """
        dialog = DialogEntry(
            id=self._get_text(element.find(".//Property[@name='Id']")) or "",
            index=element.get("_index"),
            text=self._get_text(element.find(".//Property[@name='Text']")),
            text_alien=self._get_text(element.find(".//Property[@name='TextAlien']")),
            title=self._get_text(element.find(".//Property[@name='Title']")),
            additional_text=self._get_list_values(
                element.find(".//Property[@name='AdditionalText']"), "AdditionalText"
            ),
            additional_text_alien=self._get_list_values(
                element.find(".//Property[@name='AdditionalTextAlien']"), "AdditionalTextAlien"
            ),
            mood=self._get_complex_value(element.find(".//Property[@name='Mood']"), "Mood"),
            race=self._get_complex_value(element.find(".//Property[@name='Race']"), "AlienRace"),
            progressive_dialogue=self._get_text(
                element.find(".//Property[@name='ProgressiveDialogue']")
            ),
        )

        # ProgressiveDialogue приходит строкой "true"/"false" — приводим к булеву
        if dialog.progressive_dialogue is not None:
            dialog.progressive_dialogue = dialog.progressive_dialogue.lower() == "true"

        # Парсим AdvancedInteractionFlow — сложные сцены с последовательным текстом
        flow_elem = element.find(".//Property[@name='AdvancedInteractionFlow']")
        if flow_elem is not None:
            for item in flow_elem.findall(".//Property[@value='GcPuzzleTextFlow']"):
                entry = self._parse_text_flow(item)
                if entry:
                    dialog.advanced_interaction_flow.append(entry)

        # Парсим Options — варианты ответов игрока
        options_elem = element.find(".//Property[@name='Options']")
        if options_elem is not None:
            for item in options_elem.findall(".//Property[@value='GcAlienPuzzleOption']"):
                option = self._parse_option(item)
                if option:
                    dialog.options.append(option)

        return dialog

    def parse_dialogues(self) -> List[DialogEntry]:
        """
        Главный метод. Рекурсивно обходит ВСЕ .mxml файлы в metadata_dir,
        находит в них GcAlienPuzzleEntry и возвращает плоский список DialogEntry.
        """
        all_dialogs: List[DialogEntry] = []

        for file_path in self.metadata_dir.rglob("*.mxml"):
            tree = ET.parse(file_path)
            root = tree.getroot()

            for entry in root.findall(".//Property[@value='GcAlienPuzzleEntry']"):
                dialog = self._parse_dialog_entry(entry)
                # Добавляем только если есть ID (без ID диалог недействителен)
                if dialog and dialog.id:
                    all_dialogs.append(dialog)

        return all_dialogs