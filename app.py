import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

df = pd.read_csv("superstore_data.csv")
df.columns = df.columns.str.strip().str.lower()
df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month_name()
df["year_month"] = df["order_date"].dt.to_period("M")

st.title("Superstore Sales Dashboard")

region_filter = st.sidebar.multiselect("Select Region", df["region"].unique(), default=df["region"].unique())
category_filter = st.sidebar.multiselect("Select Category", df["category"].unique(), default=df["category"].unique())

filtered_df = df[(df["region"].isin(region_filter)) & (df["category"].isin(category_filter))]

total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_quantity = filtered_df["quantity"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Quantity", f"{total_quantity}")
col4.metric("Profit Margin", f"{profit_margin:.2f}%")

st.subheader("Sales by Category")
sales_category = filtered_df.groupby("category")["sales"].sum().sort_values(ascending=False)
fig1, ax1 = plt.subplots()
ax1.bar(sales_category.index, sales_category.values)
ax1.set_xlabel("Category")
ax1.set_ylabel("Sales")
ax1.set_title("Sales by Category")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Sales by Region")
sales_region = filtered_df.groupby("region")["sales"].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots()
ax2.bar(sales_region.index, sales_region.values)
ax2.set_xlabel("Region")
ax2.set_ylabel("Sales")
ax2.set_title("Sales by Region")
st.pyplot(fig2)

st.subheader("Monthly Sales Trend")
monthly_sales = filtered_df.groupby("year_month")["sales"].sum()
fig3, ax3 = plt.subplots()
ax3.plot(monthly_sales.index.astype(str), monthly_sales.values)
ax3.set_xlabel("Month")
ax3.set_ylabel("Sales")
ax3.set_title("Monthly Sales Trend")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.subheader("Top 3 Customers by Sales")
top_customers = filtered_df.groupby("customer_name")["sales"].sum().sort_values(ascending=False).head(3)
st.dataframe(top_customers)

st.subheader("Correlation Matrix")
corr = filtered_df[["sales", "profit", "quantity"]].corr()
st.dataframe(corr)

st.subheader("Sales vs Profit Scatter Plot")
fig4, ax4 = plt.subplots()
ax4.scatter(filtered_df["sales"], filtered_df["profit"])
ax4.set_xlabel("Sales")
ax4.set_ylabel("Profit")
ax4.set_title("Sales vs Profit")
st.pyplot(fig4)
