
# 💰 Ausgaben-Tool (Demo-Version)

Ein interaktives Streamlit-Projekt zur Erfassung, Analyse und Reflexion persönlicher Ausgaben. Entstanden, weil meine Schwester sich ständig beschwert hat, dass sie zu viel impulsiv ausgibt. Ich dachte: cooles Projekt bauen, das ihr wirklich hilft – und jetzt benutzen wir die App tatsächlich beide, ich tracke sogar meine eigenen Einnahmen. 😅

In dieser Demo-Version gibt es generierte Daten, damit man die Funktionen ausprobieren kann. Das Tool visualisiert Ausgaben, zeigt den Arbeitszeitaufwand hinter jeder Ausgabe und Sparpotenziale – alles automatisch, sodass Ergebnisse sofort sichtbar sind.

Demo ansehen: Ausgaben-Tracker￼

⸻

## Funktionen

1. Überblick
	•	Gesamtübersicht über Ausgaben, Transaktionen und Durchschnitt pro Tag
	•	Visualisierung nach Kategorien
	•	Vergleich zu vorherigen Zeiträumen

2. Arbeitszeit
	•	Berechnet, wie viele Stunden Arbeit hinter jeder Ausgabe stecken
	•	Zeigt Einsparpotenziale und den „Zeitwert“ des Geldes

3. Kauf eintragen
	•	Formular zur Erfassung neuer Ausgaben
	•	Kategorien, Betrag, Beschreibung und Zahlungsart
	•	Speicherung in Google Sheets

4. Alle Ausgaben
	•	Durchsuchen, Filtern und Analysieren aller bisherigen Einträge
	•	Heatmap zur Erkennung von Ausgabemustern
	•	Top-Einzelausgaben visualisieren Impulskäufe

5. Reflexion
	•	Bewertungs-Tool: Wie wertvoll war jede Ausgabe?
	•	Dynamische Feedback-Texte zur Selbstreflexion
	•	Inspirierende Zitate für achtsame Finanzentscheidungen

Ich habe schnell gemerkt, dass nicht jede „coole“ Idee auch wirklich benutzt wird. Zum Beispiel dachte ich zuerst, dass jeder eine Heatmap haben will – am Ende haben wir sie fast nie genutzt. Echtes Feedback von mir und meiner Schwester war viel hilfreicher als alle theoretischen Überlegungen.

⸻

### Technischer Überblick
	•	Programmiersprache: Python
	•	Framework: Streamlit
	•	Visualisierung: Matplotlib, Seaborn
	•	Datenpersistenz: Google Sheets API
	•	Architektur: Modular (Tabs, Data, Analyse, Visualisierung)
	•	Besonderheiten: Google Authenticator Integration war tricky, genauso wie 		SessionStates in Streamlit