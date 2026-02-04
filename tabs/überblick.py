from data import load_data, create_fake_data
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from random import choice
import seaborn as sns
import streamlit as st

MONEY_QOUTES = [
    "Jeder Euro ist ein Samen für deine Freiheit.",
    "Impulse verblassen, Ziele bleiben.",
    "Klarheit im Geld bringt Ruhe im Geist.",
    "Automatisch sparen, entspannt gewinnen.",
    "Dein Geld folgt deiner Aufmerksamkeit.",
    "Hürden schützen vor flüchtigen Versuchungen.",
    "Jeder bewusste Euro ist ein Anker.",
    "Vision übertrifft den flüchtigen Glanz.",
    "Investiere in Morgen, nicht im Jetzt gefangen.",
        "Sparen heißt: Dein Konto soll wachsen, nicht dein Stress.",
    "Jeder Euro, den du nicht ausgibst, freut sich heimlich.",
    "Dein Konto liebt dich mehr, wenn du ihm Pausen gönnst.",
    "Jeder Euro, den du behältst, ist ein Mini-Superheld.",
    "Geld, das du siehst, rennt nicht weg – es posiert.",
    "Sparen ist wie Yoga für dein Bankkonto – flexibel bleiben!",
    "Impulse haben kurze Beine, dein Konto lange Arme.",
        "Jeder Euro ist ein Pixel in deinem Lebenskunstwerk.",
    "Sparen ist wie Origami – falte dein Geld in Form.",
    "Dein Konto kann fliegen, wenn du die Fesseln löst.",
    "Impulse sind Wolken, Ziele der blaue Himmel.",
    "Jedes bewusste Ausgeben ist ein kleiner Zaubertrick.",
    "Dein Geld erzählt Geschichten – lass es episch werden.",
    "Sparen ist wie Schach: ein Zug heute, ein Sieg morgen.",
    "Jeder Euro ist ein kleiner Stern in deinem Finanz-Universum.",
    "Hürden sind magische Portale für kluge Entscheidungen.",
        "Kontrolle beginnt, wo Klarheit wohnt.",
    "Jeder bewusste Euro zeigt deine Stärke.",
    "Du bist Architekt deiner Mittel, nicht Sklave der Versuchung.",
    "Dein Konto folgt deinem Willen, nicht deinen Impulsen.",
    "Sparen ist ein Ausdruck deiner Selbstachtung.",
    "Du bestimmst, wohin dein Geld fließt.",
    "Jede Entscheidung stärkt deine finanzielle Identität.",
    "Du bist nicht Opfer deiner Wünsche, du bist ihr Kapitän.",
    "Selbstkontrolle ist ein Zeichen deiner Freiheit, nicht Verzicht."
]

ZAHL_ZU_MONAT = {
    1: "Januar",
    2: "Februar",
    3: "März",
    4: "April",
    5: "Mai",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Dezember"
}

MONAT_ZU_ZAHL = {value: key for key, value in ZAHL_ZU_MONAT.items()}

def previous_period(df, start, end):
    delta = end - start
    prev_end = start
    prev_start = start - delta

    mask = (df["Zeitstempel"] >= prev_start) & (df["Zeitstempel"] < prev_end)
    return df[mask]

def period_label(df):
    if df is None or df.empty:
        return "kein Zeitraum" 
    
    start = df["Zeitstempel"].min()
    end = df["Zeitstempel"].max()

    days = (end - start).days + 1

    if days < 40:
        return f"{days} Tage"
    else:
        months = round(days / 30)
        return f"{months} Monate"
    
def plot_period_compare(df_view, df_prev):
    cur = df_view.groupby("Kategorie")["Betrag"].sum()
    prev = df_prev.groupby("Kategorie")["Betrag"].sum()

    if (df_view is None or df_view.empty) and (df_prev is None or df_prev.empty):
        st.info("Keine Daten im gewählten Zeitraum.")
        return

    comp = pd.concat([cur, prev], axis=1)
    # Zeitraum automatisch benennen
    label_cur = period_label(df_view)
    label_prev = period_label(df_prev)

    comp.columns = [f"Aktuell ({label_cur})", f"Vorher ({label_prev})"]

    comp = comp.fillna(0)

    st.bar_chart(comp, horizontal=True, height=500)

def filter_month(df, zeitstrahl=0):
    now = datetime.now()
    
    monat = (now.month - 1 + zeitstrahl) % 12 + 1
    df = df.loc[df['Zeitstempel'].dt.month == monat]

    return df

def has_expenses_this_month(df):
    df_m = filter_month(df)
    return not df_m.empty

