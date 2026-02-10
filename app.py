import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Study AI", page_icon="📚")
st.markdown("""
<style>
.stApp {
    background-color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- ألوان مريحة ----------
st.markdown("""
<style>
.main {background-color:#f8fafc;}
h1 {color:#2563eb; text-align:center;}
.stButton>button {
 background:#10b981;
 color:white;
 border-radius:10px;
 height:3em;
 font-size:18px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 المساعد الدراسي الذكي")

num_subjects = st.number_input("عدد المواد", 1, 12, 3)

diff_map = {"سهل":1, "متوسط":2, "صعب":3}

rows = []

for i in range(int(num_subjects)):
    st.subheader(f"المادة {i+1}")

    name = st.text_input("اسم المادة", key=i)
    score = st.number_input("درجتك", 0, 100, key=f"s{i}")
    total = st.number_input("الدرجة النهائية", 1, 100, key=f"t{i}")
    diff = st.selectbox("الصعوبة", ["سهل","متوسط","صعب"], key=f"d{i}")

    if name.strip() != "":
        percent = score / total * 100
        weakness = max(1, 100 - percent)   # يمنع صفر
        weight = weakness * diff_map[diff]

        rows.append([name, percent, weight])

hours = st.number_input("ساعات المذاكرة", 1, 16, 4)

# ---------- الحساب ----------
if st.button("احسب الخطة"):

    if not rows:
        st.warning("ادخل مواد على الأقل")
        st.stop()

    df = pd.DataFrame(rows, columns=["المادة","النسبة","الوزن"])

    total_weight = df["الوزن"].sum()

    if total_weight == 0:
        total_weight = 1   # حماية من القسمة على صفر

    total_minutes = hours * 60

    df["دقائق"] = (df["الوزن"] / total_weight) * total_minutes
    df["دقائق"] = df["دقائق"].round()

    st.subheader("⏱️ خطة المذاكرة")

    for _,r in df.iterrows():
        st.success(f"{r['المادة']} — {int(r['دقائق'])} دقيقة")

    st.subheader("📊 مستوى الدرجات")
    st.bar_chart(df.set_index("المادة")["النسبة"])
