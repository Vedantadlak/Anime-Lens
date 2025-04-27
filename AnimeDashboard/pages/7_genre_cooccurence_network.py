import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter
from itertools import combinations

st.set_page_config(page_title="Anime Genre Network", layout="wide")
st.title("🎭 Anime Genre Co-occurrence Network")
st.markdown("Explore how different anime genres are frequently paired together using an interactive network.")

@st.cache_data
def load_data():
    df = pd.read_csv('./data/anime_cleaned.csv')
    df['genre'] = df['genre'].fillna('Unknown')
    df['genre'] = df['genre'].str.split(', ')
    return df

df = load_data()
threshold = st.slider("Minimum Co-occurrence Threshold", min_value=10, max_value=100, value=50, step=5)
st.write(f"Showing genre pairs that occur together in at least **{threshold}** shows.")

pair_counter = Counter()
for genres in df['genre']:
    if isinstance(genres, list) and len(genres) > 1:
        pairs = combinations(sorted(set(genres)), 2)
        pair_counter.update(pairs)

edges = [(g1, g2, w) for (g1, g2), w in pair_counter.items() if w >= threshold]
if not edges:
    st.warning("No genre pairs meet the threshold.")
else:
    source = [e[0] for e in edges]
    target = [e[1] for e in edges]
    value = [e[2] for e in edges]
    all_genres = list(set(source + target))
    source_idx = [all_genres.index(s) for s in source]
    target_idx = [all_genres.index(t) for t in target]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_genres,
            color="blue"
        ),
        link=dict(
            source=source_idx,
            target=target_idx,
            value=value
        )
    ))
    fig.update_layout(title_text="Genre Co-occurrence Sankey Diagram", font_size=10, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
