import streamlit as st
import pandas as pd

# ---------- إعدادات الصفحة ----------
st.set_page_config(
    page_title="Smart Study AI",
    page_icon="📘",
    layout="centered"
)

# ---------- ستايل الألوان ----------
st.markdown("""
<style>
.stApp {
    background-color: #e9ecef;
}
h1, h2, h3, label {
    color: #ffffff !important;
}
.block-container {
    background: #6c757d;
    padding: 2rem;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------- العنوان ----------
st.title("📘 Smart Study AI")
st.caption("تنظيم وقت المذاكرة بالدرجات — تصميم Sameh")

# ---------- إدخال عدد المواد ----------
num_subjects = st.number_input("عدد المواد", 1, 10, 5)

subjects = []
scores = []

st.subheader("✍️ اكتب المواد والدرجة")

for i in range(num_subjects):
    col1, col2 = st.columns(2)

    with col1:
        sub = st.text_input(f"اسم المادة {i+1}", key=f"s{i}")

    with col2:
        level = st.selectbox(
            f"الدرجة",
            ["سهل", "متوسط", "صعب"],
            key=f"l{i}"
        )

    if sub:
        subjects.append(sub)

        if level == "سهل":
            scores.append(1)
        elif level == "متوسط":
            scores.append(2)
        else:
            scores.append(3)

# ---------- الوقت الكلي ----------
total_hours = st.slider("⏱️ عدد ساعات المذاكرة اليوم", 1, 12, 5)

# ---------- زر الحساب ----------
if st.button("📊 احسب خطة المذاكرة"):

    if len(subjects) == 0:
        st.warning("اكتب مواد الأول")
    else:

        df = pd.DataFrame({
            "المادة": subjects,
            "الدرجة": scores
        })

        total_score = df["الدرجة"].sum()
        total_minutes = total_hours * 60

        df["دقائق المذاكرة"] = (
            df["الدرجة"] / total_score * total_minutes
        ).round().astype(int)

        st.subheader("✅ الخطة المقترحة")

        st.dataframe(df, use_container_width=True)

        st.success("جاهز للمذاكرة 💪")
