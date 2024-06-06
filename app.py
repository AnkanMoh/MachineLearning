import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the data
alpha = pd.read_csv('Alpha.csv')

# Initial Data Information
st.title('E-commerce Data Analysis')
st.header('Initial Data Information')
st.write(alpha.info())
st.write(alpha.describe())
st.write("Number of missing values in each column:")
st.write(alpha.isnull().sum())

# Removing redundant columns
drop_list = ['product_keywords', 'usually_ships_within', 'product_id', 'product_description',
             'seller_products_sold', 'seller_id', 'seller_username', 'seller_community_rank',
             'product_name', 'reserved', 'in_stock', 'should_be_gone', 'brand_id', 'brand_url',
             'seller_badge', 'seller_price', 'has_cross_border_fees', 'buyers_fees', 'seller_num_products_listed',
             'seller_num_followers', 'product_like_count', 'seller_pass_rate']

alpha = alpha.drop(drop_list, axis=1)

# Dropping 'product_condition' and handling missing values
alpha = alpha.drop('product_condition', axis=1)
alpha = alpha.dropna(axis=0)

# Removing outliers from 'price_usd' column
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR)))]
    return df

alpha = remove_outliers(alpha, 'price_usd')

# Converting 'sold' and 'available' columns to integer type
alpha['sold'] = alpha['sold'].astype(int)
alpha['available'] = alpha['available'].astype(int)

# Trend Analysis
st.header('Trend Analysis')
st.subheader('Top 5 Brands Analysis')
brand_counts = alpha['brand_name'].value_counts()
top_5_brands = brand_counts.head(5)

plt.figure(figsize=(12, 8))
sns.barplot(x=top_5_brands.index, y=top_5_brands.values)
plt.title('Top 5 Brands Analysis')
plt.xlabel('Brand')
plt.ylabel('Count')
plt.xticks(rotation=90)
st.pyplot(plt)

# Gender Target Analysis
st.subheader('Purchases by Gender')
gender_counts = alpha['product_gender_target'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].bar(gender_counts.index, gender_counts.values, color=['pink', 'blue'])
axes[0].set_title('Purchases by Gender')
axes[0].set_xlabel('Gender')
axes[0].set_ylabel('Number of Purchases')
axes[0].set_xticks(range(len(gender_counts.index)))
axes[0].set_xticklabels(gender_counts.index, rotation=0)

colors = ['blue' if gender == 'Men' else 'pink' for gender in gender_counts.index]
axes[1].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', startangle=140, colors=colors)
axes[1].set_title('Purchases by Gender')
axes[1].axis('equal')

plt.tight_layout()
st.pyplot(fig)

majority_gender = gender_counts.idxmax()
st.write(f"The majority gender target is: {majority_gender}")

# Category Analysis
st.subheader('Product Category Analysis')
category_counts = alpha['product_category'].value_counts()

# Men's category analysis
st.write("Men's Product Categories")
men_categories = category_counts[category_counts.index.str.startswith('Men')]
plt.figure(figsize=(10, 6))
men_categories.plot(kind='bar', color='blue')
plt.title('Purchases by Men Product Categories')
plt.xlabel('Product Category')
plt.ylabel('Number of Purchases')
plt.xticks(rotation=45)
st.pyplot(plt)

plt.figure(figsize=(8, 8))
plt.pie(men_categories.values, labels=men_categories.index, autopct='%1.1f%%', startangle=140, colors='blue')
plt.title('Purchases by Men Product Categories')
plt.axis('equal')
st.pyplot(plt)

plt.figure(figsize=(10, 6))
men_categories.plot(kind='barh', color='blue')
plt.title('Purchases by Men Product Categories')
plt.xlabel('Number of Purchases')
plt.ylabel('Product Category')
st.pyplot(plt)

# Women's category analysis
st.write("Women's Product Categories")
women_categories = category_counts[category_counts.index.str.startswith('Women')]
plt.figure(figsize=(10, 6))
women_categories.plot(kind='bar', color='pink')
plt.title('Purchases by Women Product Categories')
plt.xlabel('Product Category')
plt.ylabel('Number of Purchases')
plt.xticks(rotation=45)
st.pyplot(plt)

plt.figure(figsize=(8, 8))
plt.pie(women_categories.values, labels=women_categories.index, autopct='%1.1f%%', startangle=140, colors='pink')
plt.title('Purchases by Women Product Categories')
plt.axis('equal')
st.pyplot(plt)

