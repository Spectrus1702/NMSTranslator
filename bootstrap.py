import subprocess
import sys
from pathlib import Path
from config import CONFIG


def check_and_install_hgpaktool():
    """
    Проверяет, установлен ли пакет hgpaktool (обёртка для libhgap).
    Если нет — автоматически ставит через pip.
    hgpaktool нужен для чтения PAK-архивов игры (.pak).
    """
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
    """
    Проверяет, лежит ли MBINCompiler.exe в папке tools/.
    Этот экзешник конвертирует игровые MBIN-файлы в читаемый MXML и обратно.
    Качать с GitHub: https://github.com/monkeyman192/MBINCompiler
    """
    compiler_path: Path = CONFIG["compiler"]
    if compiler_path.exists():
        print(f"✓ MBINCompiler.exe найден: {compiler_path}")
        return True
    else:
        print(f"✗ MBINCompiler.exe не найден!")
        print("   Положите его в папку tools/")
        return False


def bootstrap():
    """
    Точка входа. Проверяет все зависимости перед запуском основного приложения.
    Вызывается в самом начале, чтобы не упасть на полпути из-за отсутствия инструментов.
    """
    print("=== NMS Translator Bootstrap ===")
    check_and_install_hgpaktool()
    check_mbin_compiler()
    print("=== Bootstrap завершён ===\n")


if __name__ == "__main__":
    bootstrap()