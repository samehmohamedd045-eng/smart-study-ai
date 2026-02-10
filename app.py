import streamlit as st
import pandas as pd

# ---------- إعداد الصفحة ----------
st.set_page_config(page_title="Sameh Smart Study Assistant", page_icon="🧠")

# ---------- ستايل ----------
st.markdown("""
<style>
.stApp {
    background-color: #6b7280 !important;
}

h1,h2,h3,h4,h5,h6,p,label,div,span {
    color: white_attach !important;
    color: white !important;
}

.stButton>button {
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------- عنوان ----------
st.title("🧠 Sameh Smart Study Assistant")
st.caption("Developed by Sameh Mohamed — Smart Study AI Project")

st.write("الخوارزمية تعتمد على تحليل درجتك + مستوى الصعوبة لتوزيع وقت المذاكرة تلقائيًا")
with st.expander("كيف يعمل النظام الذكي؟"):
    st.write("""
    🔹 يحسب نسبة درجتك في كل مادة  
    🔹 يحدد مستوى الضعف = 100 − النسبة  
    🔹 يضرب الضعف × عامل الصعوبة  
    🔹 يوزع وقت المذاكرة حسب الوزن الناتج  
    🔹 يعطي توصية بأهم مادة تبدأ بها
    """)

# ---------- إدخال ----------
num_subjects = st.number_input("عدد المواد", 1, 12, 3)

diff_map = {"سهل":1, "متوسط":2, "صعب":3}

rows = []

for i in range(int(num_subjects)):
    st.subheader(f"المادة {i+1}")

    name = st.text_input("اسم المادة", key=f"name{i}")
    score = st.number_input("درجتك", 0, 100, key=f"s{i}")
    total = st.number_input("الدرجة النهائية", 1, 100, key=f"t{i}")
    diff = st.selectbox("الصعوبة", ["سهل","متوسط","صعب"], key=f"d{i}")

    if name.strip() != "":
        percent = score / total * 100
        weakness = max(1, 100 - percent)
        weight = weakness * diff_map[diff]
        rows.append([name, percent, weight])

hours = st.number_input("ساعات المذاكرة", 1, 16, 4)

# ---------- الحساب ----------
if st.button("احسب الخطة الذكية"):

    if not rows:
        st.warning("ادخل مواد على الأقل")
        st.stop()

    df = pd.DataFrame(rows, columns=["المادة","النسبة","الوزن"])

    total_weight = df["الوزن"].sum()
    if total_weight == 0:
        total_weight = 1

    total_minutes = hours * 60

    df["دقائق"] = (df["الوزن"] / total_weight) * total_minutes
    df["دقائق"] = df["دقائق"].round()

    st.subheader("⏱️ خطة المذاكرة")

    for _, r in df.iterrows():
        st.success(f"{r['المادة']} — {int(r['دقائق'])} دقيقة")

    # ---------- نصيحة ذكية ----------
    top_subject = df.sort_values("دقائق", ascending=False).iloc[0]["المادة"]
    st.info(f"🎯 نصيحة ذكية: ابدأ مذاكرتك اليوم بمادة {top_subject} لأنها الأعلى احتياجًا للوقت.")

    # ---------- رسم ----------
    st.subheader("📊 مستوى الدرجات")
    st.bar_chart(df.set_index("المادة")["النسبة"])
