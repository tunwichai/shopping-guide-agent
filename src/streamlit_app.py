import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

indices = np.linspace(0, 1, num_points)
theta = 2 * np.pi * num_turns * indices
radius = indices

x = radius * np.cos(theta)
y = radius * np.sin(theta)

df = pd.DataFrame({
    "x": x,
    "y": y,
    "idx": indices,
    "rand": np.random.randn(num_points),
})

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))

# ส่วนใหม่: Smart Product Recommendation Agent
st.title("Smart Product Recommendation Agent")
st.write("ระบบแนะนำมือถืออัจฉริยะ: พิมพ์ความต้องการ เช่น 'มือถือกล้องดี งบ 20000'")

# โหลดฐานข้อมูลสินค้า
df = pd.read_csv("data/products.csv")

user_input = st.text_input("พิมพ์ความต้องการของคุณ:")

def extract_budget(text):
    import re
    match = re.search(r"งบ\s*([0-9,]+)", text)
    if match:
        return int(match.group(1).replace(",", ""))
    return None

def filter_products(df, user_input):
    filtered = df.copy()
    # กรองเฉพาะมือถือ
    filtered = filtered[filtered["category"].str.contains("มือถือ")]
    # กรองตามคำค้นหา
    keywords = []
    if "กล้อง" in user_input or "ถ่ายรูป" in user_input:
        keywords.append("กล้อง")
    # เพิ่ม keyword อื่นๆ ได้ตามต้องการ

    for kw in keywords:
        filtered = filtered[filtered["description"].str.contains(kw)]
    # กรองตามงบประมาณ
    budget = extract_budget(user_input)
    if budget:
        filtered = filtered[filtered["price"] <= budget]
    return filtered

if user_input:
    results = filter_products(df, user_input)
    if len(results) == 0:
        st.warning("ขออภัย ไม่พบสินค้าที่ตรงกับความต้องการ")
    else:
        st.success(f"พบ {len(results)} รุ่นที่ตรงกับความต้องการ")
        for idx, row in results.iterrows():
            st.image(row["image_url"], width=200)
            st.write(f"**{row['name']}** - {row['price']} บาท")
            st.write(row["description"])
            st.write(f"[ดูสินค้าเพิ่มเติม]({row['product_url']})")