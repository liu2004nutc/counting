import streamlit as st

# 設定網頁標題
st.set_page_config(page_title="學術獎勵金試算", page_icon="")

# 主標題
st.title("國立臺中科技大學研究發展處")
st.title("期刊論文申請獎勵金額試算系統")
st.write("請由上而下輸入資訊，系統將依照校準後的公式計算。")

# --- 單一列式手動輸入欄位 ---
st.divider()

category = st.selectbox("1. 申請類別", ["A", "B1", "B2"])
total_authors = st.number_input("2. 作者總人數", min_value=1, max_value=50, value=1, step=1)
my_pos = st.number_input("3. 您的作者順位", min_value=1, max_value=total_authors, value=1, step=1)
corr_pos = st.number_input("4. 通訊作者順位", min_value=1, max_value=total_authors, value=1, step=1)

# 獎金對照表
category_map = {"A": 30000, "B1": 20000, "B2": 12000}
total_reward = category_map[category]

def calculate_precise():
    n = int(total_authors)
    me = int(my_pos)
    cp = int(corr_pos)
    results = [0] * n
    
    if n == 1:
        return total_reward
    elif n == 2:
        if cp == 1:
            r1 = round(total_reward * 0.8)
            return r1 if me == 1 else (total_reward - r1)
        else:
            return round(total_reward * 0.5)
    else:
        # 3人以上邏輯
        # 1. 處理第一作者與通訊作者 (40% 或 80%)
        if cp == 1:
            results[0] = round(total_reward * 0.8)
        else:
            results[0] = round(total_reward * 0.4)
            results[cp-1] = round(total_reward * 0.4)
        
        # 2. 處理剩餘作者 (權重分配)
        rem_money = total_reward - sum(results)
        rem_indices = [i for i in range(n) if results[i] == 0]
        
        if rem_indices:
            num_rem = len(rem_indices)
            # 權重由大到小 (例如 8, 7, 6...)
            weights = [num_rem - i for i in range(num_rem)]
            total_w = sum(weights)
            
            # 關鍵：先用 round 四捨五入
            for idx, r_idx in enumerate(rem_indices):
                results[r_idx] = int(round(rem_money * weights[idx] / total_w))
            
            # 3. 處理微小總額落差 (補在剩餘者中的第一位)
            diff = total_reward - sum(results)
            results[rem_indices[0]] += diff
            
    return results[me-1]

# 顯示結果
my_money = calculate_precise()

st.divider()

st.subheader("本篇申請獎勵金額試算結果：")
st.title(f":green[${my_money:,} 元]")

st.info(f"計算基礎：{category} 類(每篇獎勵金上限 ${total_reward:,} 元)")
st.caption("※ 本版本已針對 A 類 10 人 (1333, 1167...) 之進位邏輯進行優化。")





