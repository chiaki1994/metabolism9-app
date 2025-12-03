import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# =========================
# 日本語フォント設定
# =========================
font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
fm.fontManager.addfont(font_path)
plt.rcParams["font.family"] = "Hiragino Sans"
plt.rcParams["axes.unicode_minus"] = False


# =========================
# BurnScore 計算
# =========================
def calc_burnscore(ffm, bmr, fat_pct):
    return ffm + bmr * 0.01 - fat_pct


# =========================
# 体脂肪率推定式
# =========================
def estimate_body_fat(bmi, age, sex):
    if sex == "男性":
        return 1.20 * bmi + 0.23 * age - 16.2
    else:
        return 1.20 * bmi + 0.23 * age - 5.4


# =========================
# 9分類タイプ
# =========================
type_names = {
    (0,0): "スリム・低燃焼型",
    (0,1): "スリム・標準燃焼型",
    (0,2): "スリム・高燃焼型",
    (1,0): "ミドル・低燃焼型",
    (1,1): "ミドル・標準燃焼型",
    (1,2): "ミドル・高燃焼型",
    (2,0): "がっちり・低燃焼型",
    (2,1): "がっちり・標準燃焼型",
    (2,2): "がっちり・高燃焼型",
}

type_desc = {
    "スリム・低燃焼型": "体型はスリムですが燃焼効率がやや低め。軽い筋トレとタンパク質補給が効果的です。",
    "スリム・標準燃焼型": "健康的なスリム体型。睡眠と食事の質を整えるとさらに安定します。",
    "スリム・高燃焼型": "高い代謝を持つスリムタイプ。栄養不足に注意して活動を続けましょう。",
    "ミドル・低燃焼型": "標準体型だが燃焼が低め。日常の軽い運動でも代謝改善が期待できます。",
    "ミドル・標準燃焼型": "体型・代謝ともにバランスが取れた健康型です。",
    "ミドル・高燃焼型": "動ける標準体型。運動と食事のバランスでさらなる健康増進が期待できます。",
    "がっちり・低燃焼型": "筋肉量はあるが代謝が伸びにくいタイプ。ストレッチと休息が重要です。",
    "がっちり・標準燃焼型": "しっかりした体型で代謝も安定。食事コントロールが鍵です。",
    "がっちり・高燃焼型": "代謝の非常に高いパワフル体型。栄養補給と疲労管理が重要です。",
}


# =========================
# ① タイトル
# =========================
st.markdown("""
    <h1 style='text-align: center; font-size: 44px;'>メタボリズム9</h1>
    <h3 style='text-align: center; font-size: 22px; color: #666; margin-top: -10px;'>（Metabolism-9）</h3>
    <p style='text-align: center; font-size: 18px; color: #333; margin-top: -5px;'>
        あなたの代謝特性を9タイプに分類します。
    </p>
""", unsafe_allow_html=True)



# =========================
# ② 身体データ入力（先に表示）
# =========================
st.subheader("身体データ入力")

sex = st.selectbox("性別", ["男性", "女性"])
age = st.number_input("年齢", 18, 80, 30)
height = st.number_input("身長 (cm)", 130.0, 210.0, 170.0, step=0.1, format="%.1f")
weight = st.number_input("体重 (kg)", 30.0, 150.0, 60.0, step=0.1, format="%.1f")
fat_input = st.text_input("体脂肪率（任意・空欄OK）", "")



# ============================================================
# ③ 生活習慣 質問票（30問）
# ============================================================
st.markdown("---")
st.subheader("生活習慣チェック（30問）")

questions = {
    "① 食事（Q1〜Q5）": [
        "Q1. 朝食をほぼ毎日食べている。",
        "Q2. 食事内容のバランス（主食・主菜・副菜）を意識している。",
        "Q3. 野菜を毎日十分に摂取できている。",
        "Q4. 間食（スナック・甘いもの・清涼飲料水）を控えている。",
        "Q5. 揚げ物や脂っこい食事を控えるようにしている。",
    ],

    "② 運動（Q6〜Q10）": [
        "Q6. 週あたりの運動頻度は十分に確保できている。（1=週0回, 4=週2〜3回, 7=週5回以上）",
        "Q7. 汗ばむ程度の運動（中等度〜やや強度）を定期的に行っている。",
        "Q8. 日常生活の中でも意識して体を動かしている。",
        "Q9. 筋トレやストレッチなど、体のケアを継続できている。",
        "Q10. 長時間座りっぱなしにならないように工夫している。",
    ],

    "③ 飲酒（Q11〜Q15）": [
        "Q11. 飲酒頻度（1＝飲まない、2＝月1、3＝週1、4＝週2〜3、5＝ほぼ毎日、6＝毎日、7＝毎日かつ多め）",
        "Q12. 飲む量は適量の範囲で抑えられている。",
        "Q13. ストレス発散のために飲酒することが少ない。",
        "Q14. 平日の飲酒を控えるようにしている。",
        "Q15. 飲まない日（休肝日）を設けるようにしている。",
    ],

    "④ 仕事（Q16〜Q20）": [
        "Q16. 仕事量は適切で、無理をしすぎていない。",
        "Q17. 仕事中に強いストレスを感じることは少ない。",
        "Q18. デスクワークが長い日でも、適度に体を動かしている。",
        "Q19. 肉体労働の負荷や身体的疲労をうまく管理できている。",
        "Q20. 仕事と休息のバランスを保つことができている。",
    ],

    "⑤ 睡眠（Q21〜Q25）": [
        "Q21. 就寝時間と起床時間のリズムが安定している。",
        "Q22. 睡眠時間は十分に確保できている。",
        "Q23. 寝つきは良いほうである。",
        "Q24. 夜中に目覚めても、比較的すぐに眠りに戻れる。",
        "Q25. 翌朝、しっかり休息できたと感じることが多い。",
    ],

    "⑥ ストレス・メンタル（Q26〜Q30）": [
        "Q26. 日常生活で強いストレスを感じることは少ない。",
        "Q27. 気分の落ち込みや無気力感を感じることは少ない。",
        "Q28. 人間関係に大きなストレスを感じることは少ない。",
        "Q29. 意欲や活力を保てていると感じる。",
        "Q30. ストレスを自分でうまくコントロールできている。",
    ],
}

