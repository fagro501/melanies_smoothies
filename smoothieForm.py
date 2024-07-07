# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
# st.text(fruityvice_response)
# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose your fruits
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"), col("search_on"))
pd_df = my_dataframe.toPandas()
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop();
ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe, 
                                 max_selections = 5)


name_on_order = st.text_input("Name on the Smoothie")
if ingredients_list:
    ingredients_string = ""
    for fruit in ingredients_list:
        ingredients_string+=fruit + " "
        st.subheader(fruit + " Nutrition Information")
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
        # st.stop()
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+name_on_order, icon="✅")
        
        
