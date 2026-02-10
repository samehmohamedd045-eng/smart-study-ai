import streamlit as st
import pandas as pd

# ---------- إعداد الصفحة ----------
st.set_page_config(page_title="Smart Study AI", page_icon="🎓", layout="centered")

st.markdown("""
<style>
.main {background-color: #0f172a;}
h1 {color: #22d3ee; text-align:center;}
.stNumberInput label, .stTextInput label, .stSelectbox label {
    color: #e5e7eb !important;
}
.stButton>button {
    background-color: #22c55e;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------- العنوان ----------
st.title("📚 Smart Study AI Planner")

# ---------- إدخال البيانات ----------
num_subjects = st.number_input("عدد المواد", min_value=1, max_value=12, step=1)

subjects = []
priorities = []
difficulties = []

for i in range(int(num_subjects)):
    st.subheader(f"المادة {i+1}")

    name = st.text_input("اسم المادة", key=f"name{i}")
    priority = st.selectbox("الأولوية", [1,2,3,4,5], key=f"p{i}")
    difficulty = st.selectbox("الصعوبة", [1,2,3], key=f"d{i}")

    subjects.append(name)
    priorities.append(priority)
    difficulties.append(difficulty)

total_hours = st.number_input("عدد ساعات المذاكرة المتاحة اليوم", min_value=1, max_value=16, step=1)

# ---------- الحساب ----------
if st.button("احسب خطة المذاكرة"):

    df = pd.DataFrame({
        "subject": subjects,
        "priority": priorities,
        "difficulty": difficulties
    })

    # وزن = أولوية × صعوبة
    df["weight"] = df["priority"] * df["difficulty"]

    total_weight = df["weight"].sum()

    total_minutes = total_hours * 60

    df["minutes"] = (df["weight"] / total_weight) * total_minutes
    df["minutes"] = df["minutes"].round().astype(int)

    # ---------- عرض النتائج ----------
    st.subheader("⏱️ خطة المذاكرة المقترحة")

    for _, row in df.iterrows():
        st.write(f"✅ {row['subject']} : {row['minutes']} دقيقة")

    st.success("تم توزيع الوقت حسب الأولوية والصعوبة بنجاح 👍")
