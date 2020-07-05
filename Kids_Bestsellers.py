import pandas as pd
import streamlit as st

data = pd.read_excel("C://Users//nikhil.agarwal//Downloads//kids_bestseller.xlsx")
supplier_check = pd.read_excel("C://Users//nikhil.agarwal//Downloads//supplier_check.xlsx")
suppliers = list(supplier_check.supplier_id)

st.title("Kids Clothing Bestsellers")

supplier_id_input = int(st.number_input("Enter Supplier ID"))

if supplier_id_input in suppliers:
    category = st.selectbox("Select Category",data.sscat.unique())
    date = st.selectbox("Select Month", data.month_name.unique())
    selected_data = data[(data.sscat == category) & (data.month_name == date) & (data.supplier_id != supplier_id_input) ]

    images = list(selected_data.image1)
    caption = list(selected_data.caption)
    st.image(images,width=300,caption=caption)
else:
    st.error("Please check the supplier id")



