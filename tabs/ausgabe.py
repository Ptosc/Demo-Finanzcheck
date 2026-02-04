from datetime import datetime
import streamlit as st
from data import get_sheet

def render():

    st.title("✍️ Ausgabe eintragen")

    sheet = get_sheet()

    kategorien = [
        "Alltag & Essen",
        "Freizeit & Soziales",
        "Kleidung & Pflege",
        "Bildung & Entwicklung",
        "Sparen & Rücklagen"
        ] 

    zahlungsarten = ['Bar', 'Kreditkarte', 'PayPal', 'Banküberweisung', 'Apple Pay']

    with st.form("ausgabe_form"):
        kategorie = st.selectbox("Kategorie", kategorien)

        betrag = round(
            st.number_input("Betrag (€)", min_value=0.0, step=0.5),
            2
        )

        beschreibung = st.text_input("Beschreibung")
        zahlungsart = st.selectbox("Zahlungsart", zahlungsarten)

        submitted = st.form_submit_button("Eintragen")

    if submitted:
        # Pflichtfeldprüfung
        if not kategorie or betrag <= 0 or not beschreibung.strip() or not zahlungsart:
            st.warning("Bitte fülle alle Felder aus und gib einen Betrag größer 0 ein 🛑")
        else:
            try:
                sheet.append_row([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                    kategorie, 
                    betrag,
                    beschreibung.strip(),
                    zahlungsart
                ])
                st.success("Ausgabe gespeichert ✅")
            except Exception as e:
                st.error(f"Fehler beim Eintragen: {e}")