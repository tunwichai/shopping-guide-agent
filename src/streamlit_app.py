import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

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