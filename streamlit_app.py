import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

# Set the title of the web application
streamlit.title('My Parents New Healthy Dinner')

# Display header and some text for breakfast favorites
streamlit.header('Breakfast Favorites')
streamlit.text('  🥣  Omega 3 & Blueberry Oatmeal')
streamlit.text('  🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('  🐔 Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')

# Display header and options for building a fruit smoothie
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# Create repeatable code block (function) to fetch data from fruityvice API
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New section to display API response from fruityvice API
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

# Error handling for URL issues
except URLError as e:
  streamlit.error("Error: {e.reason}")

# Import snowflake.connector
#import snowflake.connector

# New section to display the fruit load list from Snowflake
streamlit.header("The fruit Load List contains:")

# Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
       my_cur.execute("select * from fruit_load_list")
       return my_cur.fetchall()




# Allow the end user to enter fruit to the list
# Function to insert a new fruit into the fruit_load_list table in Snowflake
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list VALUES ('" + new_fruit + "')")
    my_cnx.commit()
    return "Thanks for adding " + new_fruit

#add button to load the fruit
if streamlit.button('Get fruit list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows=get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)
  




# add button to add fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add')
if streamlit.button('Add a fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function= insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)





