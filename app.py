# app.py

import streamlit as st
import pandas as pd
import io
from openpyxl import Workbook

st.set_page_config(page_title="慶生訂購小程式", layout="wide")

st.title("🎂 慶生訂購小程式")

# 人數 & 每人預算
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    people = st.number_input("人數", min_value=1, value=35)

with col2:
    budget_per_person = st.number_input("每人預算", min_value=1, value=200)

total_budget = people * budget_per_person

with col3:
    st.markdown(
        f"### 預算上限：<span style='color:blue'>{total_budget:,} 元</span>",
        unsafe_allow_html=True,
    )

st.write("---")

# 預設品項
default_data = pd.DataFrame({
    "品項": ["點心", "飲料", "飲料"],
    "數量": [35, 18, 17],
    "單價": [140, 65, 40],
})

# Data Editor (可編輯 + 可新增列)
edited_df = st.data_editor(
    default_data,
    num_rows="dynamic",
    use_container_width=True,
    key="editor"
)

# 計算小計
edited_df["小計"] = edited_df["數量"] * edited_df["單價"]
total = edited_df["小計"].sum()
remaining = total_budget - total

st.write("---")

# 顯示總金額 & 剩餘金額
col4, col5 = st.columns(2)
with col4:
    st.metric("總金額", f"{total:,} 元")

with col5:
    if remaining < 0:
        st.metric("超出預算", f"{abs(remaining):,} 元", delta=f"-{abs(remaining):,}", delta_color="inverse")
    else:
        st.metric("剩餘預算", f"{remaining:,} 元")

# 預算檢查
if total > total_budget:
    st.error(f"⚠️ 總金額 {total:,} 元，已超過預算上限 {total_budget:,} 元！")
else:
    st.success(f"✅ 總金額 {total:,} 元，在預算內 {total_budget:,} 元。")

# 匯出 Excel
def to_excel(df, total, people, budget_per_person, total_budget, remaining):
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "訂單"

    # 標題列
    ws.append(list(df.columns))

    # 資料列
    for row in df.values:
        ws.append(list(row))

    ws.append([])
    ws.append(["總金額", total])
    ws.append(["人數", people])
    ws.append(["每人預算", budget_per_person])
    ws.append(["預算上限", total_budget])
    ws.append(["剩餘金額", remaining])

    wb.save(output)
    return output.getvalue()

excel_data = to_excel(
    edited_df, total, people, budget_per_person, total_budget, remaining
)

st.download_button(
    label="匯出 Excel",
    data=excel_data,
    file_name="慶生訂單.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
