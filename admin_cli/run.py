import os

import click
from click import style
from colorama import Fore, Style

from app.client_api import APIClient


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_size():
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(rows), int(columns)
    except:
        return 24, 80  # Standardgröße


def center_text(text, width):
    return (" " * ((width - len(text)) // 2)) + text


if __name__ == "__main__":
    terminal_height, terminal_width = get_terminal_size()

    api = APIClient(base_url="https://10.0.1.10:8090/v1/admin/", cert_path="config/certificates/root_ca/ca-public-key.pem")

    clear_screen()
    login_text = center_text("===== ANMELDUNG =====", terminal_width)
    click.echo(style(login_text, fg="green"))
    api.login()
    click.echo(style(Fore.GREEN + "Die Session wurde initiiert", fg="green"))
    click.pause(info="Drücken Sie eine Taste, um fortzufahren...")

    while True:
        clear_screen()
        menu_width = 30
        menu_indent = (terminal_width - menu_width) // 2
        click.echo(" " * menu_indent + Fore.BLUE + "========== MENÜ ==========")
        click.echo(" " * menu_indent + "1. " + Fore.YELLOW + "Neue Kundenportale hinzufügen")
        click.echo(" " * menu_indent + "2. " + Fore.YELLOW + "Kundenportale auflisten")
        click.echo(" " * menu_indent + "3. " + Fore.YELLOW + "Kundenportal löschen")
        click.echo(" " * menu_indent + "4. " + Fore.YELLOW + "Smartmeter auflisten")
        click.echo(" " * menu_indent + "5. " + Fore.RED + "Beenden" + Style.RESET_ALL)
        click.echo(" " * menu_indent + "=" * menu_width)

        choice = click.prompt(Fore.CYAN + "Bitte wählen Sie eine Option (1-5)")

        if choice == "1":
            api.new_customer_portals()
        elif choice == "2":
            api.list_customer_portals()
        elif choice == "3":
            customer_UID = input("Bitte geben Sie die Kunden-UID ein: ")
            api.delete_customer_portal(customer_UID)
        elif choice == "4":
            customer_UID = input("Bitte geben Sie die Kunden-UID ein: ")
            api.list_smart_meters_of_customer(customer_UID)
        elif choice == "5":
            click.echo(Fore.RED + "Programm wird beendet.")
            break
        else:
            click.echo(Fore.RED + "Ungültige Option. Bitte wählen Sie erneut.")
        click.pause(info="Drücken Sie eine Taste, um fortzufahren...")
