#main.py
import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO


st.title("🖼️ AI 이미지 생성기")
st.write("텍스트를 입력하면, 해당 내용을 바탕으로 이미지를 생성합니다.")

st.sidebar.title("🔑 설정")
openai_api_key = st.sidebar.text_input("OpenAI API 키 입력", type="password")

if not openai_api_key:
    st.sidebar.warning("OpenAI API 키를 입력하세요.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# 🔶 스타일 선택
style_options = {
    "기본": "",
    "파스텔 미니어처": "4K, miniature style, pastel mood, chubby and cute",
    "사이버펑크": "cyberpunk, neon lights, futuristic cityscape",
    "고흐 유화 스타일": "Van Gogh painting style, oil texture, vivid colors",
    "일러스트": "flat illustration, vector art, colorful"
}
selected_style = st.selectbox("🎨 스타일 선택", list(style_options.keys()))
style_prompt = style_options[selected_style]

# 🔷 이미지 크기 선택
size_options = {
    "정사각형 (1024x1024)": "1024x1024",
    "세로형 (1024x1792)": "1024x1792",
    "가로형 (1792x1024)": "1792x1024"
}

selected_size_label = st.radio("🖼️ 이미지 크기 선택", list(size_options.keys()), index=0)
selected_size = size_options[selected_size_label]

# 📝 프롬프트 입력
prompt = st.text_input("이미지 설명을 입력하세요", value="4 chubby cute cats repairing a huge toy car, christmas mood")

# 최종 프롬프트 구성
final_prompt = f"{style_prompt}, {prompt}" if style_prompt else prompt

# 이미지 생성 버튼
if st.button("이미지 생성하기"):
    with st.spinner("이미지를 생성 중입니다..."):
        try:
            response1 = client.images.generate(
                prompt=final_prompt,
                model="dall-e-3",
                n=1,
                size=selected_size
            )
            response2 = client.images.generate(
                prompt=final_prompt,
                model="dall-e-3",
                n=1,
                size=selected_size
            )

            image_url1 = response1.data[0].url
            image_url2 = response2.data[0].url

            cols = st.columns(2)
            with cols[0]:
                st.image(image_url1, caption="이미지 1", use_column_width=True)
                # ✅ 이미지 1 다운로드 버튼
                image_data1 = requests.get(image_url1).content
                buffer1 = BytesIO(image_data1)
                st.download_button(
                    label="⬇️ 이미지 1 다운로드",
                    data=buffer1,
                    file_name="image1.png",
                    mime="image/png"
                )

            with cols[1]:
                st.image(image_url2, caption="이미지 2", use_column_width=True)
                # ✅ 이미지 2 다운로드 버튼
                image_data2 = requests.get(image_url2).content
                buffer2 = BytesIO(image_data2)
                st.download_button(
                    label="⬇️ 이미지 2 다운로드",
                    data=buffer2,
                    file_name="image2.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
