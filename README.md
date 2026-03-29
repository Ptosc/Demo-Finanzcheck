# 💰 Ausgaben-Tool (Demo-Version)

Ein interaktives Streamlit-Projekt zur Erfassung, Analyse und Reflexion persönlicher Ausgaben. In dieser Demo-Version werden generierte Daten verwendet, um die Funktionalität zu demonstrieren. Das Tool visualisiert Ausgaben, analysiert Arbeitszeit hinter Kosten und zeigt Sparpotenziale auf – alles automatisiert, sodass die Ergebnisse sofort sichtbar sind.

Demo ansehen: https://ausgabencheck-f7zmzpgxewyy9xufzpvpel.streamlit.app

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

⸻

### Technischer Überblick
	•	Programmiersprache: Python
	•	Framework: Streamlit
	•	Visualisierung: Matplotlib, Seaborn
	•	Datenpersistenz: Google Sheets API
	•	Architektur: Modular (Tabs, Data, Analyse, Visualisierung)