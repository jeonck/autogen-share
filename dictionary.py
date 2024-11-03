import streamlit as st
import requests

def get_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    return None

def main():
    st.title("영어 단어 사전 검색")
    
    # 검색창
    word = st.text_input("검색할 단어를 입력하세요:")
    
    if word:
        result = get_word_definition(word)
        
        if result:
            # 단어 정보 표시
            st.subheader(f"'{word}' 의 검색 결과:")
            
            for entry in result[0]['meanings']:
                st.write(f"**품사:** {entry['partOfSpeech']}")
                
                for definition in entry['definitions']:
                    st.write("**정의:**", definition['definition'])
                    
                    # 예문이 있는 경우에만 표시
                    if 'example' in definition:
                        st.write("**예문:**", definition['example'])
                    
                st.markdown("---")
        else:
            st.error("단어를 찾을 수 없습니다. 철자를 확인해주세요.")

if __name__ == "__main__":
    main()
