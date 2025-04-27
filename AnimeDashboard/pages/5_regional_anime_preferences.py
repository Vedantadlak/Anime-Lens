import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🌍 Regional Anime Preferences", layout="wide")
st.title("📊 Regional Anime Preferences Analysis")

@st.cache_data
def load_data():
    df_users = pd.read_csv("./data/users_cleaned.csv")
    df_anime_lists = pd.read_csv("./data/animelists_cleaned.csv")
    df_anime = pd.read_csv("./data/anime_cleaned.csv")
    return df_users, df_anime_lists, df_anime

df_users, df_anime_lists, df_anime = load_data()

if 'location' in df_users.columns:
    df_users['country'] = df_users['location'].str.extract(r'([A-Za-z\s]+)$')[0]
    df_users['country'] = df_users['country'].fillna('Unknown').str.strip()
else:
    df_users['country'] = 'Unknown'

watchtime_region = df_users.groupby('country')['user_days_spent_watching'].sum().sort_values(ascending=False).head(15)

st.subheader("📺 Total Watch Time by Country")
fig1 = px.bar(
    watchtime_region,
    x=watchtime_region.values,
    y=watchtime_region.index,
    orientation='h',
    labels={'x': 'Total Days Spent Watching Anime', 'y': 'Country'},
    title="Total Days Spent Watching Anime (Top 15 Countries)"
)
fig1.update_layout(template='plotly_white')
st.plotly_chart(fig1, use_container_width=True)

merged = pd.merge(df_anime_lists, df_users[['username', 'country']], on='username', how='left')
merged = pd.merge(merged, df_anime[['anime_id', 'genre']], on='anime_id', how='left')
sample = merged.sample(10000, random_state=42)
sample['genre'] = sample['genre'].fillna('Unknown').str.split(', ')
sample = sample.explode('genre')
genre_region = sample.groupby(['country', 'genre']).size().reset_index(name='count')
top_regions = genre_region.groupby('country')['count'].sum().sort_values(ascending=False).head(10).index
genre_region_top = genre_region[genre_region['country'].isin(top_regions)]
heatmap_data = genre_region_top.pivot_table(index='genre', columns='country', values='count', fill_value=0)

st.subheader("🔥 Genre Popularity Heatmap (Top 10 Countries)")
fig2 = px.imshow(
    heatmap_data,
    labels=dict(x="Country", y="Genre", color="Popularity"),
    aspect="auto",
    title="Genre Popularity by Country"
)
fig2.update_layout(template='plotly_white')
st.plotly_chart(fig2, use_container_width=True)
