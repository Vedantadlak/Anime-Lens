import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Anime EDA Dashboard", layout="wide")
st.title("📊 Anime Episode Analysis Dashboard")

df_anime = pd.read_csv("./data/anime_cleaned.csv")
df_anime['episodes'] = pd.to_numeric(df_anime['episodes'], errors='coerce')
df_anime['popularity'] = pd.to_numeric(df_anime['popularity'], errors='coerce')
df_anime['score'] = pd.to_numeric(df_anime['score'], errors='coerce')

df_pop = df_anime.dropna(subset=['episodes', 'popularity'])
df_rating = df_anime.dropna(subset=['episodes', 'score'])

st.subheader("📈 Episode Count vs Popularity")
fig1 = px.scatter(
    df_pop, x='episodes', y='popularity',
    trendline='ols',
    color='episodes',
    hover_data=['title'],
    labels={'episodes': 'Number of Episodes', 'popularity': 'Popularity'},
    title="Episode Count vs Popularity"
)
fig1.update_layout(template='plotly_white')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("⭐ Episode Count vs Rating")
fig2 = px.scatter(
    df_rating, x='episodes', y='score',
    trendline='ols',
    color='episodes',
    hover_data=['title'],
    labels={'episodes': 'Number of Episodes', 'score': 'Average Rating'},
    title="Episode Count vs Rating"
)
fig2.update_layout(template='plotly_white')
st.plotly_chart(fig2, use_container_width=True)

bins = [0, 12, 24, 50, 200]
labels = ['Short', 'Medium', 'Long', 'Very Long']
df_rating['episode_bin'] = pd.cut(df_rating['episodes'], bins=bins, labels=labels)

st.subheader("📦 Boxplot: Episode Length vs Rating")
fig3 = px.box(
    df_rating, x='episode_bin', y='score', color='episode_bin',
    labels={'episode_bin': 'Episode Length', 'score': 'Average Rating'},
    title="Episode Length vs Rating"
)
fig3.update_layout(template='plotly_white', showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

corr_popularity = df_pop['episodes'].corr(df_pop['popularity'])
corr_rating = df_rating['episodes'].corr(df_rating['score'])

st.subheader("📌 Correlation Insights")
st.markdown(f"- **Correlation between Episode Count and Popularity**: `{corr_popularity:.2f}`")
st.markdown(f"- **Correlation between Episode Count and Rating**: `{corr_rating:.2f}`")
