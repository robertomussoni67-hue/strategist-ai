# strategist.py
# Script principale per il progetto Strategist

import sys
from modules.macro_module import execute_macro  # import dal pacchetto modules

def main():
    # Se lanci con un argomento da terminale, lo uso come comando
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
    else:
        comando = "report"  # predefinito se non passi nulla

    execute_macro(comando)

if __name__ == "__main__":
    main()