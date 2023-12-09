# Provider Portal 

# Spezifikation

## Plattform / Technologien

- Docker Stack
	- Container für Provider Portal
	- Container für Wrapper der Smart Meter (Umgebung in der mehrere Stromzähler betrieben werden)
- Python als Programmiersprache
- Schnittstellen: HTTPS REST API
- Authentifizierung: API Keys
- Komponenten:
	- Smart Meter
	- Provider Portal
	- Datenbanken (relationale Datenbank, InfluxDB)
	- CLI Administrations-Interface
## Smart Meter
- "generate consumption" Funktion:
	- Bekommt aktuelles Datum und die aktuelle Uhrzeit übergeben.
	- Gibt den aktuellen Verbraucht anhand eines Lastprofils mit einem Faktor zurück.
	- Das Lastprofil spiegelt den üblichen Tagesverbrauch wieder.
 - "get consumption" Funktion:
	 - Ruft jede Sekunde die "generate consumption" Funktion auf.
	 - Speichert die Daten der "generate consumption" Funktion in einem Array.
	 - Das Array beinhaltet 3600 Datenpunkte (einer pro Sekunde für eine Stunde) mit der dazugehörigen Zeit/Datum.
- "transfer" Funktion: 
	- Wird einmal pro Minute aufgerufen.
	- Speichert letzten Datenpunkt mit Zeitstempel aus Array.
	- Überträgt alle Daten bis zu diesem gespeicherten Datenpunkt an das Provider Portal.
	- Nach bestätigt erfolgreicher Übertragung wird gespeicherter Datenpunkt mit Zeitstempel an "delete" Funktion übergeben.
- "delete" Funktion: 
	- Bekommt Datenpunkt mit Zeitstempel übergeben.
	- Löscht alle Datenpunkte aus dem Array bis zum übergebenen Datenpunkt.
- REST API Schnittstelle: Smart Meter - Provider Portal
	- Nutzung der REST API Schnittstelle des Provider Portals
	- Zur Authentifizierung und Autorisierung wird ein festprogrammierter Authentifizierungscode und UID verwendet.
- Die Daten werden nur in eine Richtung vom Smart Meter zum Provider Portal übertragen (BSI Standard)
- Die Daten werden durch HTTPS / TLS verschlüsselt übertragen
- Nach bestätigt abgeschlossener Übertragung an das Provider Portal, werden die Datenpunkte über die "delete" Funktion gelöscht. 
## Provider Portal
- REST API Schnittstelle: Provider Portal - Customer Portal
	- Authentifizierung über vorher übertragenen API Key und UID für jedes Customer Portal
1. Smart Meter anlegen:
	- Übermittlung von UID von neuem Smart Meter
	- Es wird geprüft, ob die UID des Smart Meters in Kombination mit der UID des Anbieter bereits existiert. 
	- Wenn die Kombination existiert, wird eine Fehlermeldung zurückgegeben.
	- Wenn die Kombination nicht existiert, wird der Nutzer angelegt.
	- Es wird ein Datenbankeintrag in der Meters Table erstellt.
		- Der Eintrag beinhaltet die übertragene UID des Smart Meters und ein API Key, der generiert wird.
	- Analog wird ein Eintrag in der Customers-Meters Table gemacht.
		- Der Eintrag beinhaltet die UID des Customer Portals und die UID des Smart Meters
	- (Stromzähler Wrapper per Schnittstelle oder händisch über neuen Meter informieren)
	- Die Response an das Customer Portal beinhaltet eine Meldung, ob das Anlegen des Smart Meters erfolgreich war.
2. Messdaten an Customer:
	- Übermittlung von UID von bestehendem Meter, der Zeitraum der gewünschten Daten und der gewünschte Abstand zwischen Messpunkten (Vielfaches einer Sekunde)
	- Prüfung, ob UID von Meter in Kombination mit UID von Anbieter nicht existiert.
		- Fehlermeldung, wenn die Kombination besteht.
		- Daten mit Parametern annehmen, wenn die Kombination nicht besteht.
	- Anfrage von Daten mit erhaltenen Parametern an InfluxDB
	- Konvertierung der Daten aus der InfluxDB in JSON Format
	- Response an Provider Portal mit Daten in JSON Format