def period_summary(df_view):

    if df_view.empty:
        st.info("Im gewählten Zeitraum gibt es keine Ausgaben.")
        return

    df_view = df_view.sort_values("Betrag", ascending=False)

    total = df_view["Betrag"].sum()
    biggest = df_view.iloc[0]

    per_cat = (
        df_view.groupby("Kategorie")["Betrag"]
        .sum()
        .sort_values(ascending=False)
    )

    top_cat = per_cat.index[0]
    top_share = per_cat.iloc[0] / total * 100

    st.markdown(f"""
    Größter Block: **{top_cat} ({top_share:.0f} %)**  
    Teuerste Einzelzahlung: **{biggest['Beschreibung']} ({biggest['Betrag']:.2f} €)**  
    Tanken: **({total_gas_expense(df_view):.2f} €)**  
    """)


# Wo dein Geld wirklich hingeht
def plot_categories(df):
    now = datetime.now()

    # df gruppiert nach monat und sortiert absteigend nach ausgaben
    df = (
        df.groupby('Kategorie', as_index=False)['Betrag']
        .sum()
        .sort_values(by='Betrag', ascending=False)
    )

    if df.empty:
        st.markdown('In diesem Zeitraum hast du keine Ausgaben eingetragen.')
        st.empty
        return

	# Berechne den kumulierten Prozentanteil
    total = df['Betrag'].sum()
    df['cum_percent'] = df['Betrag'].cumsum() / total * 100

    # Finde die erste spalte, mit kommulierter Wahrscheinlichkeit über 70 %
    spalte = df.loc[df['cum_percent'] >= 70].iloc[[0]]

    # Finde den index dieser spalte
    index = spalte.index[0]
    # Kleinste Anzahl an Kategrien mit kommulierter Wahrscheinlichkeit über 70 %
    anzahl = int(index + 1)
    # Anteil an Gesamtausgaben
    anteil = df.iloc[index]["cum_percent"]

	# --** Klassifizierung **--

    top1 = df.iloc[0]["Betrag"] / total * 100
    top3 = df.iloc[:3]["Betrag"].sum() / total * 100

    if top1 >= 60:
        text = (
            f'Deine Ausgaben sind diesen Zeitraum extrem konzentriert. '
            f'Eine einzige Kategorie schluckt {top1:.1f} % des Budgets. '
            f'Das ist ein klarer Hebel, falls du sparen willst.'
        )

    elif top1 >= 45:
        text = (
            f'Deine Ausgaben sind deutlich konzentriert. '
            f'Die größte Kategorie macht {top1:.1f} % aus und prägt den Zeitraum spürbar.'
        )

    elif top3 >= 70:
        text = (
            f'Deine Ausgaben sind moderat gebündelt. '
            f'Drei Kategorien vereinen zusammen {top3:.1f} % deiner Ausgaben. '
            f'Der Rest verteilt sich vergleichsweise ruhig.'
        )

    else:
        text = (
            f'Deine Ausgaben sind diesen Zeitraum recht ausgewogen. '
            f'Keine einzelne Kategorie dominiert, Entscheidungen verteilen sich breit.'
        )

    st.markdown(text)

    st.header(f'{ZAHL_ZU_MONAT[now.month]} {now.year}')
    st.bar_chart(
        df,
        x='Kategorie',
        y='Betrag',
        x_label='Betrag (€)',
        horizontal=True,
        height=350
    )

# Datum des vergangenen Monats ermitteln
def date_last_month(df):
    now = datetime.now()
    
    if now.month == 1:
        p_month = 12 
        p_m_year = now.year - 1 
    else:
        p_month = now.month - 1 
        p_m_year = now.year

    return p_month, p_m_year

# Ist ein Monatsvergleich sinnvoll
def abweichungen(df):
    now = datetime.now()
    p_month, p_m_year = date_last_month(df)

    df_t_m = df.loc[(df['Zeitstempel'].dt.month == now.month) & (df['Zeitstempel'].dt.year == now.year)].groupby('Kategorie', as_index=False)['Betrag'].sum()
    df_p_m = df.loc[(df['Zeitstempel'].dt.month == p_month) & (df['Zeitstempel'].dt.year == p_m_year)].groupby('Kategorie', as_index=False)['Betrag'].sum()

    # Index setzen und fehlende Kategorien auffüllen
    df_t_m = df_t_m.set_index('Kategorie')
    df_p_m = df_p_m.set_index('Kategorie')
    categories = df_t_m.index.union(df_p_m.index)
    df_t_m = df_t_m.reindex(categories, fill_value=0)
    df_p_m = df_p_m.reindex(categories, fill_value=0)

    abweichungen_dict = {}
    for cat in categories:
        value_t_m = df_t_m.at[cat, 'Betrag']
        value_p_m = df_p_m.at[cat, 'Betrag']
        abw = (value_t_m - value_p_m) / value_p_m * 100 if value_p_m > 0 else None
        status = "neu" if value_p_m == 0 and value_t_m > 0 else ("irrelevant" if value_p_m == 0 else "ok")
        abweichungen_dict[cat] = {"status": status, "abweichung": abw}

    # Relevant ab einer Abweichung von 10%
    relevant = any(abw["abweichung"] is not None and abw["abweichung"] > 10 for abw in abweichungen_dict.values())
    
    if relevant:
        big_abw, categorie = 0, None
        for cat, abw in abweichungen_dict.items():
            if abw["abweichung"] is not None and abw["abweichung"] > big_abw:
                big_abw, categorie = abw["abweichung"], cat
        st.markdown(f'Im Vergleich zum Vormonat hast du {big_abw:.0f} % mehr für {categorie} ausgegeben.')
    
    return abweichungen_dict

