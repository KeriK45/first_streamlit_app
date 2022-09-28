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
  return fruityvice_normalized
  
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

# Snowflake connection
sl.header("View Our Fruit List - Add Your Favorites!")
# related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

# Button to load the fruit
if sl.button('Get Fruit List'): 
  my_cnx = sc.connect(**sl.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  sl.dataframe(my_data_rows)

# Allow user to add fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list values ('" + new_fruit +"')")
    return "Thanks for adding " + new_fruit

add_my_fruit = sl.text_input('What fruit would you like to add?')
if sl.button('Add a Fruit to the List'):
  my_cnx = sc.connect(**sl.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  sl.text(back_from_function)