responses = {}

for category, qs in questions.items():
    with st.expander(category):
        for q in qs:
            responses[q] = st.slider(q, 1, 7, 4)




# ============================================================
# ④ 診断ボタン（中央・大きく）
# ============================================================
st.markdown("""
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <style>
            div.stButton > button:first-child {
                font-size: 22px !important;
                padding: 12px 40px !important;
                background-color: #ff7f00 !important;
                color: white !important;
                border-radius: 10px !important;
            }
        </style>
    </div>
""", unsafe_allow_html=True)

button_clicked = st.button("診断する")



# ============================================================
# ⑤ 診断結果（Metabolism-9）
# ============================================================
if button_clicked:

    # -----------------------------
    # BMI / 体脂肪
    # -----------------------------
    bmi = weight / ((height / 100)**2)

    if fat_input.strip() == "":
        fat_pct = estimate_body_fat(bmi, age, sex)
        fat_from = "（推定値）"
    else:
        fat_pct = float(fat_input)
        fat_from = "（入力値）"

    ffm = weight * (1 - fat_pct / 100)

    # -----------------------------
    # BMR
    # -----------------------------
    if sex == "男性":
        bmr = 13.397 * weight + 4.799 * height - 5.677 * age + 88.362
    else:
        bmr = 9.247 * weight + 3.098 * height - 4.330 * age + 447.593

    burn = calc_burnscore(ffm, bmr, fat_pct)

    bmi_bin = np.digitize([bmi], [18.5, 25])[0]
    burn_bin = np.digitize([burn], [40, 60])[0]

    user_type = type_names[(bmi_bin, burn_bin)]
    user_desc = type_desc[user_type]


    st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            <h2 style="font-size: 32px;">診断結果</h2>
            <p style="font-size: 26px;">BMI：<b>{bmi:.1f}</b></p>
            <p style="font-size: 26px;">体脂肪率：<b>{fat_pct:.1f}%</b> {fat_from}</p>
            <p style="font-size: 26px;">燃焼スコア：<b>{burn:.1f}</b></p>
            <p style="font-size: 30px; color:#ff6600;"><b>{user_type}</b></p>
            <p style="font-size: 20px; color:#444;">{user_desc}</p>
        </div>
    """, unsafe_allow_html=True)



    # ============================================================
    # ⑥ グラフ（BMI × 燃焼スコア）
    # ============================================================
    fig, ax = plt.subplots(figsize=(7, 6))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    bmi_low, bmi_high = 18.5, 25
    burn_low, burn_high = 40, 60

    ax.axvspan(bmi_low, bmi_high, color="gray", alpha=0.08)
    ax.axhspan(burn_low, burn_high, color="gray", alpha=0.08)

    ax.axvline(bmi_low, linestyle="--", color="gray", alpha=0.4)
    ax.axvline(bmi_high, linestyle="--", color="gray", alpha=0.4)
    ax.axhline(burn_low, linestyle="--", color="gray", alpha=0.4)
    ax.axhline(burn_high, linestyle="--", color="gray", alpha=0.4)

    ax.scatter(bmi, burn, color="orange", s=300, edgecolor="black", linewidth=1)

    ax.set_xlim(10, 35)
    ax.set_ylim(0, 100)

    offset_y = -30
    ax.annotate("スリム", xy=((10+bmi_low)/2, 0), xytext=(0, offset_y),
                textcoords="offset points", ha="center", fontsize=8, color="#555")
    ax.annotate("ミドル", xy=((bmi_low+bmi_high)/2, 0), xytext=(0, offset_y),
                textcoords="offset points", ha="center", fontsize=8, color="#555")
    ax.annotate("がっちり", xy=((bmi_high+40)/2, 0), xytext=(0, offset_y),
                textcoords="offset points", ha="center", fontsize=8, color="#555")

    offset_x = -35
    ax.annotate("燃えにくい", xy=(10, (0+burn_low)/2), xytext=(offset_x, 0),
                textcoords="offset points", rotation=90, fontsize=8, color="#555")
    ax.annotate("標準", xy=(10, (burn_low+burn_high)/2), xytext=(offset_x, 0),
                textcoords="offset points", rotation=90, fontsize=8, color="#555")
    ax.annotate("燃えやすい", xy=(10, (burn_high+100)/2), xytext=(offset_x, 0),
                textcoords="offset points", rotation=90, fontsize=8, color="#555")

    ax.set_xlabel("BMIスコア", fontsize=12, labelpad=22)
    ax.set_ylabel("想定燃焼スコア", fontsize=12, labelpad=18)
    ax.set_title("あなたの位置（オレンジ）", fontsize=14)

    plt.subplots_adjust(bottom=0.32, left=0.34)
    st.pyplot(fig)
