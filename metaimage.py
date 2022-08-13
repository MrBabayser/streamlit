# *****************************************************************************************************
# Nom ......... : metaimage.py
# Rôle ........ : affiche et modifie les métadonnées d'une image et créer des cartes
# Auteur ...... : Georges Miot
# Version ..... : V0.2 du 13/08/2022
# Licence ..... : réalisé dans le cadre du cours de OC
# Usage : Pour exécuter : streamlit run https://github.com/MrBabayser/streamlit/blob/main/metaimage.py
#******************************************************************************************************/
 
import streamlit as st
from exif import Image
from PIL import Image as img
from streamlit_folium import st_folium
import folium

photo = 'Georges.jpg'

# dictionnaire des voyages et leur localisation
voyages={
  'La Havane': [23.135305, -82.3589631],
  'New-York': [40.7127281, -74.0060152],
  'Dublin': [53.3497645, -6.2602732],
  'Liverpool': [53.4071991, -2.99168],
  'Manchester': [53.4794892, -2.2451148],
  'Barcelone': [41.3828939, 2.1774322],
  'Naples': [40.8358846, 14.2487679],
  'Rome': [41.8933203, 12.4829321],
  'Berlin': [52.5170365, 13.3888599],
  'St-Petersbourg': [59.938732, 30.316229],
  'Novgorod': [58.5209862, 31.2757862],
  'Moscou': [55.7504461, 37.6174943],
  'Oulan-Bator': [47.9184676, 106.9177016],
  'Pékin': [39.906217, 116.3912757]
}

st.title('Image')
image = img.open(photo)
st.image(image, caption='Georges') # affiche l'image

# ouvre l'image
with open(photo, 'rb') as image_file:
  my_image = Image(image_file)
  
st.title('Métadonnées')
datas = my_image.list_all() # liste les métadonnées
  
for data in datas:
  try:
    # conversion de la saisie utilisateur en fonction du type
    if str(type(my_image[data])) == "<class 'str'>":
      rep = str(st.text_input(data, value=my_image[data]))
    elif str(type(my_image[data])) == "<class 'float'>":
      rep = float(st.text_input(data, value=my_image[data]))
    elif str(type(my_image[data])) == "<class 'int'>":
      rep = int(st.text_input(data, value=my_image[data]))
    elif str(type(my_image[data])) == "<class 'tuple'>":
      rep = st.text_input(data, value=my_image[data])
      # recrée un tuple à partir d'un type str de la forme "(23.2,29.2,92.2)"
      rep = tuple(map(float, rep[1:-1].split(',')))
    else:
      # désactive la saisie si autre type
      rep = st.text_input(data, value=my_image[data], disabled=True)
    my_image.set(data, rep) # remplace la métadonnée
  except (ValueError, RuntimeError):
    pass

# enregistre l'image
with open(photo, 'wb') as modified_image_file:
  modified_image_file.write(my_image.get_file())

st.title('Localisation')

# récupère les coordonnées gps
latitude_dms = my_image.get("gps_latitude")
longitude_dms = my_image.get("gps_longitude")

# conversion en degrés décimaux
latitude = latitude_dms[0]+((latitude_dms[1]+(latitude_dms[2]/60))/60)
longitude = longitude_dms[0]+((longitude_dms[1]+(longitude_dms[2]/60))/60)

# charge une carte localisée
map_localisation = folium.Map(location=[latitude, longitude], zoom_start=16)

# crée un marqueur
localisation = folium.Marker(
  [latitude, longitude],
  popup = "JE SUIS LÀ",
  tooltip = "JE SUIS LÀ"
  )

localisation.add_to(map_localisation) # ajoute un marqueur
st_folium(map_localisation, width = 700) # affiche la carte

st.title('Voyages')
map_voyages = folium.Map() # charge une carte du monde
localisation.add_to(map_voyages) # ajoute un marqueur

# ajoute des marqueurs
for voyage in voyages:
  folium.Marker(
    location = voyages[voyage],
    popup = voyage,
    icon=folium.Icon(color="red", icon="info-sign"),
  ).add_to(map_voyages)
  
  
# relie les marqueurs par un trait
folium.PolyLine(
  voyages.values(),
  weight=5,
  color='orange'
  ).add_to(map_voyages)

st_folium(map_voyages, width = 700) # affiche la carte
