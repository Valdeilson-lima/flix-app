from datetime import datetime
import pandas as pd
import streamlit as st
from genres.service import GenreService
from actors.service import ActorService
from movies.service import MovieService
from st_aggrid import AgGrid, ExcelExportMode


def display_movies_table(movies):
    """
    Exibe a tabela de filmes utilizando o AgGrid.
    """
    try:
        movies_df = pd.json_normalize(movies)
        movies_df = movies_df.drop(columns=['actors'])
        if 'release_date' in movies_df.columns:
            movies_df['release_date'] = pd.to_datetime(movies_df['release_date']).dt.strftime('%d/%m/%Y')

        AgGrid(
            data=movies_df,
            reload_data=True,
            columns_auto_size_mode=True,
            enableSorting=True,
            enableFilter=True,
            enableColResize=True,
            excel_export_mode=ExcelExportMode.MANUAL,
            key='movies_grid',
        )
    except Exception as e:
        st.error(f"Erro ao processar dados dos filmes: {e}")


def get_movie_inputs():
    """
    Captura os dados necessários para cadastrar um novo filme.
    """
    with st.form(key='movie_form'):
        title = st.text_input('Título')
        release_date = st.date_input(
            label='Data de lançamento',
            value=datetime.today(),
            min_value=datetime(1800, 1, 1).date(),
            max_value=datetime.today(),
            format='DD/MM/YYYY',
        )

        genre_service = GenreService()
        genres = genre_service.get_genres()
        genre_names = {genre['name']: genre['id'] for genre in genres}
        selected_genre_name = st.selectbox('Gênero', list(genre_names.keys()))

        actor_service = ActorService()
        actors = actor_service.get_actors()
        if actors:
            actor_names = {actor['name']: actor['id'] for actor in actors}
            selected_actors_names = st.multiselect('Atores/Atrizes', list(actor_names.keys()))
            selected_actors_ids = [actor_names[name] for name in selected_actors_names]
        else:
            st.warning('Nenhum ator disponível. Cadastre atores primeiro.')
            selected_actors_ids = []

        resume = st.text_area('Resumo')

        submitted = st.form_submit_button('Cadastrar')
        return submitted, title, release_date, selected_genre_name, selected_actors_ids, resume, genre_names


def show_movies():
    movie_service = MovieService()
    movies = movie_service.get_movies()

    st.title('Lista de Filmes')
    
    if movies:
        st.write('Veja os filmes abaixo:')
        display_movies_table(movies)
    else:
        st.warning('Nenhum filme encontrado. Você pode cadastrar um novo abaixo.')

    st.title('Cadastrar Novo Filme')

    # Capturar entradas do formulário
    (
        submitted,
        title,
        release_date,
        selected_genre_name,
        selected_actors_ids,
        resume,
        genre_names
    ) = get_movie_inputs()

    # Validação e cadastro de filme
    if submitted:
        if not title:
            st.error("O título é obrigatório.")
        elif not selected_genre_name:
            st.error("O gênero é obrigatório.")
        elif not selected_actors_ids:
            st.error("Selecione pelo menos um ator/atriz.")
        else:
            # Cadastrar filme
            new_movie = movie_service.create_movie(
                title=title,
                release_date=release_date,
                genre=genre_names[selected_genre_name],
                actors=selected_actors_ids,
                resume=resume,
            )
            if new_movie:
                st.success("Filme cadastrado com sucesso!")
                st.rerun()
            else:
                st.error('Erro ao cadastrar o filme. Verifique os campos.')