# Lineplot: Monatliche gesamtausgaben 
def plot_gesamt(df):
    # df mit monat und den Gesamtausgaben 
    gesamt_pro_monat = df.groupby('Monat', as_index=False)['Betrag'].sum()
    
    fig, ax = plt.subplots(figsize=(9, 4))

    sns.lineplot(
        gesamt_pro_monat,
        x='Monat',
        y='Betrag'
    )
    plt.ylabel('Total (€)')

    st.pyplot(fig)

# Top-5 Einzeltransaktionen
def top_ten(df):
    st.markdown('Einzelausgaben sagen oft mehr über Impulse als Kategorien.')

    top5_einzel = df.sort_values(by='Betrag', ascending=False).head(5)

    st.bar_chart(
        top5_einzel,
        x='Beschreibung',
        y='Betrag',
        x_label='Betrag (€)',
        y_label='',
        height=300,
        horizontal=True,
        sort=False
    )

    st.write('Diese Ausgaben sind keine Fehler – sie sind Hinweise.')

# Heatmap dieser Monat 
def plot_heatmap(df):

        # --- Jahr-Monat Spalte erstellen ---
    if not pd.api.types.is_datetime64_any_dtype(df['Zeitstempel']):
        df['Zeitstempel'] = pd.to_datetime(df['Zeitstempel'], format="%d.%m.%Y %H:%M:%S")

    df["Monat & Jahr"] = df["Zeitstempel"].dt.strftime("%m/%Y")  # z.B. 12/2025

    # --- Monatsliste nur aus Daten ---
    monate = df.groupby("Monat & Jahr")["Betrag"].sum().loc[lambda x: x != 0].index.tolist()
    monate = ["Alle anzeigen"] + monate  # explizite Option
    monat = st.selectbox("Monat", monate, index=0)

    # --- Daten filtern ---
    if monat != "Alle anzeigen":
        df_plot = df[df["Monat & Jahr"] == monat]
        titel = f"Ausgaben nach Kategorie – {monat}"
        fig_height = 4
    else:
        df_plot = df
        titel = "Heatmap nach Kategorie"
        fig_height = 6

    # --- Pivot erstellen ---
    pivot = df_plot.pivot_table(
        index="Monat & Jahr",  # eindeutige Jahr-Monat-Kombination
        columns="Kategorie",
        values="Betrag",
        aggfunc="sum"
    )

    # --- Leere Pivot abfangen ---
    pivot = pivot.dropna(how="all")
    if pivot.empty:
        st.info("Für die Auswahl sind keine Ausgaben vorhanden.")
        return

    # Optional: schöne Beschriftung auf Monat + Jahr, z.B. Dez 2025
    pivot.index = pd.to_datetime(pivot.index).strftime("%b %Y")  

    # --- Heatmap plotten ---
    sns.set_context("notebook", font_scale=1.2)
    plt.figure(figsize=(12, fig_height))
    ax = sns.heatmap(
        pivot,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=0,
        cbar_kws={"label": "Summe (€)"},
        annot_kws={"fontsize": 16}
    )

    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        ha="right",
        fontsize=16
    )
    ax.set_yticklabels(
        ax.get_yticklabels(), 
        rotation=0,
        fontsize=14
    )
    ax.set_ylabel("")

    plt.title(titel, fontsize=18)
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()

def show_quote():
    st.markdown("---")
    st.subheader("💡 Gedanke zum Mitnehmen")
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown(
            f'''
            <div style="
                text-align:center; 
                font-size:22px; 
                font-style:italic; 
                color: var(--text-color);
                background-color: var(--secondary-background-color);
                padding: 1em 1.5em;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            ">
                "{choice(MONEY_QOUTES)}"
            </div>
            ''',
            unsafe_allow_html=True
        )
    st.markdown("---\n")

