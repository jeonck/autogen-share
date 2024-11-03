import streamlit as st
import requests

def search_movie(title, api_key):
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    response = requests.get(url)
    return response.json()

def main():
    st.title("영화 검색 앱(OMDB API)")
    
    # API 키 입력
    api_key = st.text_input("OMDB API 키를 입력하세요", type="password")
    
    # 검색창
    movie_title = st.text_input("영화 제목을 입력하세요")
    
    if st.button("검색"):
        if not api_key:
            st.warning("API 키를 입력해주세요.")
            return
            
        if movie_title:
            # API 키를 search_movie 함수에 전달
            result = search_movie(movie_title, api_key)
            
            if result.get("Response") == "True":
                # 영화 정보 표시
                st.image(result["Poster"])
                st.header(result["Title"])
                st.write(f"개봉년도: {result['Year']}")
                st.write(f"감독: {result['Director']}")
                st.write(f"배우: {result['Actors']}")
                st.write(f"평점: {result['imdbRating']}")
                st.write(f"줄거리: {result['Plot']}")
            else:
                st.error("영화를 찾을 수 없습니다.")
        else:
            st.warning("영화 제목을 입력해주세요.")

if __name__ == "__main__":
    main()
