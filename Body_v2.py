import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================
# 性別セレクター（カスタムボタン）
# =============================================================
def gender_selector():
    st.write("**性別**")

    gender = st.radio(
        "",
        ["男性", "女性"],
        key="gender",
        horizontal=True
    )

    st.markdown("""
    <style>
    /* 横並び中央配置 */
    .gender-radio [role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        gap: 60px !important;
        margin: 15px 0 !important;
    }
    /* ラジオ本体を消す */
    .gender-radio input[type="radio"] { display: none !important; }

    /* ボタン風ラベル */
    .gender-radio label {
        padding: 10px 40px;
        border-radius: 12px;
        border: 2px solid #FF8C00;
        color: #FF8C00;
        font-size: 22px;
        font-weight: 700;
        cursor: pointer;
        background: white;
    }
    /* 選択時 */
    .gender-radio input[type="radio"]:checked + label {
        background: #FF8C00 !important;
        color: white !important;
    }
    </style>

    <script>
    const gs = window.parent.document.querySelectorAll('div[role="radiogroup"]');
    if (gs.length > 0) { gs[gs.length-1].classList.add("gender-radio"); }
    </script>
    """, unsafe_allow_html=True)

    return gender

# =============================================================
# 共通 CSS（背景・入力欄・ボタン）
# =============================================================
st.markdown("""
<style>

body, .main, .block-container {
    background: #FFFFFF !important;
    color: #000 !important;
}

/* 入力欄 */
.stNumberInput input, .stTextInput input {
    background: white !important;
    border: 1px solid #CCC !important;
    border-radius: 8px !important;
    color: black !important;
}

/* ナビボタン */
div.stButton > button {
    background: #FFFFFF !important;
    color: #FF8C00 !important;
    border: 2px solid #FF8C00 !important;
    border-radius: 10px !important;
    padding: 10px 25px !important;
    font-weight: 700;
}
div.stButton > button:hover {
    background: #FF8C00 !important;
    color: white !important;
}

/* 質問ラジオ（1〜7）中央揃え */
.question-radio [role="radiogroup"] {
    display: flex !important;
    justify-content: center !important;
    gap: 45px !important;
    margin-top: 25px !important;
}
.question-radio label {
    font-size: 22px !important;
    font-weight: 700 !important;
}
.question-radio input[type="radio"] {
    width: 28px !important;
    height: 28px !important;
}

</style>
""", unsafe_allow_html=True)

# =============================================================
# 状態管理
# =============================================================
if "page" not in st.session_state:
    st.session_state.page = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# =============================================================
# 質問定義
# =============================================================
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
        "運動を習慣として長期間継続できている",
        "日常生活で意識的に体を動かしている",
        "筋トレやストレッチなどを行っている",
        "座位時間を減らす工夫をしている",
    ]),
    ("飲酒", [
        "飲酒頻度は適切である",
        "飲酒量は適量に抑えている",
        "飲酒をストレス発散に使わない",
        "平日の飲酒を控えている",
        "休肝日を設けている",
    ]),
    ("仕事", [
        "仕事量と休息のバランスが取れている",
        "業務中に過度なストレスを感じない",
        "長時間のデスクワークでも適度に休憩を取っている",
        "仕事による疲労を感じにくい",
        "勤務後や休日にリフレッシュできている",
    ]),
    ("睡眠", [
        "就寝・起床時間は一定である",
        "睡眠時間は十分に確保できている",
        "寝つきが良い",
        "夜中に起きてもすぐ眠れる",
        "朝の目覚めが良い",
    ]),
    ("ストレス", [
        "強いストレスを感じることが少ない",
        "気分の落ち込みが少ない",
        "人間関係のストレスが少ない",
        "意欲や活力を保てている",
        "ストレスをうまくコントロールできている",
    ]),
]
flat_questions = [(sec, q) for sec, qs in question_sections for q in qs]


# =============================================================
# ページ 0：身体データ入力
# =============================================================
if st.session_state.page == 0:
    st.markdown("<h1 style='text-align:center;'>メタボリズム9</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>【身体データ入力】</h3>", unsafe_allow_html=True)

    sex = gender_selector()
    age = st.number_input("年齢", 18, 80, 30)
    height = st.number_input("身長 (cm)", 130.0, 210.0, 170.0)
    weight = st.number_input("体重 (kg)", 30.0, 150.0, 60.0)
    fat_input = st.text_input("体脂肪率（任意）")

    if st.button("次へ →"):
        st.session_state.sex = sex
        st.session_state.age = age
        st.session_state.height = height
        st.session_state.weight = weight
        st.session_state.fat_input = fat_input
        st.session_state.page = 1
        st.rerun()


# =============================================================
# ページ 1：質問ページ
# =============================================================
elif st.session_state.page == 1:
    total_q = 30
    now = st.session_state.current_q
    sec, q_text = flat_questions[now]

    st.progress((now + 1) / total_q)
    st.markdown(f"<p style='text-align:center;'> {now+1} / {total_q} </p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>{q_text}</h3>", unsafe_allow_html=True)

    q_key = f"Q{now}"
    ans = st.radio(
        "",
        ["1","2","3","4","5","6","7"],
        horizontal=True,
        index=3,
        key=q_key
    )

    # ラジオに class を付与
    st.markdown("""
    <script>
    const gs = window.parent.document.querySelectorAll('div[role="radiogroup"]');
    if (gs.length > 0) { gs[gs.length-1].classList.add("question-radio"); }
    </script>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("← 戻る"):
        if now > 0:
            st.session_state.current_q -= 1
            st.rerun()

    if col2.button("次へ →"):
        st.session_state.answers[q_key] = ans
        if now < total_q - 1:
            st.session_state.current_q += 1
            st.rerun()
        else:
            st.session_state.page = 2
            st.rerun()


# =============================================================
# ページ 2：結果ページ
# =============================================================
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
    bmr = (13.397*weight + 4.799*height - 5.677*age + 88.362) if sex=="男性" else \
          (9.247*weight + 3.098*height - 4.330*age + 447.593)
    burn = ffm + bmr*0.01 - fat_pct

    st.write(f"### 身体データ")
    st.write(f"**BMI:** {bmi:.1f}　/　**体脂肪率:** {fat_pct:.1f}%　/　**燃焼スコア:** {burn:.1f}")

    # BMI グラフ（横棒）
    fig, ax = plt.subplots(figsize=(7, 1.8))
    ax.barh([""], [bmi], color="#FFA500")
    ax.axvline(18.5, color="blue", linestyle="--")
    ax.axvline(25, color="red", linestyle="--")
    ax.set_xlim(10, 35)
    ax.set_yticks([])
    st.pyplot(fig)