3. Smart Meter löschen
	- Übermittlung von UID von zu löschendem Smart Meter
	- Prüfung, ob UID von Meter in Kombination mit UID von Customer existiert.
		- Fehlermeldung, wenn die Kombination existiert
		- Nutzer löschen, wenn die Kombination nicht existiert.
	- Datenbankeintrag in Meters Table löschen
		- Datenbankeintrag mit übertragenen UID von Smart Meter löschen
	- Datenbankeintrag in Customers-Meters Table löschen
		- Datenbankeintrag mit übertragenen UID von Smart Meter löschen
	- (Stromzähler Wrapper per Schnittstelle oder händisch Meter löschen)
	- Response an Customer Portal mit Meldung, dass Löschen erfolgreich war
- REST API Schnittstelle: Provider Portal - Smart Meter
	- Daten annehmen:
		- Authentifizierung über vorher übertragenen API Key und UID für jeden Smart Meter
		- Prüfung, ob UID existiert und API Key korrekt ist
			- Wenn ja, werden die Daten angenommen.
			- Wenn nein, wird eine Fehlermeldung als Response übermittelt
- Prüfung, ob früheste übertragene Wert bereits in InfluxDB existiert
	- Wenn ja, sind die Daten bereits erhalten worden. Eine Fehlermeldung wird als Response übermittelt.
	- Wenn nein, werden die Daten angenommen.
- Prüfung, ob 60 Datenpunkte pro Minute ankommen
	- Wenn ja, sind alle Daten korrekt angekommen.
	- Wenn nein, sind nicht alle Daten korrekt angekommen.
- Die Daten werden in der InfluxDB gespeichert.
- Response an Smart Meter, dass Daten angekommen und gespeichert sind.
- REST API Schnittstelle: Administration Provider Portal
	- Anlegen neuer Customer Portale
		- Authentifizierung über vorher übertragenen API Key und Username für jeden User
- Generieren von UID und API Key für das neue Customer Portal 
- (Prüfung auf Doppelung)
- Schreiben von UID und API Key in die Users Table der Datenbank
- Response beinhaltet die generierte UID und den generierten API Key
## Command Line Interface: Administration
- Menu Interface der Administration CLI
	- "Neues Customer Portal anlegen"
		- Eingabe von API Key und Username des Users
		- Aufruf der REST API Schnittstelle für das Anlegen neuer Customer Portale mit dem API Key und Username des Users
		- Response der REST API Schnittstelle mit UID und API Key ausgeben
## Datenbank
- Relationale Datenbank:
	- Customers: UID (PK) und API Key (Hash)
	- Customers-Meters: UID Customer, UID Meter
	- Meters: UID (PK), ~~API Key Smart Meter (Hash)~~, X.509 Zertifikate
	- Users: UID (PK), API Key User (Hash), Username
- InfluxDB:
	- Data: UID Users, Zeitpunkt, Messwerte
# Sicherheitsanalyse
## Intangible Assets
Im folgenden werden alle sog. "intangible Assets" aufgelistet. Diese sind alle Daten, die im zu entwickelnden System behandelt werden. Zu jedem intangible Asset stehen die Sicherheitsziele, die eingehalten werden müssen.
- IA-SM-01: Konfigurationsdaten
	- Integrität, Verfügbarkeit, Authentizität
- IA-SM-02: Messdaten
	- Vertraulichkeit, Integrität, Verfügbarkeit, Authentizität, Nicht-Abstreitbarkeit
- IA-SM-03: Anmeldedaten
	- Vertraulichkeit, Integrität, Verfügbarkeit, Identität
- IA-PP-04: Konfigurations-/Log-Daten
	- Integrität, Verfügbarkeit, Authentizität
- IA-PP-05: Meter-Daten (Meters)
	- Vertraulichkeit, Integrität, Verfügbarkeit, Identität
- IA-PP-06: Customer-Daten (Customers, Customers-Meters)
	- Vertraulichkeit, Integrität, Verfügbarkeit, Identität
- IA-PP-07: Messdaten (InfluxDB)
	- Vertraulichkeit, Integrität, Verfügbarkeit, Authentizität, Nicht-Abstreitbarkeit
