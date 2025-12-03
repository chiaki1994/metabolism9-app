import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import streamlit as st

def gender_selector():
    st.write("**性別**")

    gender = st.radio(
        "",
        ["男性", "女性"],
        key="gender",
        horizontal=True,
    )

    # class を付与
    st.markdown(
        """
        <script>
        const radios = window.parent.document.querySelectorAll('div[role="radiogroup"]');
        if (radios.length > 0) {
            const group = radios[radios.length - 1];
            const wrapper = group.querySelector('div > div');  // stHorizontalBlock を取得
            if (wrapper) wrapper.id = "question-radio";
        }
        </script>
        """,
        unsafe_allow_html=True
    )

    return gender


st.markdown("""
<style>

/* =============================================================
   共通（背景・文字色）
============================================================= */
body, .main, .block-container {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

h1, h2, h3, h4, h5, h6,
p, div, label, span {
    color: #000000 !important;
}

/* =============================================================
   入力欄
============================================================= */
.stNumberInput input,
.stTextInput input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #CCCCCC !important;
    border-radius: 8px !important;
}

/* =============================================================
   ボタン
============================================================= */
div.stButton > button {
    display: block;
    margin: 30px auto 0 auto;
    background-color: #FFFFFF !important;
    color: #FF8C00 !important;
    border: 2px solid #FF8C00 !important;
    border-radius: 8px !important;
    padding: 8px 25px !important;
    font-weight: bold;
    transition: 0.3s ease;
}

div.stButton > button:hover {
    background-color: #FF8C00 !important;
    color: #FFFFFF !important;
}

/* ナビゲーションボタン */
.nav-buttons {
    display: flex;
    justify-content: center;
    gap: 80px;
    margin-top: 30px;
}

/* =============================================================
   性別ラジオ（ボタン風）
============================================================= */
.gender-radio > div {
    display: flex;
    justify-content: center;
    gap: 50px;
    margin: 20px 0 10px 0;
}

.gender-radio input[type="radio"] {
    display: none;
}

.gender-radio label {
    background-color: #FFFFFF;
    color: #FF8C00;
    border: 2px solid #FF8C00;
    border-radius: 10px;
    padding: 8px 35px;
    font-size: 20px;
    font-weight: 600;
    cursor: pointer;
}

/* 選択時 */
.gender-radio input[type="radio"]:checked + div label {
    background-color: #FF8C00 !important;
    color: #FFFFFF !important;
}

/* =============================================================
   質問ページ（1〜7 の水平ラジオ）
============================================================= */
#question-radio .stHorizontalBlock {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 45px !important;
    margin-top: 25px !important;
}

#question-radio .stHorizontalBlock > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

#question-radio .stHorizontalBlock label {
    font-size: 24px !important;
    font-weight: 700 !important;
    cursor: pointer;
    margin-top: 5px;
}

#question-radio .stHorizontalBlock input[type="radio"] {
    width: 28px !important;
    height: 28px !important;
}

</style>


""", unsafe_allow_html=True)




# =========================
# ページ状態管理
# =========================
if "page" not in st.session_state:
    st.session_state.page = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# =========================
# 質問定義
# =========================
question_sections = [
    ("食事", [
        "朝食をほぼ毎日食べている",
        "食事はバランスの良い内容を意識している",
        "野菜を毎日十分に摂取している",
        "間食（甘いもの・ジュースなど）を控えている",
        "揚げ物・脂っこい食事を控えている",
    ]),
    ("運動", [
        "週に3回以上、息が上がる程度の運動をしている",
        "運動を習慣として長期間に継続できている",
        "通勤や買い物など、日常の中で意識的に体を動かしている",
        "筋トレやストレッチなど、筋肉を意識した運動を行っている",
        "1日の座位時間を減らす工夫をしている（立ち仕事・歩行など）",
    ]),
    ("飲酒", [
        "飲酒頻度は適切である",
        "飲む量は適量に抑えられている",
        "飲酒をストレス発散に使っていない",
        "平日の飲酒を控えている",
        "休肝日を設けている",
    ]),
    ("仕事", [
        "仕事量と休息のバランスを取れていると感じる",
        "業務中に過度なストレスやプレッシャーを感じない",
        "長時間のデスクワーク中でも、意識的に休憩や体を動かしている",
        "仕事による身体的疲労を感じにくい",
        "勤務後や休日にしっかりとリフレッシュできている",
    ]),
    ("睡眠", [
        "就寝・起床時間は一定である",
        "睡眠時間は十分に確保できている",
        "寝つきが良い",
        "夜中に起きてもすぐ眠れる",
        "朝の目覚めが良い",
    ]),
    ("ストレス", [
        "強いストレスを感じることは少ない",
        "気分の落ち込み・無気力を感じることは少ない",
        "人間関係のストレスは少ない",
        "意欲や活力を保てている",
        "ストレスをうまくコントロールしている",
    ]),
]

flat_questions = [(sec, q) for sec, qs in question_sections for q in qs]

# =========================
# ページ 0 : 身体データ入力
# =========================
if st.session_state.page == 0:
    st.markdown("<h1 style='text-align:center;'>メタボリズム9</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>【身体データ入力】</h3>", unsafe_allow_html=True)

    # ▼▼ ここを置き換える ▼▼
    sex = gender_selector()

    # ▲▲ ここまで ▲▲

    age = st.number_input("年齢", 18, 80, 30)
    height = st.number_input("身長 (cm)", 130.0, 210.0, 170.0, step=0.1)
    weight = st.number_input("体重 (kg)", 30.0, 150.0, 60.0, step=0.1)
    fat_input = st.text_input("体脂肪率（任意）", "")

    if st.button("次へ進む →"):
        st.session_state.sex = sex
        st.session_state.age = age
        st.session_state.height = height
        st.session_state.weight = weight
        st.session_state.fat_input = fat_input
        st.session_state.page = 1
        st.experimental_rerun()

