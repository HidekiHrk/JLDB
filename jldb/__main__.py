import sys
import os

try:
    from dbclasses import Client
except:
    from jldb.dbclasses import Client

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
    current_row = None
    def getstr():
        nstr = {"current_row":current_row, "current_table":current_table, "client":client}
        for x in nstr:
            if nstr.get(x):
                return x
    def clear():
        os.system("clear")
        print(
            f"JLDB Shell {version}",
            f"Editing JL Database file: {path}",
            f"Current Table: {current_table.name if current_table else 'Nenhuma'}",
            f"Current Row: {current_row.row_id if current_row else 'Nenhuma'}",
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
                if current_row:
                    current_row = None
                    exitStatus = 0
                    clear()
                    message(f"Row {current_row.row_id} closed", linebreak=False)
                    continue
                elif current_table:
                    current_table = None
                    exitStatus = 0
                    clear()
                    message(f"Table {current_table.name} closed", linebreak=False)
                    continue
                sys.exit(0)
        if exitStatus > 0: exitStatus = 0
        if command.strip().lower() == "exit":
            if current_row: current_row = None; continue
            if current_table: current_table = None; continue
            sys.exit(0)
        elif command.strip().lower() == "fexit":
            sys.exit(0)
        elif command.strip().lower() == "clear":
            clear()
        else:
            if command.strip().lower().startswith("get:"):
                new_command = command.strip()[4:]
                if new_command:
                    try:
                        result = eval(f"{getstr()}.{new_command.strip()}")
                    except Exception as e:
                        message(f"Comando inválido.\n{e}", linebreak=False)
                        continue
                    if type(result).__name__ == "Row":
                        current_row = result
                        clear()
                        continue
                    if type(result).__name__ == "Table":
                        current_table = result
                        clear()
                        continue
                    message(f"Output: {result}", linebreak=False)
                else:
                    message(f"Comando inválido.", linebreak=False)
                    continue
            else:
                try:
                    exec(f"{getstr()}.{command.strip()}")
                except Exception as e:
                    message(f"Comando inválido.\n{e}", linebreak=False)
                    continue
args = sys.argv

if len(args) >= 2:
    if args[1].strip().lower() == "--help":
        print(f"""
            usage:
                {args[0]} [path...]
        """)
    else:
        path = ' '.join(args[1:])
        main(path)