import subprocess
import sys
from pathlib import Path
from config import CONFIG


def check_and_install_hgpaktool():
    try:
        import hgpaktool
        print("✓ hgpaktool уже установлен")
        return True
    except ImportError:
        print("⚠ hgpaktool не найден. Устанавливаю...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "hgpaktool"])
            print("✓ hgpaktool успешно установлен")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Не удалось установить hgpaktool: {e}")
            sys.exit(1)


def check_mbin_compiler():
    compiler_path: Path = CONFIG["compiler"]
    if compiler_path.exists():
        print(f"✓ MBINCompiler.exe найден: {compiler_path}")
        return True
    else:
        print(f"✗ MBINCompiler.exe не найден!")
        print("   Положите его в папку tools/")
        return False


def bootstrap():
    print("=== NMS Translator Bootstrap ===")
    check_and_install_hgpaktool()
    check_mbin_compiler()
    print("=== Bootstrap завершён ===\n")


if __name__ == "__main__":
    bootstrap()