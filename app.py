import streamlit as st
import requests
import pandas as pd

st.title('광고 문구 서비스앱')
generate_ad_url = 'http://127.0.0.1:8000/create_ad'

product_name = st.text_input('제품 이름')
details = st.text_input('주요 내용')
options = st.multiselect('광고 문구의 느낌', options=['기본', '재밌게', '차분하게', '과장스럽게', '참신하게', '고급스럽게'], default=['기본'])

def storage_ad(product_name, details, tone_and_manner, ad):
    response = requests.post(
        'http://127.0.0.1:8000/store_ad',
        json={"product_name": product_name,
              "details": details,
              "tone_and_manner": tone_and_manner,
              "ad": ad})

if st.button("광고 문구 생성하기"):
    try:
        tone_and_manner = ", ".join(options)
        response = requests.post(
            generate_ad_url,
            json={"product_name": product_name,
                "details": details,
                "tone_and_manner": tone_and_manner})
        ad = response.json()['ad']
        print(ad)
        st.success(ad)
        storage_ad(product_name, details, tone_and_manner, ad)
    except:
        st.error("연결 실패!")

def show_ad():
    response = requests.get('http://127.0.0.1:8000/get_ad')
    if response.status_code == 200:
        ads = response.json()
        df = pd.DataFrame(ads)
        st.dataframe(df)
    else:
        st.error("광고 데이터를 불러오는 데 실패했습니다.")

show_ad()