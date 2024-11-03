import streamlit as st
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os

st.title("콘텐츠 자동 생성과 공유")

# OpenAI API 키 입력 섹션
api_key = st.text_input("OpenAI API 키를 입력하세요:", type="password")
if not api_key:
    st.warning("API 키를 입력해주세요.")
    st.stop()

# API 키 설정
os.environ["OPENAI_API_KEY"] = api_key

# 파일 업로드 섹션
uploaded_file = st.file_uploader("PDF 또는 텍스트 파일을 업로드하세요", type=["pdf", "txt"])

if uploaded_file is not None:
    # 임시 파일로 저장
    with open("temp_file", "wb") as f:
        f.write(uploaded_file.getvalue())
    
    # 파일 타입에 따른 로더 선택
    if uploaded_file.type == "application/pdf":
        loader = PyPDFLoader("temp_file")
    else:
        loader = TextLoader("temp_file")
    
    # 문서 로드 및 분할
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    # 임베딩 생성 및 벡터 저장소 생성
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    # 질문 입력 섹션
    user_question = st.text_input("질문을 입력하세요:")
    
    if user_question:
        # RAG를 사용한 질문-답변
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )
        
        response = qa.run(user_question)
        st.write("답변:", response)
    
    # 임시 파일 삭제
    os.remove("temp_file")