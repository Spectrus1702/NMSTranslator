from hgpaktool import HGPAKFile
from pathlib import Path
import subprocess
from config import CONFIG


class NMSTranslatorPipeline:
    def __init__(self):
        self.temp_dir = CONFIG["temp_dir"]
        self.pak_dir = CONFIG["pak_dir"]
        self.compiler = CONFIG["compiler"]

    def resolve_path(self, pak, mbin_path: str):
        target = mbin_path.replace("\\", "/").lower()
        for real in pak.files.keys():
            if real.lower() == target:
                return real
        return None

    def extract_file(self, pak_path: Path, mbin_path: str) -> Path:
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        with HGPAKFile(pak_path) as pak:
            real = self.resolve_path(pak, mbin_path)
            if not real:
                raise FileNotFoundError(f"Файл не найден: {mbin_path}")
            pak.unpack(self.temp_dir, filters=real)
        return self.temp_dir / real

    def compile_file(self, mbin_file: Path):
        mxml_file = mbin_file.with_suffix(".MXML")
        if mxml_file.exists():
            mxml_file.unlink()
        subprocess.run(
            [str(self.compiler), "-q", str(mbin_file)],
            check=True
        )
        if mbin_file.exists():
            mbin_file.unlink()

    def run(self, db: dict):
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