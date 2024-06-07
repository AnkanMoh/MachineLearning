import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
alpha = pd.read_csv('/Users/Ankan/OneDrive/Desktop/Alpha.csv')

# Data Cleaning
drop_list = [
    'product_keywords', 'usually_ships_within', 'product_id', 'product_description',
    'seller_products_sold', 'seller_id', 'seller_username', 'seller_community_rank',
    'product_name', 'reserved', 'in_stock', 'should_be_gone', 'brand_id', 'brand_url',
    'seller_badge', 'seller_price', 'has_cross_border_fees', 'buyers_fees',
    'seller_num_products_listed', 'seller_num_followers', 'product_like_count', 'seller_pass_rate'
]
alpha = alpha.drop(drop_list, axis=1)
alpha = alpha.drop('product_condition', axis=1)
alpha = alpha.dropna(axis=0)

# Convert data types
alpha['sold'] = alpha['sold'].astype(int)
alpha['available'] = alpha['available'].astype(int)

# Remove outliers
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR)))]
    return df

alpha = remove_outliers(alpha, 'price_usd')

# Add new columns for analysis
alpha['gender_category'] = alpha['product_category'].str.split().str[0]
alpha['profit'] = alpha['price_usd'] - alpha['seller_earning']

# Streamlit app
st.set_page_config(page_title='Project Alpha', page_icon=':bar_chart:', layout='wide')

# Custom CSS for black background and section separation
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #FFFFFF;
    }
    .main > div {
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Project Alpha')

st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ['Overview', 'Trend Analysis', 'Geographical Analysis', 'Profit Analysis'])

# Define the Spring Pastels palette
spring_pastels = sns.color_palette("pastel")

if options == 'Overview':
    st.header('Overview')
    st.write(alpha.describe())

elif options == 'Trend Analysis':
    st.header('Trend Analysis')

    # Top 5 Brands Analysis
    st.subheader('Top 5 Brands Analysis')
    brand_counts = alpha['brand_name'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=brand_counts.index, y=brand_counts.values, ax=ax, palette=spring_pastels)
    ax.set_title('Top 5 Brands Analysis')
    ax.set_xlabel('Brand')
    ax.set_ylabel('Count')
    st.pyplot(fig)
    st.write("---")

    # Purchases by Gender
    st.subheader('Purchases by Gender')
    gender_counts = alpha['product_gender_target'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=gender_counts.index, y=gender_counts.values, ax=ax, palette=spring_pastels)
    ax.set_title('Purchases by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Number of Purchases')
    st.pyplot(fig)
    st.write("---")

    # Product Categories Analysis
    st.subheader('Product Categories Analysis')
    category_counts = alpha['product_category'].value_counts()

    # Men's Category Analysis
    st.subheader("Men's Category Analysis")
    men_categories = category_counts[category_counts.index.str.startswith('Men')]
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=men_categories.index, y=men_categories.values, ax=ax, palette=spring_pastels)
    ax.set_title('Purchases by Men Product Categories')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Number of Purchases')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
    st.write("---")

    # Women's Category Analysis
    st.subheader("Women's Category Analysis")
    women_categories = category_counts[category_counts.index.str.startswith('Women')]
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=women_categories.index, y=women_categories.values, ax=ax, palette=spring_pastels)
    ax.set_title('Purchases by Women Product Categories')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Number of Purchases')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
    st.write("---")

    # Most Demanded Categories
    st.subheader('Most Demanded Categories')
    most_demanded_men = men_categories.idxmax()
    most_demanded_women = women_categories.idxmax()
    overall_most_demanded = category_counts.idxmax()
    st.write(f"The most demanded product category for Men is: {most_demanded_men}")
    st.write(f"The most demanded product category for Women is: {most_demanded_women}")
    st.write(f"The overall most demanded product category is: {overall_most_demanded}")
    st.write("---")

    # Top Product Materials and Colors
    st.subheader('Top Product Materials and Colors')

    # Top 3 Most Demanded Product Materials
    top_materials = alpha['product_material'].value_counts().nlargest(3)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_materials.index, y=top_materials.values, ax=ax, palette=spring_pastels)
    ax.set_title('Top 3 Most Demanded Product Materials')
    ax.set_xlabel('Product Material')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
    st.write("---")

    # Top 3 Most Demanded Product Colors
    top_colors = alpha['product_color'].value_counts().nlargest(3)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_colors.index, y=top_colors.values, ax=ax, palette=['#ff9999', '#66b3ff', '#99ff99'])
    ax.set_title('Top 3 Most Demanded Product Colors')
    ax.set_xlabel('Product Color')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
    st.write("---")

    most_demanded_material = top_materials.idxmax()
    most_demanded_color = top_colors.idxmax()
    st.write(f"The most demanded product material is: {most_demanded_material}")
    st.write(f"The most demanded product color is: {most_demanded_color}")

elif options == 'Profit Analysis':
    st.header('Profit Analysis')

    # Total Profit by Product Category
    st.subheader('Total Profit by Product Category')
    total_profit_by_category = alpha.groupby('product_category')['profit'].sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=total_profit_by_category.index, y=total_profit_by_category.values, ax=ax, palette=spring_pastels)
    ax.set_title('Total Profit by Product Category')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Total Profit (USD)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
    st.write("---")

    # Profit Table by Category
    pivot_table = alpha.pivot_table(index='product_category', columns='gender_category', values='profit', aggfunc='sum', fill_value=0)
    most_profitable_men_category = pivot_table['Men'].idxmax()
    most_profitable_women_category = pivot_table['Women'].idxmax()
    max_profit_category = total_profit_by_category.idxmax()
    st.write("Profit Table by Category:")
    st.write(pivot_table)
    st.write(f"The most profitable category for men is: {most_profitable_men_category}")
    st.write(f"The most profitable category for women is: {most_profitable_women_category}")
    st.write(f"The product category that gives maximum profit is: {max_profit_category}")

elif options == 'Geographical Analysis':
    st.header('Geographical Analysis')

    # Top 3 Most Active Warehouses
    st.subheader('Top 3 Most Active Warehouses')
    top_warehouses = alpha['warehouse_name'].value_counts().nlargest(3)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_warehouses.index, y=top_warehouses.values, ax=ax, palette=spring_pastels)
    ax.set_title('Top 3 Most Active Warehouses')
    ax.set_xlabel('Warehouse Name')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
    st.write("---")

    # Top 3 Most Active Seller Countries
    st.subheader('Top 3 Most Active Seller Countries')
    top_countries = alpha['seller_country'].value_counts().nlargest(3)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_countries.index, y=top_countries.values, ax=ax, palette=spring_pastels)
    ax.set_title('Top 3 Most Active Seller Countries')
    ax.set_xlabel('Country')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
    st.write("---")

    # Conclusions
    st.subheader('Conclusions')
    for warehouse in top_warehouses.index:
        country = alpha.loc[alpha['warehouse_name'] == warehouse, 'seller_country'].iloc[0]
        st.write(f"The top 3 most active warehouse {warehouse} in {country}.")
    st.write(f"The top 3 most active seller countries are: {', '.join(top_countries.index)}")
