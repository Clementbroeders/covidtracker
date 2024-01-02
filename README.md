# Covidtracker dashboard

## Streamlit Covid Tracker

Vous pouvez accéder au dashboard Covid Tracker à partir du lien suivant : [https://covidtracker.streamlit.app/](https://covidtracker.streamlit.app/)


## Docker (local)

Pour lancer le docker en local, utiliser les commandes suivantes :

> Création de l'image
```
docker build -t covidtracker-streamlit .
```

> Run le container
```
docker run -it -p 8501:8501 -e PORT=8501 streamlit
```