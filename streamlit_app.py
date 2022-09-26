import streamlit as sl
import pandas as pd
import requests as rq

fruityvice_response = rq.get("https://fruityvice.com/api/fruit/watermelon")
sl.text(fruityvice_response)

my_fruit_list_df = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list_df.sort_values(by=["Fruit"])

# Setting index to allow names in fruit picker
my_fruit_list = my_fruit_list.set_index('Fruit')

# Text 
sl.title('My Parents New Healthy Diner')
sl.header('Breakfast Menu')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinach, and Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')
sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Pick list for fruit smoothie
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Displaying table on the page 
sl.dataframe(fruits_to_show)
