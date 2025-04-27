import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📅 Seasonal Release Patterns of Anime")
st.markdown("Analyze anime release trends, scores, and popularity based on seasons.")

df = pd.read_csv("./data/anime_cleaned.csv")
df = df.dropna(subset=['premiered'])
df[['season', 'season_year']] = df['premiered'].str.split(' ', expand=True)
df = df.dropna(subset=['season_year'])
df['season_year'] = df['season_year'].astype(int)

min_year = int(df['season_year'].min())
max_year = int(df['season_year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))
seasons = ['Winter', 'Spring', 'Summer', 'Fall']
selected_seasons = st.sidebar.multiselect("Select Seasons", seasons, default=seasons)

filtered_df = df[
    (df['season_year'] >= year_range[0]) &
    (df['season_year'] <= year_range[1]) &
    (df['season'].isin(selected_seasons))
]

release_trend = (
    filtered_df.groupby(['season_year', 'season'])['title']
    .count()
    .reset_index()
    .rename(columns={'title': 'anime_count'})
)

st.subheader("Anime Releases by Season Over Time")
fig1 = px.line(
    release_trend,
    x='season_year',
    y='anime_count',
    color='season',
    markers=True,
    labels={'season_year': 'Year', 'anime_count': 'Anime Count'},
    title="Number of Anime Released Per Season"
)
fig1.update_layout(template='plotly_white')
st.plotly_chart(fig1, use_container_width=True)

avg_score = (
    filtered_df.groupby('season')['score']
    .mean()
    .reset_index()
    .sort_values(by='score', ascending=False)
)
st.subheader("⭐ Average Anime Score by Season")
fig2 = px.bar(
    avg_score,
    x='season',
    y='score',
    color='season',
    labels={'score': 'Average Score'},
    title="Average Anime Score (Filtered)"
)
fig2.update_layout(template='plotly_white', showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

avg_popularity = (
    filtered_df.groupby('season')['popularity']
    .mean()
    .reset_index()
    .sort_values(by='popularity')
)
st.subheader("Average Popularity Rank by Season (Lower is Better)")
fig3 = px.bar(
    avg_popularity,
    x='season',
    y='popularity',
    color='season',
    labels={'popularity': 'Popularity Rank'},
    title="Average Popularity Rank (Filtered)"
)
fig3.update_layout(template='plotly_white', showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

with st.expander("🔍 View Filtered Data"):
    st.dataframe(filtered_df[['title', 'season', 'season_year', 'score', 'popularity']])
