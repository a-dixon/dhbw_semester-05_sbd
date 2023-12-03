# security_by_design

## Installation
Unsere Anwendung wird über Docker bereitgestellt. 

Getestet ist die Anwendung unter: 
- Ubuntu in der Version 22.04
- Docker in der Version 24.0

Mit dem folgenden Befehl werden die Container gestartet:
```
docker compose up
```

Mit dem folgenden Befehl werden die Container gestoppt:
```
docker compose down
```

Mit dem folgenden Befehl können die Container gebaut werden:
```
docker compose build
```
Die obigen Befehle funktionieren auch mit `docker-compose ...`.

## IP Adressen
Die verschiedenen Teile unserer Anwendung stehen unter den folgenden IP Adressen zur Verfügung:
- Das Provider Portal unter `10.0.1.10`.
- Der Smart Meter Wrapper unter `10.0.1.20`.
- Die InfluxDB unter `10.0.1.30`.
- Die MySQL unter `10.0.1.40`.
- Das PHPMyAdmin Interface unter `10.0.1.50`.

## Aufbau
Die Smart Meter, die erstellt werden, senden Messdaten an das Provider Portal, wo sie in der InfluxDB gespeichert werden.
Diese Messdaten können in der InfluxDB unter `https://10.0.1.30` mit den gesetzten Passwörtern eingesehen werden.

Die Schnittstelle für die Stromanbieter (API Endpoint) ist unter `https://10.0.1.10` verfügbar.

Die Konfiguration der Stromanbieter im Provider Portal geschieht über die Admin CLI, die über die Admin API Schnittstelle mit dem Provider Portal kommuniziert.

## Passwörter
Die Anwendung kommt mit Standardpasswörtern. Diese dürfen unter keinen Umständen in der Produktion verwendet werden und müssen geändert werden.

Die Passwörter sind im folgenden Pfad zu finden:
`provider_portal/config/secrets`

Die Passwörter im obigen Pfad werden in der Docker Compose als Secrets eingebunden und beim `build` des Containers gesetzt. Sie müssen dementsprechend vor dem erstmaligen `build` ausgetauscht werden.

## Certificates
Für die Certificates gilt die gleiche Regel wie für die Passwörter:
Sie sind default und öffentlich zugänglich. Vor dem ersten Starten müssen sie geändert werden.

Die Certificates liegen unter dem folgenden Pfad:
`provider_portal/config/certificates`

## Inbetriebnahme
Um die Anwendung in Betrieb zu nehmen, muss nach dem Starten der Container ein Stromanbieter hinzugefügt werden. Dies ist mit Hilfe der Admin CLI möglich. Diese liegt im Pfad `admin_cli/run.py`.

Um ein Stromanbieter anzulegen muss in den `admin_cli` Ordner navigiert werden. Hier kann mit dem folgenden Befehl die Admin CLI gestartet werden:
```
python3 run.py
```

Der Username und der API Key für die Admin CLI befinden sich in der folgenden Datei:
```
provider_portal/config/secrets/admin_users.txt
```

Diese müssen für den produktiven Betrieb geändert werden!

Im Menü der Admin CLI gibt es die folgenden fünf Wahlmöglichkeiten:
1. Neue Kundenportale hinzufügen
2. Kundenportale auflisten
3. Kundenportal löschen
4. Smartmeter auflisten
5. Beenden

Mit Eingabe einer `1` wird ein neues Kundenportal angelegt. Die Kunden-UID und der API-Key müssen gespeichert werden, da mit diesen die Authentifizierung an der API stattfindet.

Mit Eingabe einer `2` werden alle angelegten Kundenportale angezeigt.

Ein Kundenportal kann anhand der `Kunden-UID` gelöscht werden. Hierfür muss im Menü nach Eingabe einer `3` die `Kunden-UID` eingegeben werden.

Es können alle Smartmeter aufgelistet werden, die mit einem Kundenportal verknüpft sind. Hierfür muss im Menü eine `4` eingegeben werden, gefolgt von der `Kunden-UID`.

## Logging
Vom Provider Portal wird extensives Logging betrieben. Beim erstmaligen Starten wird die Log Datei erstellt. Diese ist unter folgendem Pfad zu finden:
```
provider_portal/provider_portal.log
```
