import streamlit as st
import pandas as pd

# ---------- إعداد الصفحة ----------
st.set_page_config(page_title="Smart Study AI", page_icon="📚", layout="centered")

# ---------- ستايل وألوان مريحة ----------
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
h1 {
    color: #2563eb;
    text-align:center;
}
.stNumberInput label, .stTextInput label, .stSelectbox label {
    color: #334155 !important;
    font-weight: 600;
}
.stButton>button {
    background-color: #10b981;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- عنوان ----------
st.title("🎓 Smart Study AI Planner")

# ---------- إدخال ----------
num_subjects = st.number_input("عدد المواد", 1, 12, 3)

subjects = []
levels = []
priorities = []

level_map = {
    "سهل": 1,
    "متوسط": 2,
    "صعب": 3
}

for i in range(int(num_subjects)):
    st.subheader(f"المادة {i+1}")

    name = st.text_input("اسم المادة", key=f"name{i}")
    level_text = st.selectbox("درجة الصعوبة", ["سهل","متوسط","صعب"], key=f"lvl{i}")
    priority = st.selectbox("الأولوية", ["منخفضة","متوسطة","عالية"], key=f"pri{i}")

    subjects.append(name)
    levels.append(level_map[level_text])

    pri_map = {
        "منخفضة": 1,
        "متوسطة": 2,
        "عالية": 3
    }
    priorities.append(pri_map[priority])

total_hours = st.number_input("عدد ساعات المذاكرة اليوم", 1, 16, 4)

# ---------- الحساب ----------
if st.button("📊 احسب خطة المذاكرة"):

    df = pd.DataFrame({
        "subject": subjects,
        "difficulty": levels,
        "priority": priorities
    })

    # الوزن = صعوبة × أولوية
    df["weight"] = df["difficulty"] * df["priority"]

    total_weight = df["weight"].sum()
    total_minutes = total_hours * 60

    df["minutes"] = (df["weight"] / total_weight) * total_minutes
    df["minutes"] = df["minutes"].round().astype(int)

    st.subheader("⏱️ التوزيع الذكي للمذاكرة")

    for _, row in df.iterrows():
        st.success(f"{row['subject']} — {row['minutes']} دقيقة")

    st.info("التوزيع تم حسب الصعوبة + الأولوية")
