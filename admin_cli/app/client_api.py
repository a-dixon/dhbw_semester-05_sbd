import requests
import click

class APIClient:
    def __init__(self, base_url, cert_path):
        self.base_url = base_url
        self.cert_path = cert_path
        self.username = None
        self.api_key = None

    def api_request(self, endpoint, data=None, method='POST'):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, json=data, verify=self.cert_path)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            click.echo(click.style(f"HTTP Error: {errh}", fg='red'))
        except requests.exceptions.RequestException as err:
            click.echo(click.style(f"Anfragefehler: {err}", fg='red'))
        except ValueError as verr:
            click.echo(click.style(f"JSON Dekodierungsfehler: {verr}", fg='red'))
        return {}

    def login(self):
        self.username = input("Username: ")
        self.api_key = input("API Key: ")
        print("Die Anmeldedaten wurden gespeichert.")

    def new_customer_portals(self):
        data = {"username": self.username, "api_key": self.api_key}
        response = self.api_request("customer-create", data)

        if "customer_UID" in response and "customer_api_key" in response:
            click.echo(click.style("Kunde erfolgreich erstellt:", fg='yellow'))
            click.echo(f"Kunden-UID: {response['customer_UID']}")
            click.echo(f"Kunden-API-Key: {response['customer_api_key']}")
        else:
            error_message = response.get('message', 'Unbekannter Fehler')
            click.echo(click.style(f"Fehler: {error_message}", fg='red'))

    def list_customer_portals(self):
        data = {"api_key": self.api_key, "username": self.username}
        response = self.api_request("customer-list", data, method='GET')
        click.echo(click.style("Liste der Kundenportale:", fg='blue'))
        for customer_portal in response.get('customer_portals', []):
            click.echo(f"Kunden-UID: {customer_portal['customer_UID']}, API-Key: {customer_portal['api_key']}")

    def list_smart_meters_of_customer(self, customer_UID):
        data = {"api_key": self.api_key, "username": self.username, "customer_UID": customer_UID}
        response = self.api_request("meter-list", data, method='GET')
        click.echo(click.style("Liste der Smartmeters:", fg='blue'))
        for meter in response.get('meters', []):
            click.echo(f"Smartmeter: {meter['meter_UID']}")

    def delete_customer_portal(self, customer_UID):
        data = {"api_key": self.api_key, "username": self.username, "customer_UID": customer_UID}
        response = self.api_request("customer-delete", data, method='DELETE')
        if "message" in response:
            click.echo(response["message"])
        else:
            click.echo(click.style("Fehler beim Löschen des Kundenportals.", fg='red'))