# =========================
# ページ 1 : 質問ページ
# =========================
elif st.session_state.page == 1:
    total_q = 30
    now = st.session_state.current_q
    sec, q_text = flat_questions[now]

    st.progress((now + 1) / total_q)
    st.markdown(f"<p style='text-align:center;color:#555;'>{now+1} / {total_q}</p>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:24px;font-weight:700;text-align:center;margin-top:30px;'>{q_text}</div>",
        unsafe_allow_html=True
    )

    q_key = f"Q{now}"

    # ラベル（当てはまらない・当てはまる）
    st.markdown(
        "<div style='display:flex;justify-content:space-between;margin:0 20%;font-weight:600;'>"
        "<span>当てはまらない</span><span>当てはまる</span></div>",
        unsafe_allow_html=True
    )

    # --- ラジオボタン（1〜7） ---
    ans = st.radio("", options=["1","2","3","4","5","6","7"], 
                horizontal=True, index=3, key=q_key)

    # ▼▼ 質問ページ用に ID を付ける ▼▼
    st.markdown(
        """
        <script>
        const groups = window.parent.document.querySelectorAll('div[role="radiogroup"]');
        if (groups.length > 0) {
            const target = groups[groups.length - 1];  // 最後が質問ラジオ
            target.id = "question-radio";
        }
        </script>
        """,
        unsafe_allow_html=True
    )

    # --- ナビゲーション（戻る / 次へ） ---
    st.markdown("<div class='nav-buttons'>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])

    with c1:
        if now > 0:
            if st.button("← 戻る"):
                st.session_state.current_q -= 1
                st.experimental_rerun()

    with c2:
        if st.button("次へ →"):
            st.session_state.answers[q_key] = ans
            if now < total_q - 1:
                st.session_state.current_q += 1
                st.experimental_rerun()
            else:
                st.session_state.page = 2
                st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ページ 2 : 結果ページ
# =========================
elif st.session_state.page == 2:
    st.markdown("<h2 style='text-align:center;'>診断結果</h2>", unsafe_allow_html=True)

    sex = st.session_state.sex
    age = st.session_state.age
    height = st.session_state.height
    weight = st.session_state.weight
    fat_input = st.session_state.fat_input

    bmi = weight / ((height / 100) ** 2)
    if fat_input.strip() == "":
        fat_pct = 1.20*bmi + 0.23*age - (16.2 if sex=="男性" else 5.4)
    else:
        fat_pct = float(fat_input)
    ffm = weight * (1 - fat_pct / 100)
    bmr = (13.397*weight + 4.799*height - 5.677*age + 88.362) if sex=="男性" else (9.247*weight + 3.098*height - 4.330*age + 447.593)
    burn = ffm + bmr*0.01 - fat_pct

    # 結果カード
    st.markdown(
        f"""
        <div style='background-color:#f9f9f9;padding:20px;border-radius:15px;border:1px solid #ddd;margin:20px 0;'>
        <h4 style='text-align:center;'>身体データ</h4>
        <p style='text-align:center;'>BMI：<b>{bmi:.1f}</b>　体脂肪率：<b>{fat_pct:.1f}%</b>　燃焼スコア：<b>{burn:.1f}</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # BMI棒グラフ
    fig, ax = plt.subplots(figsize=(6, 1.2))
    ax.barh([""], [bmi], color="orange")
    ax.axvline(18.5, color="blue", linestyle="--", label="やせ")
    ax.axvline(25, color="red", linestyle="--", label="肥満")
    ax.set_xlim(10, 35)
    ax.set_xlabel("BMI")
    ax.legend()
    st.pyplot(fig)

    # 燃焼スコア棒グラフ
    fig2, ax2 = plt.subplots(figsize=(6, 1.2))
    ax2.barh([""], [burn], color="orange")
    ax2.axvline(50, color="green", linestyle="--", label="平均的な燃焼スコア")
    ax2.set_xlim(0, 100)
    ax2.set_xlabel("燃焼スコア")
    ax2.legend()
    st.pyplot(fig2)

    # レーダーチャート
    df = pd.read_excel("/Users/chiakiyamaguchi/Desktop/SGSB/model/synthetic_inbody_300_with_survey.xlsx")
    overall_means = [df[[f"Q{1+i*5}", f"Q{2+i*5}", f"Q{3+i*5}", f"Q{4+i*5}", f"Q{5+i*5}"]].mean().mean() for i in range(6)]
    user_scores = [np.mean([int(st.session_state.answers[f"Q{idx}"]) for idx in range(i*5, i*5+5)]) for i in range(6)]
    categories = ["食事","運動","飲酒","仕事","睡眠","ストレス"]
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist() + [0]
    fig3 = plt.figure(figsize=(6,6))
    ax3 = plt.subplot(111, polar=True)
    ax3.set_ylim(1,7)
    ax3.plot(angles, overall_means+[overall_means[0]], color="skyblue", linewidth=2, label="平均")
    ax3.fill(angles, overall_means+[overall_means[0]], color="skyblue", alpha=0.15)
    ax3.plot(angles, user_scores+[user_scores[0]], color="orange", linewidth=2.5, label="あなた")
    ax3.fill(angles, user_scores+[user_scores[0]], color="orange", alpha=0.3)
    plt.xticks(angles[:-1], categories)
    ax3.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
    st.pyplot(fig3)
