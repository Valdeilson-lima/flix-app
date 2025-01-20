import streamlit as st
from movies.repository import MovieRepository


class MovieService:

    def __init__(self):
        self.movie_repository = MovieRepository()

    def get_movies(self):
        """
        Retorna a lista de filmes. Se já estiver no estado da sessão, utiliza-a para evitar chamadas desnecessárias.
        """
        if 'movies' in st.session_state and st.session_state.movies:
            return st.session_state.movies

        movies = self.movie_repository.get_movies()
        if movies:  # Verifica se os filmes foram retornados corretamente
            st.session_state.movies = movies
        else:
            st.session_state.movies = []  # Evita que 'movies' seja None
        return st.session_state.movies

    def create_movie(self, title, release_date, genre, actors, resume):
        """
        Cria um novo filme e o adiciona ao estado da sessão, se bem-sucedido.
        """
        movie = dict(
            title=title,
            release_date=release_date,
            genre=genre,
            actors=actors,
            resume=resume,
        )
        try:
            new_movie = self.movie_repository.create_movie(movie)
            if new_movie:
                # Verifica se 'movies' existe no estado da sessão antes de adicionar
                if 'movies' not in st.session_state:
                    st.session_state.movies = []
                st.session_state.movies.append(new_movie)
            return new_movie
        except Exception as e:
            st.error(f"Erro ao criar o filme: {e}")
            return None

    def get_movie_stats(self):
        """
        Obtém estatísticas de filmes. Lança erro caso a API retorne dados inválidos.
        """
        try:
            stats = self.movie_repository.get_movie_stats()
            if stats:
                return stats
            st.warning("Estatísticas não disponíveis no momento.")
            return None
        except Exception as e:
            st.error(f"Erro ao obter estatísticas: {e}")
            return None
