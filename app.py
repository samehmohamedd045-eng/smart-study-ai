import streamlit as st
import pandas as pd

# ================= إعداد الصفحة =================
st.set_page_config(
    page_title="Smart Study AI",
    page_icon="📚",
    layout="centered"
)

# ================== تصميم الألوان ==================
st.markdown("""
<style>

.stApp {
    background-color: #8f8f8f;
}

/* النص */
html, body, [class*="css"] {
    color: black;
}

/* كروت النتائج */
div[data-testid="stMetric"] {
    background-color: white;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.25);
}

/* الأزرار */
.stButton>button {
    background-color: white;
    color: black;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ================== العنوان ==================
st.title("📚 Smart Study AI Assistant")
st.caption("Developed by المهندس سامح")

st.write("مساعد ذكي لتنظيم وقت المذاكرة حسب درجاتك ومستوى صعوبة المواد")

# ================== إدخال البيانات ==================
num_subjects = st.number_input("عدد المواد", 1, 12)

difficulty_map = {
    "سهل": 1,
    "متوسط": 2,
    "صعب": 3
}

data = []

for i in range(num_subjects):
    st.subheader(f"المادة {i+1}")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("اسم المادة", key=f"name{i}")

    with col2:
        grade = st.number_input("درجتك من 100", 0, 100, key=f"grade{i}")

    diff_text = st.selectbox(
        "مستوى الصعوبة",
        ["سهل", "متوسط", "صعب"],
        key=f"diff{i}"
    )

    data.append({
        "name": name,
        "grade": grade,
        "difficulty": difficulty_map[diff_text]
    })

# ================== الحساب الذكي ==================
if st.button("إنشاء خطة المذاكرة الذكية"):

    df = pd.DataFrame(data)

    if df["name"].str.strip().eq("").all():
        st.warning("من فضلك أدخل أسماء المواد")
        st.stop()

    df["need"] = 100 - df["grade"]
    df["weight"] = df["need"] * df["difficulty"]

    total_weight = df["weight"].sum()

    if total_weight == 0:
        st.error("لا توجد مواد تحتاج وقت مذاكرة")
        st.stop()

    TOTAL_MINUTES = 300  # إجمالي وقت المذاكرة

    df["study_minutes"] = (df["weight"] / total_weight * TOTAL_MINUTES).round()

    st.success("✅ تم إنشاء خطة مذاكرة ذكية")

    for _, row in df.iterrows():
        if row["name"].strip():
            st.metric(
                label=row["name"],
                value=f"{int(row['study_minutes'])} دقيقة"
            )

    st.info("التوزيع يعتمد على ضعف الدرجة × مستوى الصعوبة")

# ================== About ==================
st.divider()

st.header("ℹ️ About / عن المشروع")

st.write("""
Smart Study AI هو مساعد دراسة ذكي يساعد الطلاب على تنظيم وقت المذاكرة
بناءً على درجاتهم ومستوى صعوبة كل مادة.

آلية العمل:
يتم حساب احتياج كل مادة = ضعف الدرجة
ثم حساب وزن = الاحتياج × الصعوبة
ثم توزيع الوقت الكلي بشكل نسبي ذكي.

التقنيات المستخدمة:
Python – Streamlit – Pandas

إعداد وتطوير: المهندس سامح
""")
