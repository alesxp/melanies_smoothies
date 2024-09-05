# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize Your Application!")
st.write(
    """Choose the frt in your smoth - custom!"""
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your order will be:", name_on_order)

cnx = st.connection("Snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to five:'
    , my_dataframe
    , max_selections = 5
    )

ingredients_string = ''
my_insert_stmt = ''

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    

    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '

    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""

st.write(my_insert_stmt)
time_to_insert = st.button('Submit order')
# st.stop

if time_to_insert:
# if ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


