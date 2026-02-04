from data import load_data
import streamlit as st
import tabs.ausgabe as ausgabe, tabs.arbeitszeit as arbeitszeit, tabs.browse_data as browse_data, tabs.überblick as überblick


def main():
    df = load_data()

    tab1, tab2, tab3, tab4  = st.tabs(['Überblick', 'Arbeitszeit', 'Kauf eintragen', 'Alle Ausgaben'], width='stretch')

    with tab1:
        überblick.render(df)

    with tab2:
        arbeitszeit.render(df)

    with tab3:
        ausgabe.render()

    with tab4:
        browse_data.render(df)

if __name__ == "__main__":
    main()