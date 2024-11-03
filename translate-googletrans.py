import streamlit as st
from googletrans import Translator

def main():
    st.title('영어-한국어 번역기')
    
    # 번역기 객체 생성
    translator = Translator()
    
    # 텍스트 입력 영역
    text_input = st.text_area("번역할 텍스트를 입력하세요:", height=150)
    
    # 번역 방향 선택
    translation_direction = st.radio(
        "번역 방향을 선택하세요:",
        ('영어 → 한국어', '한국어 → 영어')
    )
    
    if st.button('번역하기'):
        if text_input:
            try:
                if translation_direction == '영어 → 한국어':
                    translated = translator.translate(text_input, src='en', dest='ko')
                else:
                    translated = translator.translate(text_input, src='ko', dest='en')
                
                st.success('번역 결과:')
                st.write(translated.text)
            except Exception as e:
                st.error(f'번역 중 오류가 발생했습니다: {str(e)}')
        else:
            st.warning('번역할 텍스트를 입력해주세요.')

if __name__ == '__main__':
    main()
