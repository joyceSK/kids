import pandas as pd
import streamlit as st
from datetime import timedelta

#data_duplicates = pd.read_excel("kids bestsellers2.xlsx")
#data_oos = pd.read_excel("kids_oos.xlsx")
supplier_check = pd.read_excel("supplier_check.xlsx")

#Inventory projection data import
@st.cache
def load_order_data():
    df = pd.read_excel("orders.xlsx")
    return df

data_projection = load_order_data()
#data_projection = pd.read_excel("orders.xlsx")
projection_summary = pd.read_excel("summary.xlsx")
data_inv = pd.read_excel("inventory.xlsx")

#suppliers = list(supplier_check.supplier_id)
suppliers_email = list(supplier_check.email)

st.title("Kids Clothing - Trending Products and Inventory Projections")

#supplier_id_input = int(st.number_input("Enter Supplier ID"))
supplier_email_input = st.text_input("Enter Registered Email ID")

#if supplier_id_input in suppliers:
if supplier_email_input in suppliers_email:
    supplier_id_input = supplier_check[supplier_check.email==supplier_email_input].supplier_id.iloc[0]
    st.write("Supplier id - ",supplier_id_input)
#    status = st.radio("Please select", ("Inventory Projection"))

    data_projection_sup = data_projection[data_projection.supplier_id == supplier_id_input]
    projection_summary_sup = projection_summary[projection_summary.supplier_id == supplier_id_input].drop('supplier_id',axis=1)
    data_inv_sup = data_inv[data_inv.supplier_id == supplier_id_input]
    #Getting per day sale
    d_30 = data_projection_sup.order_date.max().date() - timedelta(30)
    d_15 = data_projection_sup.order_date.max().date() - timedelta(15)
    d_7 = data_projection_sup.order_date.max().date() - timedelta(7)
    d_3 = data_projection_sup.order_date.max().date() - timedelta(3)

    d_30_order = data_projection_sup[data_projection_sup.order_date > pd.Timestamp(d_30)].groupby(['product_id','variation']).agg(d_30=('orders','sum'))/30
    d_15_order = data_projection_sup[data_projection_sup.order_date > pd.Timestamp(d_15)].groupby(['product_id','variation']).agg(d_15=('orders','sum'))/15
    d_7_order = data_projection_sup[data_projection_sup.order_date > pd.Timestamp(d_7)].groupby(['product_id','variation']).agg(d_7=('orders','sum'))/7
    d_3_order = data_projection_sup[data_projection_sup.order_date > pd.Timestamp(d_3)].groupby(['product_id','variation']).agg(d_3=('orders','sum'))/3

    df_perdaysale = projection_summary_sup[['product_id','variation']].merge(d_30_order,on=['product_id','variation'],how='left').merge(d_15_order,on=['product_id','variation'],how='left').merge(d_7_order,on=['product_id','variation'],how='left').merge(d_3_order,on=['product_id','variation'],how='left')
    df_perdaysale['per_day_sale'] = round(df_perdaysale[['d_30','d_15','d_7','d_3']].apply(pd.to_numeric,errors='coerce'),0).fillna(0).max(axis=1)


    #perdaysale = round(data_projection_sup.groupby(['product_id','variation']).orders.sum()/data_projection_sup.groupby(['product_id','variation']).order_date.count(),0)
    #df_perdaysale = perdaysale.reset_index(name='per_day_sale')
    #Merging Live inventory
    projection_temp1 = projection_summary_sup.merge(data_inv_sup[['product_id','variation','live_inventory']],on=['product_id','variation'],how='left')
    projection_final = projection_temp1.merge(df_perdaysale[['product_id','variation','per_day_sale']], on=['product_id','variation'],how='left')
    #DOH
    projection_final['days_on_hand'] = round(projection_final.live_inventory/projection_final.per_day_sale,1)
    #Additional Inv Required
    
    projection_final['Additional_inventory_needed'] = round((30 - projection_final.days_on_hand) * projection_final.per_day_sale,0)

    projection_final.fillna("",inplace=True)
    #selecting 80% oc pids
    selected_pid = ((data_projection_sup.groupby(['product_id']).orders.sum().sort_values(ascending=False)*100/data_projection_sup.orders.sum()).cumsum() <80)
    pid_80_oc = list(selected_pid[selected_pid].index)
    for pid in pid_80_oc:
        st.write(projection_final[projection_final.product_id == pid])

# ################### Showing all radio buttons 
#     status = st.radio("Please select", ("Best Sellers","Trending Products - Low Stock","Inventory Projection"))


