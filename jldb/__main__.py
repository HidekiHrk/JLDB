import sys
import os
from dbclasses import Client

version = 'v0.1'

# utils #

def message(message, name="system", linebreak=True):
    if linebreak: sys.stdout.write('\n')
    print(f"[{name}]: {message}")

# main #

def main(path):
    client = Client(path)
    exitStatus = 0
    current_table = None
    alter = ""
    def clear():
        os.system("clear")
        print(
            f"JLDB Shell {version}",
            f"Editing JL Database file: {path}",
            f"Current Table: {current_table.name if current_table else 'Nenhuma'}",
            f"Alterations: {alter}",
            sep="\n"
        )
    clear()
    while True:
        # Header #
        try:
            command = input('> ')
        except (KeyboardInterrupt, EOFError):
            if exitStatus == 0:
                message("To exit, press ^C one more time, or type exit")
                exitStatus += 1
                continue
            elif exitStatus == 1:
                if current_table:
                    clear()
                    message(f"Table {current_table.name} closed", linebreak=False)
                    current_table = None
                    exitStatus = 0
                    continue
                sys.exit()
        if exitStatus > 0: exitStatus = 0
        if command.strip().lower() == "exit":
            sys.exit(0)
        elif command.strip().lower() == "clear":
            clear()
        elif command.strip().lower().startswith("table:"):
            current_table = client.get_table(command.split(':'))
        else:
            loc = locals()
            obj_str = "current_table" if current_table else "client"
            exec(f"result = {obj_str}.{command.strip()}", globals(), loc)
            result = loc['result']
            if type(result).__name__ == "Table":
                current_table = result
                clear()
            elif type(result).__name__ == "Row":
                print(result.dict)

args = sys.argv

if len(args) >= 2:
    path = ' '.join(args[1:])
    main(path)