plt.figure(figsize=(10, 6))
women_categories.plot(kind='barh', color='pink')
plt.title('Purchases by Women Product Categories')
plt.xlabel('Number of Purchases')
plt.ylabel('Product Category')
st.pyplot(plt)

most_demanded_men = men_categories.idxmax()
most_demanded_women = women_categories.idxmax()
overall_most_demanded = category_counts.idxmax()
st.write(f"The most demanded product category for Men is: {most_demanded_men}")
st.write(f"The most demanded product category for Women is: {most_demanded_women}")
st.write(f"The overall most demanded product category is: {overall_most_demanded}")

# Season Analysis
alpha['count'] = alpha['product_season'].value_counts()

# Sold and Available Products
sold_and_available = alpha[(alpha['sold'] == 1) & (alpha['available'] == 1)]
sold_but_not_available = alpha[(alpha['sold'] == 1) & (alpha['available'] == 0)]
count_sold_and_available = len(sold_and_available)
count_sold_but_not_available = len(sold_but_not_available)
st.write("Count of products when they are sold and available:", count_sold_and_available)
st.write("Count of products when they are sold but not available:", count_sold_but_not_available)

# Profit Analysis
st.subheader('Profit Analysis')
alpha['gender_category'] = alpha['product_category'].str.split().str[0]
alpha['profit'] = alpha['price_usd'] - alpha['seller_earning']
total_profit_by_category = alpha.groupby('product_category')['profit'].sum()
pivot_table = alpha.pivot_table(index='product_category', columns='gender_category', values='profit', aggfunc='sum', fill_value=0)

most_profitable_men_category = pivot_table['Men'].idxmax()
most_profitable_women_category = pivot_table['Women'].idxmax()

plt.figure(figsize=(10, 6))
sns.barplot(x=total_profit_by_category.index, y=total_profit_by_category.values, palette='husl')
plt.title('Total Profit by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Profit (USD)')
plt.xticks(rotation=45)
st.pyplot(plt)

st.write("Profit Table by Category:")
st.write(pivot_table)
st.write(f"The most profitable category for men is: {most_profitable_men_category}")
st.write(f"The most profitable category for women is: {most_profitable_women_category}")
max_profit_category = total_profit_by_category.idxmax()
st.write(f"The product category that gives maximum profit is: {max_profit_category}")

# Material and Color Analysis
st.subheader('Material and Color Analysis')
top_materials = alpha['product_material'].value_counts().nlargest(3)
plt.figure(figsize=(10, 6))
top_materials.plot(kind='bar', color='lightcoral')
plt.title('Top 3 Most Demanded Product Materials')
plt.xlabel('Product Material')
plt.ylabel('Count')
plt.xticks(rotation=45)
st.pyplot(plt)

top_colors = alpha['product_color'].value_counts().nlargest(3)
plt.figure(figsize=(10, 6))
top_colors.plot(kind='bar', color=['black', 'blue', 'grey'])
plt.title('Top 3 Most Demanded Product Colors')
plt.xlabel('Product Color')
plt.ylabel('Count')
plt.xticks(rotation=45)
st.pyplot(plt)

most_demanded_material = top_materials.idxmax()
most_demanded_color = top_colors.idxmax()
st.write(f"The most demanded product material is: {most_demanded_material}")
st.write(f"The most demanded product color is: {most_demanded_color}")

# Geographical Analysis
st.subheader('Geographical Analysis')
top_warehouses = alpha['warehouse_name'].value_counts().nlargest(3)
plt.figure(figsize=(10, 6))
top_warehouses.plot(kind='bar', color='skyblue')
plt.title('Top 3 Most Active Warehouses')
plt.xlabel('Warehouse Name')
plt.ylabel('Count')
plt.xticks(rotation=45)
st.pyplot(plt)

top_countries = alpha['seller_country'].value_counts().nlargest(3)
plt.figure(figsize=(10, 6))
top_countries.plot(kind='bar', color='lightgreen')
plt.title('Top 3 Most Active Seller Countries')
plt.xlabel('Country')
plt.ylabel('Count')
plt.xticks(rotation=45)
st.pyplot(plt)

st.write("Conclusions:")
for warehouse in top_warehouses.index:
    country = alpha.loc[alpha['warehouse_name'] == warehouse, 'seller_country'].iloc[0]
    st.write(f"The top 3 most active warehouse {warehouse} is in {country}.")
st.write(f"The top 3 most active seller countries are: {', '.join(top_countries.index)}")

