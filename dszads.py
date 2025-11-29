import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv.csv")

# st.set_page_config (Función de Streamlit)
        st.set_page_config(
            page_title="Análisis de Contenido de Netflix",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        st.title('🎬 Análisis de Contenido de Netflix')
        st.markdown('Una aplicación interactiva de visualización de datos con **Streamlit**, **Pandas** y **Matplotlib**.')

        # --- SIDEBAR (Filtros, Componentes de Streamlit) ---
        st.sidebar.header('⚙️ Opciones de Filtrado')
        
        # Filtro por Tipo de Contenido (Componente de Streamlit)
        content_type = st.sidebar.selectbox(
            'Tipo de Contenido',
            ['Todos', 'Movie', 'TV Show']
        )
        
        # Slider para el Año de Lanzamiento (Componente de Streamlit)
        # Se asume que 'release_year' y las otras columnas necesarias ya existen en 'df'.
        min_year = int(df['release_year'].min())
        max_year = int(df['release_year'].max())
        year_range = st.sidebar.slider(
            'Rango de Año de Lanzamiento',
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )

        # Filtrar el DataFrame basado en las selecciones del usuario (Uso de Pandas)
        df_filtered = df.copy()
        if content_type != 'Todos':
            df_filtered = df_filtered[df_filtered['type'] == content_type]
        
        df_filtered = df_filtered[
            (df_filtered['release_year'] >= year_range[0]) & 
            (df_filtered['release_year'] <= year_range[1])
        ]

        st.sidebar.markdown('---')
        st.sidebar.info(f'Mostrando **{len(df_filtered)}** títulos filtrados.')
        
        # ==============================================================================
        # 2. VISUALIZACIONES CON MATPLOTLIB (Cumpliendo el requisito)
        # ==============================================================================

        st.header('📊 Visualizaciones Clave del Dataset (Matplotlib)')

        # Diseño en dos columnas (Streamlit)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('1. Distribución de Tipos de Contenido')
            # Datos (Pandas)
            type_counts = df_filtered['type'].value_counts()
            
            # Gráfico (Matplotlib)
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
            st.pyplot(fig_type) # Mostrar el gráfico (Función de Streamlit)

        with col2:
            st.subheader('2. Top 10 Géneros Populares')
            # Datos (Pandas)
            genre_counts = df_filtered['main_genre'].value_counts().head(10)

            # Gráfico (Matplotlib)
            fig_genre, ax_genre = plt.subplots(figsize=(6, 6))
            genre_counts.sort_values(ascending=True).plot(kind='barh', ax=ax_genre, color='#B20710')
            ax_genre.set_xlabel('Número de Títulos', color='white')
            ax_genre.set_ylabel('Género', color='white')
            ax_genre.tick_params(colors='white')
            fig_genre.patch.set_facecolor('#0E1117')
            ax_genre.set_facecolor('#0E1117')
            plt.tight_layout()
            st.pyplot(fig_genre) # Mostrar el gráfico (Función de Streamlit)


        st.markdown('---')

        # Visualización 3: Tendencia de Contenido Añadido
        st.subheader('3. Tendencia de Contenido Añadido a Netflix por Año')
        # Datos (Pandas)
        df_trend = df.groupby('year_added').size().reset_index(name='count')
        df_trend = df_trend.dropna(subset=['year_added']) 
        df_trend['year_added'] = df_trend['year_added'].astype(int)

        # Gráfico (Matplotlib)
        fig_trend, ax_trend = plt.subplots(figsize=(12, 5))
        ax_trend.plot(df_trend['year_added'], df_trend['count'], marker='o', color='#E50914', linewidth=2)
        ax_trend.set_title('Contenido Añadido por Año (Global Dataset)', color='white')
        ax_trend.set_xlabel('Año de Adición', color='white')
        ax_trend.set_ylabel('Cantidad de Títulos', color='white')
        ax_trend.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Estilo oscuro
        fig_trend.patch.set_facecolor('#0E1117')
        ax_trend.set_facecolor('#0E1117')
        ax_trend.tick_params(axis='x', colors='white')
        ax_trend.tick_params(axis='y', colors='white')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig_trend) # Mostrar el gráfico (Función de Streamlit)

        # Opcional: Mostrar los datos crudos filtrados
        st.markdown('---')
        st.subheader('📋 Vista de Datos Filtrados')
        st.dataframe(df_filtered[['title', 'type', 'country', 'release_year', 'main_genre', 'rating']].head(20)) # Mostrar tabla (Función de Streamlit)

        # ==============================================================================
        # 3. RESUMEN DE REQUISITOS
        # ==============================================================================
        st.sidebar.markdown('---')
        st.sidebar.caption('Proyecto desarrollado estrictamente con:')
        st.sidebar.markdown('- **Streamlit** (Interfaz Web)')
        st.sidebar.markdown('- **Pandas** (Análisis de Datos)')
        st.sidebar.markdown('- **Matplotlib** (Visualización de Datos)')
