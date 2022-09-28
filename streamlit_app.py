import streamlit as sl
import pandas as pd
import requests as rq
import snowflake.connector as sc
from urllib.error import URLError

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

# Function for fruit choice
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruitvice_normalized
  
# Section for displaying fruityvice api response
sl.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = sl.text_input('What fruit would you like information about?')
  if not fruit_choice:
    sl.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)    
    sl.dataframe(back_from_function)
except URLError as e:
  sl.error()

# temporary
sl.stop()

# Snowflake connection
my_cnx = sc.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
sl.header("The fruit load list contains: ")
sl.dataframe(my_data_row)

# Section for adding fruit
add_my_fruit = sl.text_input('What fruit would you like to add?')
sl.write('Thanks for adding ', add_my_fruit)
