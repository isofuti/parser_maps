import subprocess
import sys

def run_parsers(*args):
    # Запуск link_parser.py с переданными аргументами
    subprocess.run(['python', 'link_parser.py'] + list(args), check=True)
    
    # Запуск info_parser.py с теми же аргументами
    subprocess.run(['python', 'info_parser.py'] + list(args), check=True)

if __name__ == "__main__":
    # Проверка аргументов командной строки
    if len(sys.argv) < 1:
        print("Использование: python goodinie.py <аргументы>")
        sys.exit(1)

    # Запуск функции с аргументами командной строки
    run_parsers(*sys.argv[1:])
