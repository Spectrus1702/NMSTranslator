from hgpaktool import HGPAKFile
from pathlib import Path
import subprocess
from config import CONFIG


class NMSTranslatorPipeline:
    """
    Конвейер распаковки MBIN из PAK-архивов игры и компиляции их в MXML.
    Эта штука дёргает HGPAKFile (питонячья обёртка для libhgap) и MBINCompiler.exe.
    """

    def __init__(self):
        self.temp_dir = CONFIG["temp_dir"]
        self.pak_dir = CONFIG["pak_dir"]
        self.compiler = CONFIG["compiler"]

    def resolve_path(self, pak: HGPAKFile, mbin_path: str) -> Optional[str]:
        """
        Внутри PAK-архива регистр имён файлов может гулять (METADATA vs Metadata vs metadata).
        Эта функция ищет реальный путь внутри архива, игнорируя регистр.
        """
        target = mbin_path.replace("\\", "/").lower()
        for real in pak.files.keys():
            if real.lower() == target:
                return real
        return None

    def extract_file(self, pak_path: Path, mbin_path: str) -> Path:
        """
        Извлекает ОДИН файл mbin_path из PAK-архива pak_path во временную папку.
        Возвращает путь к извлечённому файлу на диске.
        """
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        with HGPAKFile(pak_path) as pak:
            real = self.resolve_path(pak, mbin_path)
            if not real:
                raise FileNotFoundError(f"Файл не найден в архиве {pak_path.name}: {mbin_path}")
            pak.unpack(self.temp_dir, filters=real)

        return self.temp_dir / real

    def compile_file(self, mbin_file: Path):
        """
        Запускает MBINCompiler.exe для конвертации MBIN → MXML.
        После компиляции удаляет исходный MBIN (он больше не нужен).
        Ключ -q = quiet mode (меньше вывода в консоль).
        """
        mxml_file = mbin_file.with_suffix(".MXML")

        # Если старый MXML остался с прошлого запуска — удаляем
        if mxml_file.exists():
            mxml_file.unlink()

        subprocess.run(
            [str(self.compiler), "-q", str(mbin_file)],
            check=True
        )

        # Исходный MBIN больше не нужен, освобождаем место
        if mbin_file.exists():
            mbin_file.unlink()

    def run(self, db: dict):
        """
        Главный метод. Принимает словарь {mbin_path: pak_name} из files.json.
        Для каждого файла: извлекает из архива → компилирует в MXML.
        """
        print(f"Файлов для извлечения: {len(db)}")
        for mbin_path, pak_name in db.items():
            print(f"→ {Path(mbin_path).name}", end=" ")
            try:
                mbin_file = self.extract_file(self.pak_dir / pak_name, mbin_path)
                print(".", end="")
                self.compile_file(mbin_file)
                print(" ✓")
            except Exception as e:
                print(f" ✗ ({e})")