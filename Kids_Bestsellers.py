import pandas as pd
import streamlit as st

data_duplicates = pd.read_excel("kids bestsellers2.xlsx")
data_oos = pd.read_excel("kids_oos.xlsx")
supplier_check = pd.read_excel("supplier_check.xlsx")
#suppliers = list(supplier_check.supplier_id)
suppliers_email = list(supplier_check.email)

st.title("Kids Clothing - Trending Products")

#supplier_id_input = int(st.number_input("Enter Supplier ID"))
supplier_email_input = st.text_input("Enter Registered Email ID")

#if supplier_id_input in suppliers:
if supplier_email_input in suppliers_email:
    supplier_id_input = supplier_check[supplier_check.email==supplier_email_input].supplier_id.iloc[0]
    st.write("Supplier id - ",supplier_id_input)
    status = st.radio("Please select", ("Best Sellers","Trending Products - Low Stock"))

    if status == 'Best Sellers':
        category = st.selectbox("Select Category",data_duplicates.sscat.unique())
        date = st.selectbox("Select Month", data_duplicates[data_duplicates.sscat == category].month_name.unique())
        selected_data_duplicates = data_duplicates[(data_duplicates.sscat == category) & (data_duplicates.month_name == date) & 
                        (data_duplicates.supplier_id != supplier_id_input) ]

        images_duplicates = list(selected_data_duplicates.image1)
        caption_duplicates = list(selected_data_duplicates.caption)
        st.image(images_duplicates,width=300,caption=caption_duplicates)

    elif status == 'Trending Products - Low Stock':
        category_oos = st.selectbox("Select Category",data_oos.sscat.unique())
#        date = st.selectbox("Select Month", data_oos[data_oos.sscat == category_oos].month_name.unique())
        selected_data_oos = data_oos[(data_oos.sscat == category_oos) & (data_oos.supplier_id != supplier_id_input) ]

        images_oos = list(selected_data_oos.image1)
        caption_oos = list(selected_data_oos.caption)
        st.image(images_oos,width=300,caption=caption_oos)
        
else:
    st.error("Please check the registered email id")