- IA-PP-08: Administration-Anmeldedaten (Users)
	- Vertraulichkeit, Integrität, Verfügbarkeit, Identität
- (IA-PP-09: Verbindungs-/Anmeldungsdaten an Server) (theoretische Überlegung)
	- Vertraulichkeit, Integrität, Verfügbarkeit, Identität
## Tangible Assets
Im folgenden werden alle sog. "tangible Assets" aufgelistet. Diese sind die Komponenten, die im zu entwickelnden System existieren werden. Die Schutzziele aller tangible Assets sind Integrität und Verfügbarkeit
- TA-SM-01: Smart Meter
- TA-PP-02: Provider Portal
- TA-AA-03: CLI Administration (Anwendung)
- TA-SA-04: Administration (System)
- TA-CP-05: Customer Portal (Stromanbieter) (out of scope)
## Connections
### External Connections
Im folgenden werden alle sog. "external Connections" aufgelistet. Diese sind die externen Verbindungen, die im zu entwickelnden System existieren werden. Zu jeder Verbindung sind die intangible Assets aufgeführt, die über diese Verbindung laufen.
- EC-01: TA-SM-01 <--> TA-PP-02
	- IA-SM-01: Konfigurationsdaten
	- IA-SM-02: Messdaten
	- IA-SM-03: Anmeldedaten
- EC-02: TA-PP-02 <--> TA-AA-03
	- IA-PP-06: Customer-Daten (Customers, Customers-Meters)
	- IA-PP-08: Administration-Anmeldedaten (Users)
- EC-03: TA-PP-02 <--> TA-SA-04
	- IA-PP-04: Konfigurations-/Log-Daten
	- (IA-PP-09: Verbindungs-/Anmeldungsdaten an Server)
- EC-04: TA-PP-02 <--> TA-CP-05
	- IA-PP-05: Meter-Daten (Meters)
	- IA-PP-06: Customer-Daten (Customers, Customers-Meters)
	- IA-PP-07: Messdaten (InfluxDB)
### Internal Connections
Im folgenden werden alle sog. "internal Connections" aufgelistet. Diese sind die internen Verbindungen, die im zu entwickelnden System existieren werden. Zu jeder Verbindung sind die intangible Assets aufgeführt, die über diese Verbindung laufen.
- IC-01: TA-SM-01 <--> Stromsensor (theoretische Überlegung)
- IC-02: TA-PP-02 <--> Relationale Datenbank
	- IA-PP-04: Konfigurations-/Log-Daten
	- IA-PP-05: Meter-Daten (Meters)
	- IA-PP-06: Provider-Daten (Providers, Providers-Meters)
	- IA-PP-08: Administration-Anmeldedaten (Users)
- IC-03: TA-PP-02 <--> InfluxDB
	- IA-PP-05: Meter-Daten (Meters)
	- IA-PP-07: Messdaten (InfluxDB)
## Security Controls mit technologischem Kontext
Im folgenden werden alle "Security Controls" aufgelistet. Diese sind die Arten und Weisen, wie im zu entwickelnden System die internen und externen Verbindungen und die darin übertragenen intangible Assets geschützt werden.
Zu den Security Controls ist der technologische Kontext erläutert, der die notwendigen Sicherheitsaspekte der gewählten Technologien aufgreift.
- SC-01: TLS >= 1.2
	- Es existieren REST API Schnittstellen. Diese sind über HTTP erreichbar.
	- Um eine verschlüsselte Verbindung aufzubauen, wird HTTPS, bzw. TLS verwendet.
	- TLS wird mindestens in der Version 1.2 vorausgesetzt.
- SC-02: Input Validation (Schutz vor XSS, CSRF, SQL Angriffen)
	- Es werden SQL relationale Datenbanken verwendet. Um Schutz vor SQL Angriffen zu bieten, wird für Benutzereingaben eine Input Validation durchgeführt.
	- Die API Endpoints sind im Internet frei zugänglich. Um Schutz vor XSS und CSRF Angriffen zu bieten, wird eine Input Validation für Eingaben implementiert.
