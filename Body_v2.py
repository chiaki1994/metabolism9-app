import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================
# カスタム：性別ボタン
# =============================================================
def gender_selector():
    st.write("**性別**")

    selection = st.radio(
        "",
        ["男性", "女性"],
        key="gender",
        horizontal=True
    )

    # カスタムCSS
    st.markdown("""
        <style>
        .gender-radio div[role="radiogroup"] {
            display: flex !important;
            justify-content: center !important;
            gap: 60px !important;
            margin: 20px auto !important;
        }
        .gender-radio input[type="radio"] { display: none !important; }
        .gender-radio label {
            padding: 10px 40px;
            border-radius: 12px;
            border: 2px solid #FF8C00;
            font-size: 22px;
            font-weight: 700;
            background: white;
            color: #FF8C00;
            cursor: pointer;
        }
        .gender-radio input[type="radio"]:checked + label {
            background: #FF8C00 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # radiogroup を gender-radio クラスに置き換える
    st.markdown("""
        <script>
        const groups = window.parent.document.querySelectorAll('div[role="radiogroup"]');
        if (groups.length > 0) {
            const g = groups[groups.length - 1];
            g.classList.add('gender-radio');
        }
        </script>
    """, unsafe_allow_html=True)

    return selection


# =============================================================
# CSS（全体デザイン）
# =============================================================
st.markdown("""
<style>

body, .main, .block-container {
    background-color: white !important;
    color: black !important;
}

h1, h2, h3, h4, h5, p, span, div, label {
    color: black !important;
}

/* 入力欄 */
.stNumberInput input, .stTextInput input {
    background-color: white !important;
    color: black !important;
    border-radius: 8px !important;
    border: 1px solid #ccc !important;
}

/* ボタン */
div.stButton > button {
    display: block;
    margin: 30px auto 0 auto;
    background-color: white !important;
    color: #FF8C00 !important;
    border: 2px solid #FF8C00 !important;
    border-radius: 10px !important;
    padding: 10px 25px !important;
    font-weight: 700;
}
div.stButton > button:hover {
    background-color: #FF8C00 !important;
    color: white !important;
}

/* ナビゲーション */
.nav-buttons {
    display: flex;
    justify-content: center;
    gap: 80px;
    margin-top: 30px;
}

/* 質問のカスタムラジオ */
.question-radio div[role="radiogroup"] {
    display: flex !important;
    justify-content: center !important;
    gap: 40px !important;
    margin-top: 20px !important;
}

.question-radio input[type="radio"] {
    width: 26px !important;
    height: 26px !important;
}

.question-radio label {
    font-size: 24px !important;
    font-weight: 700 !important;
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
        "間食を控えている",
        "揚げ物を控えている"
    ]),
    ("運動", [
        "週に3回以上、運動している",
        "運動を習慣化できている",
        "日常で体を動かしている",
        "筋トレなどを行っている",
        "座位時間を減らしている"
    ]),
    ("飲酒", [
        "飲酒頻度は適切である",
        "飲む量を抑えている",
        "飲酒をストレス発散に使わない",
        "平日飲酒を控えている",
        "休肝日がある"
    ]),
    ("仕事", [
        "仕事と休息のバランスが取れている",
        "過度なストレスがない",
        "適度に休憩を取る",
        "仕事で疲れにくい",
        "休日にリフレッシュできている"
    ]),
    ("睡眠", [
        "就寝・起床時間が一定",
        "睡眠時間は十分",
        "寝つきが良い",
        "夜中もすぐ眠れる",
        "朝の目覚めが良い"
    ]),
    ("ストレス", [
        "強いストレスを感じにくい",
        "気分の落ち込みが少ない",
        "人間関係のストレスが少ない",
        "意欲を保てている",
        "ストレス管理ができている"
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

    if st.button("次へ進む →"):
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

    st.progress((now+1)/total_q)
    st.markdown(f"<p style='text-align:center;color:#555;'>{now+1} / {total_q}</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>{q_text}</h3>", unsafe_allow_html=True)

    q_key = f"Q{now}"

    # 質問ラジオ（1〜7）
    ans = st.radio(
        "",
        ["1","2","3","4","5","6","7"],
        horizontal=True,
        index=3,
        key=q_key
    )

    # カスタムCSS適用
    st.markdown("""
        <script>
        const groups = window.parent.document.querySelectorAll('div[role="radiogroup"]');
        if (groups.length > 0) {
            groups[groups.length - 1].classList.add('question-radio');
        }
        </script>
    """, unsafe_allow_html=True)

    st.markdown("<div class='nav-buttons'>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if now > 0:
            if st.button("← 戻る"):
                st.session_state.current_q -= 1
                st.rerun()

    with c2:
        if st.button("次へ →"):
            st.session_state.answers[q_key] = ans
            if now < total_q - 1:
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.session_state.page = 2
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


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

    bmi = weight / ((height/100)**2)

    if fat_input.strip() == "":
        fat_pct = 1.20*bmi + 0.23*age - (16.2 if sex=="男性" else 5.4)
    else:
        fat_pct = float(fat_input)

    ffm = weight * (1 - fat_pct/100)
    bmr = (13.397*weight + 4.799*height - 5.677*age + 88.362) if sex=="男性" else \
          (9.247*weight + 3.098*height - 4.330*age + 447.593)
    burn = ffm + bmr*0.01 - fat_pct

    st.write("### 身体データ")
    st.write(f"**BMI:** {bmi:.1f} / **体脂肪率:** {fat_pct:.1f}% / **燃焼スコア:** {burn:.1f}")

    # グラフ（フォントなし OK）
    fig, ax = plt.subplots(figsize=(6, 1.2))
    ax.barh([""], [bmi], color="orange")
    ax.axvline(18.5, color="blue", linestyle="--")
    ax.axvline(25, color="red", linestyle="--")
    st.pyplot(fig)
