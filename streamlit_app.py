import streamlit as st
import pandas as pd
import plotly.express as px 
import numpy as np

st.set_page_config( 
    page_title="Covid-tracker", 
    layout="wide" )

DATA_URL = ('https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv')


st.title("Covid Tracker Dashboard")

st.markdown("""
    Bienvenue sur mon dashboard Covid Tracker !
    
    Source des données disponible au lien : [Data covid-19](https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country)
""")

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data['dateRep'] = pd.to_datetime(data['dateRep'])
    data.loc[data['cases'] < 0, 'cases'] = 0
    data['cumulated_cases'] = data.sort_values('dateRep')['cases'].cumsum()
    data['average_cases'] = data['cases'].rolling(window=7).mean()
    data['average_deaths'] = data['deaths'].rolling(window=7).mean()
    return data


data_load_state = st.text('Chargement des données en cours...')
data = load_data(28729)
data_load_state.text("Ci-dessous les données Covid-19")

if st.checkbox('Afficher les données'):
    st.subheader('Données brutes')
    st.write(data)

date_update = data['dateRep'].max().strftime('%d/%m/%Y')
st.text(f'Date dernier update des données : {date_update}')

st.header('Analyse dans le monde')
st.subheader('Cumul du nombre de cas')

fig = px.line(data.sort_values('dateRep'), x = 'dateRep', y = 'cumulated_cases')
fig.update_traces(fill='tozeroy')  
st.plotly_chart(fig, use_container_width=True)

st.subheader('Nouveaux cas')
fig2 = px.line(data.groupby('dateRep')[['cases', 'average_cases']].sum().sort_values('dateRep'), y = ['cases', 'average_cases'])
st.plotly_chart(fig2, use_container_width=True)


st.header('Analyse par pays')

country = st.selectbox("Selectionner un pays", data["countriesAndTerritories"].sort_values().unique(), index = 9)
country_filter = data[data['countriesAndTerritories'] == country]

# Calculate the average number of cases today and yesterday
average_cases_today = country_filter.groupby('dateRep')['cases'].sum()[-1]
average_cases_yesterday = country_filter.groupby('dateRep')['cases'].sum()[-2]
average_cases_before_yesterday = country_filter.groupby('dateRep')['cases'].sum()[-3]
growth_rate = np.round(average_cases_today / average_cases_yesterday, 3)
growth_rate_yesterday = np.round(average_cases_yesterday / average_cases_before_yesterday, 3)


date_country_update = country_filter['dateRep'].max().strftime('%d/%m/%Y')
st.text(f'Date dernier update du pays selectionné : {date_country_update}')

st.metric(f'Taux de croissance actuel en {country}', value = f'{growth_rate}', delta = f'{np.round(growth_rate - growth_rate_yesterday, 3)}')

st.markdown("""
    Le taux de croissance compare le nombre moyen de cas d'aujourd'hui au nombre moyen de cas d'hier. Si le taux de croissance est > 1, le virus se propage. Si le taux de croissance est inférieur à 1, la propagation ralentit.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader(f'Nouveaux cas en {country}')
    fig3 = px.line(country_filter.groupby('dateRep')[['cases', 'average_cases']].sum(), y = ['cases', 'average_cases'])
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader(f'Morts en {country}')
    fig4 = px.line(country_filter.groupby('dateRep')[['deaths', 'average_deaths']].sum(), y = ['deaths', 'average_deaths'])
    st.plotly_chart(fig4, use_container_width=True)