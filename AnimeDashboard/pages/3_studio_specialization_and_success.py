import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🎥 Anime Studio Insights Dashboard")

df_anime = pd.read_csv("./data/anime_cleaned.csv")
df_genre_studio = df_anime[['studio', 'genre']].dropna()
df_genre_studio['genre'] = df_genre_studio['genre'].str.split(',')
df_genre_studio = df_genre_studio.explode('genre')
df_genre_studio['genre'] = df_genre_studio['genre'].str.strip()
df_genre_studio['studio'] = df_genre_studio['studio'].str.strip()
studio_genre_counts = df_genre_studio.groupby(['genre', 'studio']).size().reset_index(name='count')

st.header("🏆 Top Studios by Genre")
top_n = st.slider("Select Top N Studios per Genre", 1, 10, 3)
genres = st.multiselect("Pick genres to show:", sorted(studio_genre_counts['genre'].unique()), default=['Action', 'Romance', 'Comedy'])
top_studios_by_genre = studio_genre_counts.sort_values(['genre', 'count'], ascending=[True, False])
top_studios = top_studios_by_genre.groupby('genre').head(top_n)
filtered = top_studios[top_studios['genre'].isin(genres)]

fig = px.bar(
    filtered,
    x='count',
    y='studio',
    color='genre',
    facet_col='genre',
    orientation='h',
    title="Top Studios by Genre",
    labels={'count': 'Anime Count', 'studio': 'Studio'}
)
fig.update_layout(template='plotly_white', showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.header("🔥 Heatmap: Anime Counts by Studio and Genre")
heatmap_data = studio_genre_counts.pivot(index='studio', columns='genre', values='count').fillna(0)
top_heatmap_studios = heatmap_data.sum(axis=1).sort_values(ascending=False).head(10).index
heatmap_data = heatmap_data.loc[top_heatmap_studios]

fig_heatmap = go.Figure(
    data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlGnBu'
    )
)
fig_heatmap.update_layout(
    title="Top 10 Studios: Genre Spread",
    xaxis_title="Genre",
    yaxis_title="Studio",
    template='plotly_white'
)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.header("🌞 Sunburst & Treemap Visualizations")
sunburst_df = studio_genre_counts[studio_genre_counts['count'] > 2]
tab1, tab2 = st.tabs(["Sunburst Chart", "Treemap"])
with tab1:
    fig = px.sunburst(
        sunburst_df, path=['genre', 'studio'], values='count', color='genre',
        title='Sunburst: Genres → Studios'
    )
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    fig = px.treemap(
        sunburst_df, path=['genre', 'studio'], values='count',
        title='Treemap: Studio Dominance by Genre'
    )
    st.plotly_chart(fig, use_container_width=True)

st.header("🏅 Studios with Consistently High Scores")
df_scores = df_anime[['studio', 'score']].dropna()
df_scores['studio'] = df_scores['studio'].str.strip()
studio_scores = df_scores.groupby('studio').agg(
    avg_score=('score', 'mean'),
    anime_count=('score', 'count')
).reset_index()
min_anime = st.slider("Minimum Anime to Consider", 1, 20, 5)
studio_scores = studio_scores[studio_scores['anime_count'] >= min_anime]
top_studios_by_score = studio_scores.sort_values('avg_score', ascending=False).head(10)
fig = px.bar(
    top_studios_by_score,
    x='avg_score',
    y='studio',
    orientation='h',
    color='avg_score',
    color_continuous_scale='viridis',
    title="Top Studios by Score"
)
fig.update_layout(template='plotly_white', showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🫧 Studio Productivity vs Quality")
studio_stats = df_anime.groupby('studio').agg({'score': 'mean', 'anime_id': 'count'}).rename(
    columns={'anime_id': 'anime_count'}).reset_index()
top_studio_stats = studio_stats[studio_stats['anime_count'] > 10]
fig = px.scatter(
    top_studio_stats,
    x='anime_count',
    y='score',
    size='anime_count',
    color='score',
    hover_name='studio',
    title='Bubble Plot: Productivity vs Quality',
    size_max=40,
    color_continuous_scale='Viridis'
)
fig.update_layout(template='plotly_white')
st.plotly_chart(fig, use_container_width=True)
