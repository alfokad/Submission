import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("dashboard/data.csv")

# Define functions for analysis
def max_products(df):
    sum_products = df["product_category_name"].value_counts().head()
    return sum_products

def min_products(df):
    sum_products = df["product_category_name"].value_counts().tail(5).sort_values()
    return sum_products

def top_payment_types(df):
    sum_payment_type = df["payment_type"].value_counts().head(3)
    return sum_payment_type

def order_status_counts(df):
    sum_status = df["order_status"].value_counts()
    return sum_status

def delivered_count(df):
    delivered_df = df[df["order_status"] == "delivered"]
    return delivered_df.shape[0]

def total_orders(df):
    total_orders_count = df["order_status"].count()
    return total_orders_count

def other_statuses_count(df):
    other_count = total_orders(df) - delivered_count(df)
    return other_count

def top_cities(df):
    top_cities_df = df[df["order_status"] == "delivered"]["customer_city"].value_counts().head()
    return top_cities_df

# Streamlit App
st.title('Proyek Analisis Data: E-Commerce Public Dataset')

# Sidebar for data selection
selected_analysis = st.sidebar.selectbox('Select Analysis', 
                                         ['Top 5 Most Ordered Products', 
                                          'Top 5 Least Ordered Products', 
                                          'Top 3 Most Used Payment Types',
                                          'Order Status Comparison',
                                          'Top 5 City with the Most Delivered Status'])

# Main content based on selected analysis
if selected_analysis == 'Top 5 Most Ordered Products':
    st.header('Top 5 Most Ordered Products')
    
    sum_products = max_products(df)
    sum_products_df = pd.DataFrame({
        'Product Name': sum_products.index,
        'Total': sum_products.values
    })
    st.table(sum_products_df)

    colors_top = ['navy' if prod == sum_products.idxmax() else 'skyblue' for prod in sum_products.index]

    # Bar plot
    plt.figure(figsize=(12, 6))
    max_plot = sum_products.plot(kind='bar', color=colors_top)
    for bar in max_plot.patches:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{int(bar.get_height())}', ha='center', va='bottom')
    plt.title('Top 5 Most Ordered Products')
    plt.xlabel('Product Name')
    plt.ylabel('Total')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

elif selected_analysis == 'Top 5 Least Ordered Products':
    st.header('Top 5 Least Ordered Products')
    
    sum_products = min_products(df)
    sum_products_df = pd.DataFrame({
        'Product Name': sum_products.index,
        'Total': sum_products.values
    })
    st.table(sum_products_df)
    
    colors_bottom = ['grey' if prod == sum_products.idxmin() else 'lightgrey' for prod in sum_products.index]

    # Bar plot
    plt.figure(figsize=(12, 6))
    min_plot = sum_products.plot(kind='bar', color=colors_bottom)
    for bar in min_plot.patches:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{int(bar.get_height())}', ha='center', va='bottom')
    plt.title('Top 5 Least Ordered Products')
    plt.xlabel('Product Name')
    plt.ylabel('Total')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

elif selected_analysis == 'Top 3 Most Used Payment Types':
    st.header('Top 3 Most Used Payment Types')
    
    sum_payment_type = top_payment_types(df)
    sum_payment_type_df = pd.DataFrame({
        'Payment Type': sum_payment_type.index,
        'Total': sum_payment_type.values
    })
    st.table(sum_payment_type_df)
    
    colors = ['navy' if prod == sum_payment_type.idxmax() else 'grey' for prod in sum_payment_type.index]

    # Pie chart
    plt.figure(figsize=(6,5))
    payment_top = sum_payment_type.plot(kind='bar', color=colors)
    for bar in payment_top.patches:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{int(bar.get_height())}', ha='center', va='bottom')
    plt.title('Top 3 Most Used Payment Types')
    plt.xlabel('Payment Type')
    plt.ylabel('Total')
    st.pyplot(plt)

elif selected_analysis == 'Order Status Comparison':
    st.header('Order Status Comparison')
    
    sum_status = order_status_counts(df)
    sum_status_df = pd.DataFrame({
        'Order Status': sum_status.index,
        'Total': sum_status.values
    })
    st.table(sum_status_df)
    
    colors = ['navy' if prod == sum_status.idxmax() else 'grey' for prod in sum_status.index]
    delivered_orders = delivered_count(df)
    other_orders = other_statuses_count(df)

    # Bar plot
    plt.figure(figsize=(8,5))
    status_plot = sum_status.plot(kind='bar', color=colors)
    for bar in status_plot.patches:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{int(bar.get_height())}', ha='center', va='bottom')
    plt.title('Order Status Comparison')
    plt.xlabel('Order Status')
    plt.ylabel('Total')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

    # Pie chart
    statuses = ['Delivered', 'Other']
    counts = [delivered_orders, other_orders]
    plt.figure(figsize=(5,4))
    plt.pie(counts, labels=statuses, autopct='%1.2f%%', explode=[0.3, 0.5], colors=sns.color_palette('Set2'))
    plt.title('Order Status Comparison: Delivered vs. Others', fontsize=16)
    st.pyplot(plt)

elif selected_analysis == 'Top 5 City with the Most Delivered Status':
    st.header('Top 5 City with the Most Delivered Status')
    
    top_cities = top_cities(df).sort_values(ascending=True)
    top_cities_df = pd.DataFrame({
        'City':top_cities.index,
        'Total': top_cities.values
    })
    st.table(top_cities_df)
    
    # Bar plot
    plt.figure(figsize=(15, 8))
    city_plot = top_cities.plot(kind='barh', color=['blue' if city == top_cities.idxmax() else 'grey' for city in top_cities.index])
    for bar in city_plot.patches:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{int(bar.get_width())}', va='center')
    plt.title('Top 5 City with the Most Delivered Status')
    plt.xlabel('Total')
    plt.ylabel('City')
    plt.tight_layout()
    st.pyplot(plt)
