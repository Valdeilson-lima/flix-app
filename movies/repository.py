import requests
import streamlit as st
from login.service import logout


class MovieRepository:

    def __init__(self):
        self.__base_url = 'http://35.184.34.233:8000/api/v1/'
        self.__movies_url = f'{self.__base_url}movies/'
        self.__headers = {
            'Authorization': f'Bearer {st.session_state.get("token", "")}'
        }

    def get_movies(self):
        try:
            response = requests.get(
                self.__movies_url,
                headers=self.__headers
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                st.warning("Sessão expirada. Realize login novamente.")
                logout()
                return None
            elif response.status_code == 404:
                st.error(f"Endpoint não encontrado: {self.__movies_url}")
                return None
            else:
                raise Exception(f"Erro ao obter filmes. Código de status: {response.status_code}")
        except requests.RequestException as e:
            st.error(f"Erro de conexão com a API: {e}")
            return None

    def create_movie(self, movie):
        try:
            response = requests.post(
                self.__movies_url,
                headers=self.__headers,
                data=movie,  # Use `json` para enviar dados no formato JSON
            )
            if response.status_code == 201:
                st.success("Filme cadastrado com sucesso!")
                return response.json()
            elif response.status_code == 401:
                st.warning("Sessão expirada. Realize login novamente.")
                logout()
                return None
            elif response.status_code == 400:
                st.error("Erro de validação ao cadastrar o filme. Verifique os dados enviados.")
                return None
            else:
                raise Exception(f"Erro ao cadastrar filme. Código de status: {response.status_code}")
        except requests.RequestException as e:
            st.error(f"Erro de conexão com a API: {e}")
            return None

    def get_movie_stats(self):
        try:
            response = requests.get(
                f'{self.__movies_url}stats/',
                headers=self.__headers
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                st.warning("Sessão expirada. Realize login novamente.")
                logout()
                return None
            elif response.status_code == 404:
                st.error(f"Endpoint de estatísticas não encontrado: {self.__movies_url}stats/")
                return None
            else:
                raise Exception(f"Erro ao obter estatísticas. Código de status: {response.status_code}")
        except requests.RequestException as e:
            st.error(f"Erro de conexão com a API: {e}")
            return None
