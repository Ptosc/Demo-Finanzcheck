import pandas as pd
import streamlit as st
import random
from datetime import datetime, timedelta
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials
import gspread

@st.cache_resource
def get_credentials():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    return Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )

def get_client():
    creds = get_credentials()
    return gspread.authorize(creds)

def get_sheet():
    gc = get_client()
    return gc.open('Demo Ausgaben').sheet1

#@st.cache_data(ttl=3600)
def load_data():
    sheet = get_sheet()
    df = get_as_dataframe(sheet, header=0).dropna(how="all")

    # Zeit in Datetime objekt umwandeln
    df["Zeitstempel"] = pd.to_datetime(df["Zeitstempel"], format="%Y-%m-%d %H:%M:%S.%f")

    # Betrag in Zahl umwandeln
    df['Betrag'] = pd.to_numeric(df['Betrag'])

    # Zeit extrahieren
    df['Tag'] = df['Zeitstempel'].dt.date
    df['Woche'] = df['Zeitstempel'].dt.isocalendar().week
    df['Monat'] = df['Zeitstempel'].dt.month
    df['Stunde'] = df['Zeitstempel'].dt.hour

    # spaltennamen von leerzeichen befreien
    df.columns = df.columns.str.strip()
    df['Beschreibung'] = df["Beschreibung"].str.strip()


    return df

def random_datetimes(n=100, days=240):
    start = datetime.now() - timedelta(days=days)
    return [
        start + timedelta(seconds=random.randint(0, days * 24 * 60 * 60))
        for _ in range(n)
    ]
    
def create_fake_data(zeilen=400):

    # Fake-Ausgaben, Beträge, Beschreibungen, Zahlungsarten
    AUSGABEN = [
        'Snacks', 'Eis', 'Schokolade', 'Obst', 'Gemüse', 'Frühstück', 'Mittagessen', 
        'Abendessen', 'Fast Food', 'Restaurantbesuch', 'Takeaway', 'Lieferdienst', 
        'Kaffee to go', 'Tee', 'Säfte', 'Wasserflaschen', 'Alkohol', 'Bier', 'Wein', 
        'Cocktails', 'Spirituosen', 'Partyzubehör', 'Geburtstagsgeschenke', 'Weihnachtsgeschenke', 
        'Ostergeschenke', 'Geschenke für Freunde', 'Geschenke für Familie', 'Blumen', 
        'Bücher', 'Magazine', 'Zeitungen', 'eBooks', 'Hörbücher', 'Onlinekurse', 
        'Fortbildungen', 'Seminare', 'Webinare', 'Kurse', 'Workshops', 'Software', 
        'Apps', 'Abos', 'Streaming', 'Netflix', 'Spotify', 'Disney+', 'Amazon Prime', 
        'Fitnessstudio', 'Sportkleidung', 'Sportgeräte', 'Yoga', 'Pilates', 'Kickboxen', 
        'Schwimmen', 'Laufen', 'Radfahren', 'ÖPNV Ticket', 'Taxi', 'Uber', 'Benzin', 
        'Diesel', 'Autowäsche', 'Autoreparatur', 'KFZ Versicherung', 'Haftpflichtversicherung', 
        'Krankenversicherung', 'Zahnversicherung', 'Reiseversicherung', 'Hausratversicherung', 
        'Miete', 'Nebenkosten', 'Strom', 'Wasser', 'Heizung', 'Internet', 'Telefon', 
        'Handy', 'Handyvertrag', 'Laptop', 'PC', 'Monitor', 'Drucker', 'Kopierpapier', 
        'Schreibwaren', 'Büromaterial', 'Möbel', 'Dekoration', 'Lampenzubehör', 'Putzmittel', 
        'Reinigungsservice', 'Haushaltsgeräte', 'Werkzeuge', 'Gartenbedarf', 'Blumenerde', 
        'Pflanzen', 'Tierfutter', 'Tierarzt', 'Haustierbedarf', 'Spielzeug', 'Videospiele', 
        'Kino', 'Konzerte', 'Theater', 'Museumsbesuche', 'Freizeitpark', 'Reisen', 
        'Flüge', 'Hotels', 'Airbnb', 'Camping', 'Zelt', 'Schlafsack', 'Rucksack', 'Tickets',    
        'Geschenk', 'Essen', 'Ladekabel', 'Tanken', 'Miete', 'Strom', 'Wasser', 
        'Internet', 'Handyvertrag', 'Streamingdienste', 'Kleidung', 'Schuhe', 
        'Bücher', 'Kaffee', 'Snacks', 'Fitnessstudio', 'Sportausrüstung', 
        'ÖPNV', 'Taxi', 'Reisen', 'Hotel', 'Flug', 'Restaurant', 'Friseur', 
        'Kosmetik', 'Medikamente', 'Arztbesuch', 'Versicherung', 'Steuern', 
        'Auto Versicherung', 'Autoreparatur', 'Software', 'Laptop', 'PC Zubehör', 
        'Gadgets', 'Hobbybedarf', 'Kino', 'Konzerte', 'Freizeitpark', 'Museumsbesuche', 
        'Gesundheit', 'Zahnarzt', 'Brillen', 'Kontaktlinsen', 'Haushaltsgeräte', 
        'Putzmittel', 'Dekoration', 'Möbel', 'Bürobedarf', 'Werkzeuge', 'Haustierbedarf', 
        'Tierarzt', 'Benzin', 'Parkgebühren', 'Gebühren & Steuern', 'Spenden', 
        'Geschenk für Freunde', 'Partybedarf', 'Essen zum Mitnehmen', 'Lieferdienste', 
        'Snacks für Arbeit', 'Reinigungsservice', 'Handwerker', 'Streaming Equipment', 
        'Kurse & Weiterbildung', 'Apps', 'Software Abos', 'Hardware Zubehör', 'Verpackung', 
        'Post & Versand', 'Bier & Wein', 'Spirituosen', 'Tabak', 'Zubehör fürs Auto', 
        'Autowäsche', 'Batterien', 'Lampenzubehör', 'Büromaterial', 'Fahrkarten', 
        'Tickets für Events', 'Gesundheitskurse', 'Massage', 'Wellness', 'Sportevents'
    ]

    KATEGORIEN = [
    "Alltag & Essen",
    "Freizeit & Soziales",
    "Kleidung & Pflege",
    "Bildung & Entwicklung",
    "Sparen & Rücklagen"
    ]
    BETRAEGE = [round(random.uniform(1, 100), 2) for _ in range(zeilen)]
    ZAHLUNGSARTEN = ['Bar', 'Kreditkarte', 'PayPal', 'Banküberweisung', 'Apple Pay']

    # DataFrame erstellen
    df = pd.DataFrame({
        "Zeitstempel": random_datetimes(zeilen),
        "Kategorie": [random.choice(KATEGORIEN) for _ in range(zeilen)],
        "Betrag": [random.choice(BETRAEGE) for _ in range(zeilen)],
        "Beschreibung": [random.choice(AUSGABEN) for _ in range(zeilen)],
        "Zahlungsart": [random.choice(ZAHLUNGSARTEN) for _ in range(zeilen)]
    })

    return df