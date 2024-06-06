import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
alpha = pd.read_csv('Alpha.csv')

# Data cleaning and preprocessing
drop_list = ['product_keywords', 'usually_ships_within', 'product_id', 'product_description', 
             'seller_products_sold', 'seller_id', 'seller_username', 'seller_community_rank', 
             'product_name', 'reserved', 'in_stock', 'should_be_gone', 'brand_id', 'brand_url', 
             'seller_badge', 'seller_price', 'has_cross_border_fees', 'buyers_fees', 
             'seller_num_products_listed', 'seller_num_followers', 'product_like_count', 
             'seller_pass_rate']
alpha = alpha.drop(drop_list, axis=1)
alpha = alpha.drop('product_condition', axis=1)
alpha = alpha.dropna(axis=0)

def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR)))]
    return df

alpha = remove_outliers(alpha, 'price_usd')
alpha['sold'] = alpha['sold'].astype(int)
alpha['available'] = alpha['available'].astype(int)

st.title('Data Analysis of Alpha Dataset')

# Trend Analysis
st.subheader('Top 5 Brands Analysis')
brand_counts = alpha['brand_name'].value_counts()
top_5_brands = brand_counts.head(5)
fig = px.bar(top_5_brands, x=top_5_brands.index, y=top_5_brands.values, labels={'x': 'Brand', 'y': 'Count'})
fig.update_layout(title='Top 5 Brands Analysis', xaxis_title='Brand', yaxis_title='Count')
st.plotly_chart(fig)

st.subheader('Purchases by Gender')
gender_counts = alpha['product_gender_target'].value_counts()
fig = px.pie(names=gender_counts.index, values=gender_counts.values, title='Purchases by Gender')
st.plotly_chart(fig)

st.subheader('Purchases by Product Category')
category_counts = alpha['product_category'].value_counts()

men_categories = category_counts[category_counts.index.str.startswith('Men')]
women_categories = category_counts[category_counts.index.str.startswith('Women')]

fig = px.bar(men_categories, x=men_categories.index, y=men_categories.values, title='Purchases by Men Product Categories')
st.plotly_chart(fig)

fig = px.bar(women_categories, x=women_categories.index, y=women_categories.values, title='Purchases by Women Product Categories')
st.plotly_chart(fig)

most_demanded_men = men_categories.idxmax()
most_demanded_women = women_categories.idxmax()
overall_most_demanded = category_counts.idxmax()

st.write(f"The most demanded product category for Men is: {most_demanded_men}")
st.write(f"The most demanded product category for Women is: {most_demanded_women}")
st.write(f"The overall most demanded product category is: {overall_most_demanded}")

st.subheader('Profit Analysis')
alpha['profit'] = alpha['price_usd'] - alpha['seller_earning']
total_profit_by_category = alpha.groupby('product_category')['profit'].sum()

fig = px.bar(total_profit_by_category, x=total_profit_by_category.index, y=total_profit_by_category.values, title='Total Profit by Product Category')
st.plotly_chart(fig)

st.subheader('Top 3 Most Demanded Product Materials and Colors')
top_materials = alpha['product_material'].value_counts().nlargest(3)
top_colors = alpha['product_color'].value_counts().nlargest(3)

fig = px.bar(top_materials, x=top_materials.index, y=top_materials.values, title='Top 3 Most Demanded Product Materials')
st.plotly_chart(fig)

fig = px.bar(top_colors, x=top_colors.index, y=top_colors.values, title='Top 3 Most Demanded Product Colors')
st.plotly_chart(fig)

most_demanded_material = top_materials.idxmax()
most_demanded_color = top_colors.idxmax()

st.write(f"The most demanded product material is: {most_demanded_material}")
st.write(f"The most demanded product color is: {most_demanded_color}")

st.subheader('Geographical Analysis')
top_warehouses = alpha['warehouse_name'].value_counts().nlargest(3)
top_countries = alpha['seller_country'].value_counts().nlargest(3)

fig = px.bar(top_warehouses, x=top_warehouses.index, y=top_warehouses.values, title='Top 3 Most Active Warehouses')
st.plotly_chart(fig)

fig = px.bar(top_countries, x=top_countries.index, y=top_countries.values, title='Top 3 Most Active Seller Countries')
st.plotly_chart(fig)

st.write("Conclusions:")
for warehouse in top_warehouses.index:
    country = alpha.loc[alpha['warehouse_name'] == warehouse, 'seller_country'].iloc[0]
    st.write(f"The top 3 most active warehouse {warehouse} is in {country}.")
st.write(f"The top 3 most active seller countries are: {', '.join(top_countries.index)}")