- SC-03: DDOS Protection (Schutz durch Rate Limiting)
	- Die API Endpoints sind im Internet frei zugänglich. Um Schutz vor DDOS Angriffen zu bieten, wird ein DDOS Protection Provider verwendet.
	- Der API Endpoint ist im Internet frei zugänglich. Um Schutz vor DDOS Angriffen zu bieten, wird Rate Limiting für die API Endpoints eingeführt. 
- SC-04: Authentifizierung
	- Die API Endpoints sind im Internet frei zugänglich. Damit keine unberechtigten Anfragen ausgeführt werden, wird Authentifizierung verwendet. Um die Anfragen authentifizieren zu können, werden API Keys verwendet.
	- Um berechtigte Anfragen identifizieren zu können, werden Anfragen anhand der UID authentisiert.
- SC-05: Autorisierung
	- Damit nicht-autorisierte Anfragen keine Daten erhalten, werden Anfragen anhand der übertragenen UID autorisiert.
- SC-06: Verschlüsselung von Daten (relationale Datenbank, InfluxDB)
	- Die Daten in den Datenbanken (relationale Datenbank und InfluxDB) werden verschlüsselt gespeichert, damit selbst bei unberechtigtem Zugriff auf die Datenbank kein Zugang zu den Daten möglich ist.
- SC-07: Logging
	- Damit keine unrechtmäßigen Änderungen an Daten oder Systemen unbemerkt vorgenommen werden können, werden Log-Dateien erstellt. 
	- Hierdurch wird die Integrität der Daten und Systemen gewahrt.
## Regulatorische Kontext
- KRITIS - Energie Sektor (Nach Anhang 1 - 2.20 des BSI-Gesetz BSI-KritisV) 
	- Daraus resultiert die Einhaltung der ISO27001 als Anforderung.
	- Des Weiteren auch der 2-jährliche Nachweis des Stand der Technik, somit eine Auffrischung der Zertifizierung 
- Die DSGVO spielt in unserem Kontext keine Rolle, da wir keine kundenbezogenen Daten innerhalb dieses Systems speichern.
- Der EU Cyber Resilience Act spielt aktuell keine Rolle, da es noch nicht in Kraft getreten ist. Es könnte allerdings bald eine Rolle spielen.
	- Es regelt Pflichten für Hersteller und Betreiber von digitalen Produkten 
		- Darunter sind etwaige Thematiken innerhalb der Planungs-, der Entwurfs-, der Entwicklungs-, Produktions-, Lieferungs- und Wartungsphase 
- Die ISO27001 betrifft nicht direkt das Produkt, sondern mehr ein Informationssicherheitsmanagementsystem (ISMS), welches für die Sicherheit in der Entwicklung und dem Betrieb des Produktes sorgen soll.
- Das MsbG (Messstellenbetriebsgesetz) ist ein deutsches Gesetz, welches einige Dinge regelt, um die sichere und schnelle Digitalisierung der Energiewende zu ermöglichen.
	- Wichtig in unserem Kontext ist, dass es Regelungen zu technischen Mindestanforderungen an Smart-Meter-Gateways und den Einsatz von intelligenten Messsystemen trifft (Kapitel 3).
		- Eine Regularie schreibt vor, sichere Verbindungen in Kommunikationsnetzen durchsetzen (Security Control SC-01, SC-04, SC-05).
		- Hinsichtlich konkreter technischer Anforderungen verweist es auf BSI: Technische Richtlinie TR-03109.
- BSI TR-03109 ist eine technische Richtlinie, die Sicherheitsanforderungen für Smart Meter Gateways festhält. Sie beschreibt eine sichere Kommunikation zwischen dem Stromzähler und Energieversorgungsunternehmen.
	- Einige technische Anforderungen sind:
		- Die Kommunikation zwischen Stromzählern und Gateways dürfen immer nur vom Stromzähler aufgebaut werden (wird durch das Design der Anwendung sichergestellt)
		- Verbindungen müssen stets geschützt sein (die Richtlinie setzt auch konkrete Standards hinsichtlich der Verschlüsselung fest, bspw. TLS >= 1.2 oder ein TLS Zertifikat zur Authentifizierung, in diesem Kontext wird stattdessen ein API-Key verwendet siehe Security Control SC-04)
	- Teilweise sind diese Anforderungen auch aus dem Dokument TR-03116 entnommen welches in TR-03109 referenziert wird