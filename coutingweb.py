import streamlit as st

# 設定網頁標題
st.set_page_config(page_title="學術獎勵金試算", page_icon="💰")

st.title("💰 學術獎勵金試算系統")
st.write("根據您的作者順位與申請類別，自動計算預計獎金。")

# --- 側邊欄輸入 ---
st.sidebar.header("輸入參數")
category = st.sidebar.selectbox("申請類別", ["A", "B1", "B2"])
total_authors = st.sidebar.slider("作者總人數", 1, 10, 5)
my_pos = st.sidebar.number_input("您的作者順位", min_value=1, max_value=total_authors, value=1)
is_corr = st.sidebar.checkbox("我是通訊作者")

# 獎金邏輯
category_map = {"A": 30000, "B1": 20000, "B2": 12000}
total_reward = category_map[category]

def calculate():
    results = [0] * total_authors
    corr_pos = my_pos if is_corr else 1
    
    if total_authors == 1:
        results[0] = total_reward
    elif total_authors == 2:
        if corr_pos == 1:
            results[0] = int(total_reward * 0.8)
            results[1] = total_reward - results[0]
        else:
            results[0] = int(total_reward * 0.5)
            results[1] = int(total_reward * 0.5)
    else:
        if corr_pos == 1:
            results[0] = int(total_reward * 0.8)
        else:
            results[0] = int(total_reward * 0.4)
            results[corr_pos-1] = int(total_reward * 0.4)
        
        rem_money = total_reward - sum(results)
        rem_indices = [i for i in range(total_authors) if results[i] == 0]
        
        if rem_indices:
            weights = [len(rem_indices) - i for i in range(len(rem_indices))]
            total_weight = sum(weights)
            for idx, r_idx in enumerate(rem_indices):
                results[r_idx] = round(rem_money * weights[idx] / total_weight)
            
            diff = total_reward - sum(results)
            results[rem_indices[0]] += diff
    return results[my_pos-1]

# --- 顯示結果 ---
my_money = calculate()

st.metric(label="您預計可獲得的獎金", value=f"${my_money:,} 元")

st.info(f"計算基礎：{category} 類總額 ${total_reward:,} 元。")

# 加個小提醒
st.caption("※ 本工具僅供參考，實際金額請以校方/單位核算為準。")