# Style-Funktion 
def highlight_expenses(val):
    highlight_color = "rgba(255, 158, 158, 0.4)"  # Pastell-Rot
    try:
        # Betrag extrahieren
        num = float(str(val).replace(" €",""))
        return f"background-color: {highlight_color}" if num > st.session_state.mark else ""
    except:
        return ""
    
def zeitraum(df: pd.DataFrame):
    if df.empty:
        st.warning("Keine Daten vorhanden.")
        return df, df

    df = df.copy()
    df["Zeitstempel"] = pd.to_datetime(df["Zeitstempel"])

    min_date = df["Zeitstempel"].min()
    max_date = df["Zeitstempel"].max()

    # ---------- Monat bestimmen (failsafe) ----------
    month_df = filter_month(df)

    if month_df.empty:
        month_df = filter_month(df, -1)

    if month_df.empty:
        month_df = df  # letzter fallback: alle Daten

    cur_month_dt1 = month_df["Zeitstempel"].min()

    cur_month = ZAHL_ZU_MONAT[cur_month_dt1.month]
    cur_year = cur_month_dt1.year

    # ---------- Date Input robust ----------
    default_start = cur_month_dt1.date()
    default_end = max_date.date()

    start_date, end_date = st.date_input(
        "**🔭 Zeitraum**",
        value=(default_start, default_end),
        format="DD.MM.YYYY"
    )

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    if start > end:
        start, end = end, start  # automatisch korrigieren statt crashen

    st.caption(f"Ausgewählt: {start:%d.%m} – {end:%d.%m.%Y}")

    # ---------- Filter ----------
    mask = df["Zeitstempel"].between(start, end)
    df_view = df.loc[mask]

    df_prev = previous_period(df, start, end)

    return df_view, df_prev

def calc_kpis(df):
    kpis = {}

    total = df['Betrag'].sum()
    kpis['total'] = total

    if df.empty:
        kpis['avg_day'] = 0
        return kpis

    # Zeitraum bestimmen
    days = (df['Zeitstempel'].max() - df['Zeitstempel'].min()).days + 1

    kpis['avg_day'] = total / days if days > 0 else 0

    return kpis

def total_gas_expense(df):
    # Tank ausgaben herausfiltern
    mask = df['Beschreibung'].str.contains('tanken', case=False, na=False) 
    tank_df = df[mask] 

    if tank_df.empty:
        return 0
    else:
        total = tank_df['Betrag'].sum()
        return total

def render(df):

    # Zeitraum festlegen
    st.title('💵 Ausgaben')

    try: 
        df_view, df_prev = zeitraum(df)

    except ValueError:
        df_view, df_prev = filter_month(df), filter_month(df, -1)


    # KPIs Anzeigen
    KPIs = calc_kpis(df_view)

    col1, col2, col3 = st.columns(3)

    col1.metric("Gesamt", f"{KPIs['total']:.2f} €")
    col2.metric("Ø pro Tag", f"{KPIs['avg_day']:.2f} €")
    col3.metric("Transaktionen", len(df_view))


    # --- größter Kostenblock & teuerste Ausg. ---
    with st.container():
        st.subheader("📌 Zusammenfassung")
        period_summary(df_view)


    st.markdown("---")


    # --- Wo dein Geld wirklich hingeht ---
    with st.container():
        st.subheader("📊 Ausgaben nach Kategorie")
        plot_categories(df_view)
        st.markdown("Konzentrierte Ausgaben zeigen, wo du sparen könntest.")

    st.markdown("---")

    # --- Vergleich zum Vormonat (nur wenn relevant) ---
    with st.container():
        st.markdown("""
            #### 💡 Vergleicht deinen aktuellen Zeitraum mit dem direkt davor. 
            So erkennst du, welche Kategorien wachsen oder schrumpfen."""
            )

        plot_period_compare(df_view, df_prev)

    st.markdown("---")

    # --- Top 5 Einzelausgaben ---
    with st.container():
        st.subheader("🏆 Top Einzelausgaben")
        top_ten(df_view)

    st.markdown("---")

    # --- Heatmap als Rückblick ---
    with st.container():
        st.subheader("🌡️ Rückblick: Heatmap aller Ausgaben")
        st.markdown(
            "Über mehrere Monate betrachtet zeigen sich Muster – unabhängig von einzelnen Ausreißern."
        )
        plot_heatmap(df)

# # # --- Optional: Verlauf der Monatsausgaben ---
#     if len(df['Monat'].unique()) > 1:
#         st.markdown("---")
#         with st.container():
#             st.subheader("")
#             st.markdown('')

#             st.subheader("📉 Verlauf deiner Monatsausgaben")
#             plot_gesamt(df)

    # --- Inspirierendes Zitat ---
    show_quote()