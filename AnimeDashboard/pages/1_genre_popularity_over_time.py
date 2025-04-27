import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📈 Anime Genre Popularity Over Time")
st.markdown("Explore how different anime genres have evolved in popularity over the years.")

df = pd.read_csv("./data/anime_cleaned.csv")
df = df.dropna(subset=['aired_from_year', 'genre'])
df['aired_from_year'] = df['aired_from_year'].astype(int)
df['genre'] = df['genre'].str.split(', ')
df_exploded = df.explode('genre')

min_year, max_year = int(df_exploded['aired_from_year'].min()), int(df_exploded['aired_from_year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))
unique_genres = sorted(df_exploded['genre'].dropna().unique())
selected_genres = st.sidebar.multiselect("Select Genres", unique_genres, default=["Action", "Romance", "Slice of Life"])

filtered = df_exploded[
    (df_exploded['aired_from_year'] >= year_range[0]) &
    (df_exploded['aired_from_year'] <= year_range[1]) &
    (df_exploded['genre'].isin(selected_genres))
]

genre_trend = (
    filtered.groupby(['aired_from_year', 'genre'])['title']
    .count()
    .reset_index()
    .rename(columns={'title': 'count'})
)

st.subheader("📊 Genre Popularity Trends")
fig = px.line(
    genre_trend,
    x='aired_from_year',
    y='count',
    color='genre',
    markers=True,
    labels={'aired_from_year': 'Year', 'count': 'Number of Anime Released'},
    title='Anime Genre Popularity Over Time'
)
fig.update_layout(legend_title_text='Genre', template='plotly_white')
st.plotly_chart(fig, use_container_width=True)

with st.expander("📊 Show Data Table"):
    st.dataframe(genre_trend)
