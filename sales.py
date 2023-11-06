# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['text.usetex'] = False

# %%
sales=pd.read_csv(r'sales_data_sample.csv', encoding='unicode_escape')

# %%
sales.head(4)

# %%
sales.info()

# %%
sales.columns=sales.columns.str.lower()

# %%
sales.drop(['addressline2', 'territory', 'postalcode'], axis=1, inplace=True)

# %%
pd.set_option('display.max_columns', 21)

# %%
sales.rename(columns={'month_id':'month','qtr_id':'qtr','year_id': 'year'}, inplace=True)

# %%
sales['sales']=sales['quantityordered']*sales['priceeach']

# %%
"""
### 1. Sales analysis
"""

# %%
"""
#### Change in sales value over time
"""

# %%
sales['orderdate']=pd.to_datetime(sales['orderdate'])

# %%
sales['month_year']=sales['month'].astype(str)+'.'+ sales['year'].astype(str)

# %%
sales_per_orderdate=sales.groupby('month_year')['sales'].sum().reset_index()

# %%
sorted_sale=sales_per_orderdate.sort_values(by='month_year', key=lambda x: pd.to_datetime(x, format='%m.%Y')).reset_index()

# %%
plt.figure(figsize=(10, 6))
sns.lineplot(data=sorted_sale, x='month_year', y='sales')
plt.xticks(rotation=90)
plt.xlabel('Month and year')
plt.ylabel('Sales in $')
plt.title('Sales over Time')
plt.grid(True)
plt.legend(title=None)  # Atur legend menjadi None untuk menghilangkannya

plt.show()

# %%
"""
#### Sales value per month and per quarter
"""

# %%
sales_per_month=sales.groupby('month')['sales'].sum()

# %%
df3=sales_per_month.reset_index()

plt.figure(figsize=(10, 4))
sns.barplot(data=df3, x='month', y='sales', palette='RdPu')
plt.xlabel('Month')
plt.ylabel('Sales value ($)')
plt.title('Sales per month')
plt.xticks(range(len(df3)), df3['month'])
plt.legend(title=None)  # Atur legend menjadi None untuk menghilangkannya

plt.show()

# %%
sales_per_qtr=sales.groupby('qtr')['sales'].sum()

# %%
df4=sales_per_qtr.reset_index()

plt.figure(figsize=(8, 3))
sns.barplot(data=df4, x='qtr', y='sales', palette='RdPu')
plt.xlabel('Quarter')
plt.ylabel('Sales value ($)')
plt.title('Sales per quarter')
plt.xticks(range(len(df4)), df4['qtr'], rotation=0, ha='right')
plt.legend(title=None)  # Atur legend menjadi None untuk menghilangkannya

plt.show()

# %%
"""
#### Sales for various categories of products
"""

# %%
total_sale=sales.groupby('productline')['sales'].sum().sort_values(ascending=True)

# %%
df8=total_sale.reset_index()

sns.barplot(data=df8, x=total_sale.values,y='productline', palette='RdPu')
plt.xlabel('Sale value (in $)')
plt.title('Sale value per product line')
plt.legend(title=None)  # Atur legend menjadi None untuk menghilangkannya

plt.show()

# %%
"""
#### Sales in individual countries
"""

# %%
sales_by_country=sales.groupby(['country'])['sales'].sum()

# %%
sorted_sales_by_country=sales_by_country.sort_values(ascending=True)

# %%
sns.barplot(x=sorted_sales_by_country.values, y=sorted_sales_by_country.index, palette='RdPu')
plt.xlabel('in $')
plt.ylabel('Country')
plt.title('Sales per country')
plt.legend(title=None)  # Atur legend menjadi None untuk menghilangkannya

plt.show()

# %%
"""
## Order analysis
"""

# %%
"""
#### Order value per month and quarter
"""

# %%
unique_orders=sales.drop_duplicates('ordernumber')
orders_per_month=unique_orders.groupby('month')['ordernumber'].count()

# %%
df = orders_per_month.reset_index()

plt.figure(figsize=(10, 4))
sns.barplot(data=df, x='month', y='ordernumber', palette='RdPu')
plt.xlabel('Month')
plt.ylabel('Number of orders')
plt.title('Orders per month')
plt.xticks(range(len(df)), df['month'], rotation=0, ha='right')
plt.legend(title=None)  # Atur legend menjadi None untuk menghilangkannya

plt.show()

# %%
orders_per_qtr=unique_orders.groupby('qtr')['ordernumber'].count()

# %%
df2 = orders_per_qtr.reset_index()

plt.figure(figsize=(8, 3))
sns.barplot(data=df2, x='qtr', y='ordernumber', palette='RdPu')
plt.xlabel('Quarter')
plt.ylabel('Number of Orders')
plt.title('Orders per quarter')
plt.xticks(range(len(df2)), df2['qtr'], rotation=0, ha='right')
plt.legend(title=None)  # Atur legend menjadi None untuk menghilangkannya

plt.show()

# %%
"""
#### Order statuses
"""

# %%
status_count=unique_orders.groupby(['status'])['orderlinenumber'].count()
status_percentages=(status_count/status_count.sum())*100
print(status_percentages)

# %%
#Analysis of remaining statuses - other than 'Shipped'

# %%
is_same_status=sales.groupby('ordernumber')['status'].nunique()==1

# %%
if is_same_status.all():
    print("For each order, every position has the same status.")
else:
    print("For some orders, different positions have a different satuses")

# %%
other_status=unique_orders[unique_orders['status']!='Shipped']
other_status_count=other_status.groupby(['status'])['orderlinenumber'].count()
other_status_perc=(other_status_count/other_status_count.sum())*100

# %%
other_status_perc

# %%
df6=pd.DataFrame({'Other statuses': other_status_perc.index, 'Percentage Share': other_status_perc.values})

colors = plt.cm.Set3(range(len(df6['Other statuses'])))

plt.figure(figsize=(6, 4))
plt.pie(df6['Percentage Share'], labels=df6['Other statuses'], autopct='%.1f%%', colors=colors)
plt.title('Order statuses different than "Shipped"')
plt.legend(title=None)  # Atur legend menjadi None untuk menghilangkannya

plt.show()

# %%
"""
## Product analysis
"""

# %%
"""
#### Analysis of average prices for different product categories
"""

# %%
product_line_mean=sales.groupby('productline')['priceeach'].mean()

# %%
product_line_mean

# %%
df7=product_line_mean.reset_index()
sns.catplot(data=df7, y='productline', x=product_line_mean.values, color='Purple')
plt.title('Avegare price for each product line')
plt.xlabel('Average price')
plt.legend(title=None)  # Atur legend menjadi None untuk menghilangkannya

plt.show()

# %%
