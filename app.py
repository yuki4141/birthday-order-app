# app.py
import streamlit as st
import pandas as pd

st.title("慶生訂購小程式")

people = st.number_input("人數", min_value=1, value=35)
budget_per_person = st.number_input("每人預算", min_value=1, value=200)

total_budget = people * budget_per_person
st.write(f"預算上限：{total_budget} 元")

# 建立 DataFrame 表單
df = pd.DataFrame([
    ["點心", 35, 140],
    ["飲料", 18, 65],
    ["飲料", 17, 40]
], columns=["品項", "數量", "單價"])

edited_df = st.data_editor(df, num_rows="dynamic")

# 計算小計
edited_df["小計"] = edited_df["數量"] * edited_df["單價"]

total = edited_df["小計"].sum()
st.write(f"總金額：{total} 元")

# 預算比較
if total > total_budget:
    st.error(f"⚠️ 超過預算！總金額 {total} 元，大於預算上限 {total_budget} 元")
else:
    st.success(f"✅ 預算正常，總金額 {total} 元")

# 匯出 Excel
import io
from openpyxl import Workbook

if st.button("匯出 Excel"):
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.append(list(edited_df.columns))
    for row in edited_df.values:
        ws.append(list(row))
    wb.save(output)
    st.download_button(
        label="下載 Excel",
        data=output.getvalue(),
        file_name="order.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
