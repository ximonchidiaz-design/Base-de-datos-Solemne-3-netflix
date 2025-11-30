import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv.csv")

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Contenido de Netflix",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title('🎬 Análisis de Contenido de Netflix')
st.markdown('Una aplicación interactiva de visualización de datos con **Streamlit**, **Pandas** y **Matplotlib**.')

# --- SIDEBAR ---
st.sidebar.header('⚙️ Opciones de Filtrado')

content_type = st.sidebar.selectbox(
    'Tipo de Contenido',
    ['Todos', 'Movie', 'TV Show']
)

min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())

year_range = st.sidebar.slider(
    'Rango de Año de Lanzamiento',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

df_filtered = df.copy()
if content_type != 'Todos':
    df_filtered = df_filtered[df_filtered['type'] == content_type]

df_filtered = df_filtered[
    (df_filtered['release_year'] >= year_range[0]) &
    (df_filtered['release_year'] <= year_range[1])
]

st.sidebar.markdown('---')
st.sidebar.info(f'Mostrando **{len(df_filtered)}** títulos filtrados.')

# =====================================================================
# 2. VISUALIZACIONES
# =====================================================================

st.header('📊 Visualizaciones Clave del Dataset (Matplotlib)')

col1, col2 = st.columns(2)

# --- Gráfico 1 ---
with col1:
    st.subheader('1. Distribución de Tipos de Contenido')
    type_counts = df_filtered['type'].value_counts()

    fig_type, ax_type = plt.subplots(figsize=(6, 6))
    ax_type.pie(
        type_counts,
        labels=type_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=['#E50914', '#221F1F'],
        textprops={'color': 'white'}
    )
    ax_type.axis('equal')
    fig_type.patch.set_facecolor('#0E1117')
    ax_type.set_facecolor('#0E1117')
    st.pyplot(fig_type)

# --- Gráfico 2 ---
with col2:
    st.subheader('2. Top 10 Géneros Populares')
    df['main_genre'] = df['listed_in'].str.split(',').str[0]
    genre_counts = df_filtered['main_genre'].value_counts().head(10)

    fig_genre, ax_genre = plt.subplots(figsize=(6, 6))
    genre_counts.sort_values(ascending=True).plot(kind='barh', ax=ax_genre, color='#B20710')
    ax_genre.set_xlabel('Número de Títulos', color='white')
    ax_genre.set_ylabel('Género', color='white')
    ax_genre.tick_params(colors='white')
    fig_genre.patch.set_facecolor('#0E1117')
    ax_genre.set_facecolor('#0E1117')
    plt.tight_layout()
    st.pyplot(fig_genre)

# --- Gráfico 3 ---
st.markdown('---')
st.subheader('3. Tendencia de Contenido Añadido a Netflix por Año')

df_trend = df.groupby('year_added').size().reset_index(name='count')
df_trend = df_trend.dropna(subset=['year_added'])
df_trend['year_added'] = df_trend['year_added'].astype(int)

fig_trend, ax_trend = plt.subplots(figsize=(12, 5))
ax_trend.plot(df_trend['year_added'], df_trend['count'], marker='o', color='#E50914', linewidth=2)

ax_trend.set_title('Contenido Añadido por Año', color='white')
ax_trend.set_xlabel('Año de Adición', color='white')
ax_trend.set_ylabel('Cantidad de Títulos', color='white')
ax_trend.grid(axis='y', linestyle='--', alpha=0.7)

fig_trend.patch.set_facecolor('#0E1117')
ax_trend.set_facecolor('#0E1117')
ax_trend.tick_params(axis='x', colors='white')
ax_trend.tick_params(axis='y', colors='white')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig_trend)

# --- Datos filtrados ---
st.markdown('---')
st.subheader('📋 Vista de Datos Filtrados')
st.dataframe(df_filtered[['title', 'type', 'country', 'release_year', 'main_genre', 'rating']].head(20))

# --- Resumen ---
st.sidebar.markdown('---')
st.sidebar.caption('Proyecto desarrollado con:')
st.sidebar.markdown('- **Streamlit**')
st.sidebar.markdown('- **Pandas**')
st.sidebar.markdown('- **Matplotlib**')
