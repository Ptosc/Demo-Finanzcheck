import streamlit as st

# Style-Funktion 
def highlight_expenses(val):
    highlight_color = "rgba(255, 158, 158, 0.4)"  # Pastell-Rot
    try:
        # Betrag extrahieren
        num = float(str(val).replace(" €",""))
        return f"background-color: {highlight_color}" if num > st.session_state.mark else ""
    except:
        return ""
    
def render(df):
    with st.expander("🪜 Kurzer Einstieg"):
            st.write("""
            🔹 Verschiebe den Slider um Teure Käufe zu markieren  
            🔹 Klick auf die Spalten, um die Ausgaben zu sortieren  
            🔹 Du kannst nach Betrag, Datum oder Kategorie filtern
            """)

    # Spalten sortieren: Wichtiges zuerst
    cols_order = ["Zeitstempel", "Tag", "Kategorie", "Beschreibung", "Betrag", "Zahlungsart", "Woche", "Monat", "Stunde", "Monat & Jahr"]
    df = df[cols_order]
    # Zahlen formatieren
    df["Betrag"] = df["Betrag"].map(lambda x: f"{x:.2f} €")

    # Slider erstellen, initial mit session_state
    mark = st.slider(f'Kosten', min_value=0, max_value=100, value=50, step=1)
    st.session_state.mark = mark

    color = 'background-color: #ffcccc' if mark > st.session_state.mark else ''

    sorted_df = df.sort_values(by='Zeitstempel', ascending=False)

    styled_df = sorted_df.style.map(highlight_expenses, subset=['Betrag'])


    st.markdown("## 💸 Alle Ausgaben im Überblick")
    
    st.dataframe(styled_df, height=400)

    st.caption("Tipp: Einmal auf eine Spalte tippen, sortiert sie auf- oder absteigend")