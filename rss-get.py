#  pip install feedparser pandas

import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

st.title("RSS 피드 리더")

# RSS 피드 URL 목록
rss_feeds = {
    "GeekNews": "http://feeds.feedburner.com/geeknews-feed",
    "IT/과학 - 한겨레": "https://www.hani.co.kr/rss/science/",
    "IT 뉴스 - ZDNet Korea": "https://feeds.feedburner.com/zdkorea",
    "ITFind": "http://www.itfind.or.kr/itfind/rss/all.htm?rssType=02",
    "KISA 공지사항": "https://www.kisa.or.kr/rss/401",
    "한국관광공사 블로그": "http://blog.rss.naver.com/korea_diary.xml"
}

# 피드 선택 셀렉트박스
selected_feed = st.selectbox(
    "RSS 피드를 선택하세요:",
    options=list(rss_feeds.keys())
)

if selected_feed:
    # RSS 피드 파싱
    feed = feedparser.parse(rss_feeds[selected_feed])
    
    # 데이터 추출 및 데이터프레임 생성
    feed_data = []
    for entry in feed.entries:
        published = entry.get('published', entry.get('updated', 'No date'))
        try:
            # 날짜 형식 통일
            date = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M')
        except:
            date = published
            
        feed_data.append({
            '제목': entry.title,
            '날짜': date,
            '링크': entry.link
        })
    
    df = pd.DataFrame(feed_data)
    
    # 각 뉴스 항목 표시
    for idx, row in df.iterrows():
        with st.container():
            st.subheader(row['제목'])
            st.write(f"게시일: {row['날짜']}")
            st.markdown(f"[기사 링크]({row['링크']})")
            st.divider()

    # 데이터프레임 다운로드 버튼
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="CSV로 다운로드",
        data=csv,
        file_name=f"{selected_feed}_뉴스.csv",
        mime="text/csv"
    )
