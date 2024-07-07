# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose your fruits
    """
)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe, 
                                 max_selections = 5)
name_on_order = st.text_input("Name on the Smoothie")
if ingredients_list:
    ingredients_string = ""
    for fruit in ingredients_list:
        ingredients_string+=fruit + " "
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
        # st.stop()
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+name_on_order, icon="✅")
        