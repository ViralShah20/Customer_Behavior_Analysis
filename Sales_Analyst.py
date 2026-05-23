import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv(r"D:\VIRAL\POWER\POWER BI\Sales Analyst\customer_shopping_behavior.csv")

# print(df.head())
#print(df.describe(include='all'))

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

labels = ['Young Adult','Adult','Middle-aged','Senior']
df['age_group'] = pd.qcut(df['age'],q=4,labels=labels)

#print(df[['age','age_group']].head(10))

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
df[['purchase_frequency_days','frequency_of_purchases']].head(10)



df[['discount_applied','promo_code_used']].head(10)
(df['discount_applied'] == df['promo_code_used']).all()
df = df.drop('promo_code_used', axis=1)
#print(df.columns)

import pandas as pd
from sqlalchemy import create_engine

# Read CSV File
df = pd.read_csv(
    r"D:\VIRAL\POWER\POWER BI\Sales Analyst\customer_shopping_behavior.csv"
)

# ---------------- DATA CLEANING ---------------- #

# Fill missing review ratings with median by category
df['Review Rating'] = df.groupby('Category')['Review Rating'] \
    .transform(lambda x: x.fillna(x.median()))

# Convert column names to lowercase
df.columns = df.columns.str.lower()

# Replace spaces with underscore
df.columns = df.columns.str.replace(' ', '_')

# Rename purchase amount column
df = df.rename(
    columns={'purchase_amount_(usd)': 'purchase_amount'}
)

# Create Age Group Column
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']

df['age_group'] = pd.qcut(
    df['age'],
    q=4,
    labels=labels
)

# Convert purchase frequency into days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = \
    df['frequency_of_purchases'].map(frequency_mapping)

# Drop unnecessary column
df = df.drop('promo_code_used', axis=1)

# Display cleaned columns
print(df.columns)

# ---------------- MYSQL CONNECTION ---------------- #

username = "root"
password = "root"
host = "localhost"
port = "3306"
database = "customer_behaviour"

# Create Engine
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# ---------------- UPLOAD DATA TO MYSQL ---------------- #

table_name = "customer"

df.to_sql(
    table_name,
    engine,
    if_exists="replace",
    index=False
)

print("Table created successfully!")

# ---------------- READ DATA FROM MYSQL ---------------- #

result = pd.read_sql(
    "SELECT * FROM customer LIMIT 5;",
    engine
)

print(result)

# ---------------- SAMPLE SQL QUERY ---------------- #

query = """
SELECT 
    category,
    AVG(purchase_amount) AS avg_purchase
FROM customer
GROUP BY category
"""

avg_result = pd.read_sql(query, engine)

print(avg_result)