#     if status == 'Best Sellers':
#         category = st.selectbox("Select Category",data_duplicates.sscat.unique())
#         date = st.selectbox("Select Month", data_duplicates[data_duplicates.sscat == category].month_name.unique())
#         selected_data_duplicates = data_duplicates[(data_duplicates.sscat == category) & (data_duplicates.month_name == date) & 
#                         (data_duplicates.supplier_id != supplier_id_input) ]

#         images_duplicates = list(selected_data_duplicates.image1)
#         caption_duplicates = list(selected_data_duplicates.caption)
#         st.image(images_duplicates,width=300,caption=caption_duplicates)

#     elif status == 'Trending Products - Low Stock':
#         category_oos = st.selectbox("Select Category",data_oos.sscat.unique())
# #        date = st.selectbox("Select Month", data_oos[data_oos.sscat == category_oos].month_name.unique())
#         selected_data_oos = data_oos[(data_oos.sscat == category_oos) & (data_oos.supplier_id != supplier_id_input) ]

#         images_oos = list(selected_data_oos.image1)
#         caption_oos = list(selected_data_oos.caption)
#         st.image(images_oos,width=300,caption=caption_oos)
#     elif status == 'Inventory Projection':
#         data_projection_sup = data_projection[data_projection.supplier_id == supplier_id_input]
#         projection_summary_sup = projection_summary[projection_summary.supplier_id == supplier_id_input].drop('supplier_id',axis=1)
#         data_inv_sup = data_inv[data_inv.supplier_id == supplier_id_input]
#         #Getting per day sale
#         d_30 = data_projection_sup.order_date.max().date() - timedelta(30)
#         d_15 = data_projection_sup.order_date.max().date() - timedelta(15)
#         d_7 = data_projection_sup.order_date.max().date() - timedelta(7)
#         d_3 = data_projection_sup.order_date.max().date() - timedelta(3)

#         d_30_order = data_projection_sup[data_projection_sup.order_date > pd.Timestamp(d_30)].groupby(['product_id','variation']).agg(d_30=('orders','sum'))/30
#         d_15_order = data_projection_sup[data_projection_sup.order_date > pd.Timestamp(d_15)].groupby(['product_id','variation']).agg(d_15=('orders','sum'))/15
#         d_7_order = data_projection_sup[data_projection_sup.order_date > pd.Timestamp(d_7)].groupby(['product_id','variation']).agg(d_7=('orders','sum'))/7
#         d_3_order = data_projection_sup[data_projection_sup.order_date > pd.Timestamp(d_3)].groupby(['product_id','variation']).agg(d_3=('orders','sum'))/3

#         df_perdaysale = projection_summary_sup[['product_id','variation']].merge(d_30_order,on=['product_id','variation'],how='left').merge(d_15_order,on=['product_id','variation'],how='left').merge(d_7_order,on=['product_id','variation'],how='left').merge(d_3_order,on=['product_id','variation'],how='left')
#         df_perdaysale['per_day_sale'] = round(df_perdaysale[['d_30','d_15','d_7','d_3']].apply(pd.to_numeric,errors='coerce'),0).fillna(0).max(axis=1)


#         #perdaysale = round(data_projection_sup.groupby(['product_id','variation']).orders.sum()/data_projection_sup.groupby(['product_id','variation']).order_date.count(),0)
#         #df_perdaysale = perdaysale.reset_index(name='per_day_sale')
#         #Merging Live inventory
#         projection_temp1 = projection_summary_sup.merge(data_inv_sup[['product_id','variation','live_inventory']],on=['product_id','variation'],how='left')
#         projection_final = projection_temp1.merge(df_perdaysale[['product_id','variation','per_day_sale']], on=['product_id','variation'],how='left')
#         #DOH
#         projection_final['days_on_hand'] = round(projection_final.live_inventory/projection_final.per_day_sale,1)
#         #Additional Inv Required
        
#         projection_final['Additional_inventory_needed'] = round((30 - projection_final.days_on_hand) * projection_final.per_day_sale,0)

#         projection_final.fillna("",inplace=True)
#         #selecting 80% oc pids
#         selected_pid = ((data_projection_sup.groupby(['product_id']).orders.sum().sort_values(ascending=False)*100/data_projection_sup.orders.sum()).cumsum() <80)
#         pid_80_oc = list(selected_pid[selected_pid].index)
#         for pid in pid_80_oc:
#             st.write(projection_final[projection_final.product_id == pid])

# ################### end showing all radio buttons        
        
else:
    st.error("Please check the registered email id")


