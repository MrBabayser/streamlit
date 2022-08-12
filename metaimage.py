# *****************************************************************************************************
# Nom ......... : metaimage.py
# Rôle ........ : affiche et modifie les métadonnées d'une image
# Auteur ...... : Georges Miot
# Version ..... : V0.1 du 12/08/2022
# Licence ..... : réalisé dans le cadre du cours de OC
# Usage : Pour exécuter : streamlit run https://github.com/MrBabayser/streamlit.git/metaimage.py
#******************************************************************************************************/
 
import streamlit as st
from exif import Image
from PIL import Image as img
  
photo = 'Georges.jpg'
image = img.open(photo)
st.image(image, caption='Georges') # affiche l'image avec un titre

# ouvre l'image
with open(photo, 'rb') as image_file:
  my_image = Image(image_file)
  
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
