import streamlit as st
import pandas as pd

# ================== إعداد الصفحة ==================
st.set_page_config(page_title="Smart Study AI", page_icon="📚", layout="centered")

# ================== تصميم الألوان ==================
st.markdown("""
<style>

.stApp {
    background-color: #e6e6e6;
}

/* الصناديق */
.block-container {
    background-color: transparent;
}

div[data-testid="stMetric"],
div.stAlert {
    background-color: #111 !important;
    color: white !important;
    border-radius: 12px;
    padding: 12px;
}

/* النصوص */
h1, h2, h3, h4, h5, h6, label, p {
    color: white !important;
}

/* الأزرار */
.stButton>button {
    background-color: black;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
}

</style>
""", unsafe_allow_html=True)

# ================== عنوان ==================
st.title("📚 Smart Study AI Assistant")
st.caption("Developed by Sameh Mohamed")

st.write("مساعد ذكي لتنظيم وقت المذاكرة حسب درجاتك وصعوبة المواد")

# ================== إدخال البيانات ==================
num_subjects = st.number_input("عدد المواد", min_value=1, max_value=10, step=1)

subjects = []

difficulty_map = {
    "سهل": 1,
    "متوسط": 2,
    "صعب": 3
}

for i in range(num_subjects):
    st.subheader(f"المادة {i+1}")

    name = st.text_input("اسم المادة", key=f"name{i}")
    grade = st.number_input("درجتك من 100", 0, 100, key=f"grade{i}")
    diff_text = st.selectbox("الصعوبة", ["سهل", "متوسط", "صعب"], key=f"diff{i}")

    subjects.append({
        "name": name,
        "grade": grade,
        "difficulty": difficulty_map[diff_text]
    })

# ================== الحساب الذكي ==================
if st.button("احسب خطة المذاكرة الذكية"):

    df = pd.DataFrame(subjects)

    if len(df) == 0 or df["name"].eq("").all():
        st.warning("من فضلك أدخل المواد")
    else:
        # كل ما الدرجة أقل → احتياج أعلى
        df["need"] = 100 - df["grade"]

        # وزن ذكي = الاحتياج × الصعوبة
        df["weight"] = df["need"] * df["difficulty"]

        total_weight = df["weight"].sum()

        total_minutes = 300  # 5 ساعات مذاكرة إجمالي

        df["study_minutes"] = (df["weight"] / total_weight * total_minutes).round()

        st.success("✅ تم إنشاء خطة المذاكرة")

        for _, row in df.iterrows():
            st.metric(
                label=row["name"],
                value=f"{int(row['study_minutes'])} دقيقة"
            )

        st.info("الخطة مبنية على ضعف الدرجة ومستوى صعوبة المادة — توزيع ذكي للوقت")

