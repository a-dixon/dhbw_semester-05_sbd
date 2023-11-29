import click
import requests
from colorama import Fore, Style, init
import os
from click.termui import style

init(autoreset=True)

# Globale Variablen für die Anmeldedaten
username = None
api_key = None

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

def api_request(endpoint, data):
    url = f"https://10.0.1.10:8090/v1/admin/{endpoint}"
    try:
        response = requests.post(url, json=data, verify="config/certificates/root_ca/ca-public-key.pem")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        click.echo(Fore.RED + f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        click.echo(Fore.RED + f"Anfragefehler: {err}")
    except ValueError as verr:
        click.echo(Fore.RED + f"JSON Dekodierungsfehler: {verr}")
    return {}

def login():
    global username, api_key

    click.echo(Fore.GREEN + center_text("===== ANMELDUNG =====", terminal_width))
    username = click.prompt(Fore.CYAN + "Username")
    api_key = click.prompt("API Key")
    click.echo(Fore.GREEN + "Anmeldung erfolgreich!")

def neue_customer_portale():
    global username, api_key

    if username is None or api_key is None:
        click.echo(Fore.RED + "Fehler: Nicht angemeldet. Das Programm wird beendet.")
        return

    data = {"username": username, "api_key": api_key}
    response = api_request("customer-create", data)

    if "customer_UID" in response and "customer_api_key" in response:
        click.echo(Fore.YELLOW + "Kunde erfolgreich erstellt:")
        click.echo(f"Kunden-UID: {response['customer_UID']}")
        click.echo(f"Kunden-API-Key: {response['customer_api_key']}")
    else:
        click.echo(Fore.RED + f"Fehler: {response.get('message', 'Unbekannter Fehler')}")

if __name__ == "__main__":
    terminal_height, terminal_width = get_terminal_size()

    clear_screen()
    login_text = center_text("===== ANMELDUNG =====", terminal_width)
    click.echo(style(login_text, fg="green"))
    username = click.prompt(style(Fore.CYAN + "Username", fg="green"))
    api_key = click.prompt(style("API Key", fg="green"))
    click.echo(style(Fore.GREEN + "Anmeldung erfolgreich!", fg="green"))
    click.pause(info="Drücken Sie eine Taste, um fortzufahren...")

    while True:
        clear_screen()
        menu_width = 30
        menu_indent = (terminal_width - menu_width) // 2
        click.echo(" " * menu_indent + Fore.BLUE + "========== MENÜ ==========")
        click.echo(" " * menu_indent + "1. " + Fore.YELLOW + "Neue Kundenportale hinzufügen")
        click.echo(" " * menu_indent + "2. " + Fore.RED + "Beenden" + Style.RESET_ALL)
        click.echo(" " * menu_indent + "=" * menu_width)

        choice = click.prompt(Fore.CYAN + "Bitte wählen Sie eine Option (1-2)", type=int)

        if choice == 1:
            neue_customer_portale()
        elif choice == 2:
            click.echo(Fore.RED + "Programm wird beendet.")
            break
        else:
            click.echo(Fore.RED + "Ungültige Option. Bitte wählen Sie erneut.")
        click.pause(info="Drücken Sie eine Taste, um fortzufahren...")