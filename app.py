import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient

# Title
st.title("IMDb Top Movies Analysis")

# Load pre-saved data
@st.cache_data
def load_data():
    return pd.read_csv('moviesCleaned.csv')

df = load_data()

# Convert columns to numeric
df['Fan Rating'] = pd.to_numeric(df['Fan Rating'], errors='coerce')
df['Release Year'] = pd.to_numeric(df['Release Year'], errors='coerce')

# Show raw data
if st.checkbox("Show raw data"):
    st.dataframe(df)

# Filters
year = st.selectbox("Select a Year", sorted(df['Release Year'].unique()))
pg13_df = df[df['Age Rating'] == 'PG-13']
year_df = df[df['Release Year'] == year]

st.subheader(f"Movies Released in {year}")
st.dataframe(year_df)

st.subheader("PG-13 Movies")
st.dataframe(pg13_df)

# Statistics
st.subheader("Statistics Summary")
st.write(df.describe())

# Visualizations
st.subheader("Visualizations")

tab1, tab2, tab3, tab4 = st.tabs(["Trend by Year", "Trend by Age Rating", "Heatmap", "Boxplot"])

with tab1:
    trend = df.groupby('Release Year')['Fan Rating'].mean()
    st.line_chart(trend)

with tab2:
    trend = df.groupby('Age Rating')['Fan Rating'].mean()
    st.bar_chart(trend)

with tab3:
    st.write("Correlation Heatmap")
    sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, cmap='coolwarm')
    st.pyplot(plt.gcf())

with tab4:
    st.write("Fan Rating Distribution by Age Rating")
    sns.boxplot(data=df, x='Age Rating', y='Fan Rating', palette='Set3')
    st.pyplot(plt.gcf())

# Upload to MongoDB
st.subheader("Upload to MongoDB")

if st.button("Upload cleaned data to MongoDB"):
    try:
        uri = "mongodb+srv://ahmedtheeditor:eZWM3zA9bqiDd6bo@toolscluster.mom07ap.mongodb.net/?retryWrites=true&w=majority&appName=toolsCluster"
        client = MongoClient(uri)
        db = client['imdb_data']
        collection = db['top_movies']

        # Optional: Clear existing data to avoid duplicates
        # collection.delete_many({})

        collection.insert_many(df.to_dict(orient='records'))
        st.success("Data uploaded to MongoDB successfully!")

    except Exception as e:
        st.error(f"MongoDB upload failed: {e}")