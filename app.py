import streamlit as st
import pandas as pd

st.set_page_config(page_title="慶生訂購小程式", layout="wide")

st.title("🎂 慶生訂購小程式")

# 預設人數、預算
people = st.number_input("人數", min_value=1, value=35)
budget_per_person = st.number_input("每人預算", min_value=1, value=200)
budget_limit = people * budget_per_person

st.info(f"目前總預算上限： {budget_limit} 元")

# 建立 session state DataFrame
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["品項", "數量", "單價", "小計"])

# 新增品項表單
st.subheader("新增品項")

with st.form("add_form"):
    col1, col2, col3 = st.columns(3)
    name = col1.text_input("品項名稱", "")
    qty = col2.number_input("數量", min_value=0, value=0, step=1)
    price = col3.number_input("單價", min_value=0, value=0, step=1)

    submitted = st.form_submit_button("新增品項")

    if submitted:
        if name:
            subtotal = qty * price
            st.session_state.df = st.session_state.df.append(
                {
                    "品項": name,
                    "數量": qty,
                    "單價": price,
                    "小計": subtotal
                },
                ignore_index=True
            )
            st.success(f"✅ 已新增品項：{name}")
        else:
            st.warning("請輸入品項名稱！")

# 顯示目前品項表格
if not st.session_state.df.empty:
    st.subheader("目前訂購項目")
    st.dataframe(
        st.session_state.df,
        use_container_width=True
    )

    total = st.session_state.df["小計"].sum()
    st.markdown(f"## 💰 總金額：{total} 元")

    if total > budget_limit:
        st.error(f"⚠️ 總金額 {total} 元，超過預算上限 {budget_limit} 元！")
    else:
        st.success(f"✅ 總金額 {total} 元，在預算內。")

# 清空按鈕
if st.button("清空所有品項"):
    st.session_state.df = pd.DataFrame(columns=["品項", "數量", "單價", "小計"])
    st.info("✅ 已清空所有品項！")