import streamlit as st
import pandas as pd

# ---------- إعداد الصفحة ----------
st.set_page_config(page_title="Smart Study AI", page_icon="📚", layout="centered")

# ---------- ألوان مريحة ----------
st.markdown("""
<style>
.main {background-color: #f8fafc;}
h1 {color: #2563eb; text-align:center;}
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
</style>
""", unsafe_allow_html=True)

# ---------- عنوان ----------
st.title("🎓 المساعد الدراسي الذكي")

st.write("حلل درجاتك وسيتم توزيع وقت المذاكرة تلقائيًا حسب الضعف والصعوبة")

# ---------- إدخال البيانات ----------
num_subjects = st.number_input("عدد المواد", 1, 12, 3)

names=[]
scores=[]
totals=[]
diffs=[]

diff_map = {
    "سهل":1,
    "متوسط":2,
    "صعب":3
}

for i in range(int(num_subjects)):
    st.subheader(f"المادة {i+1}")

    names.append(st.text_input("اسم المادة", key=f"n{i}"))
    scores.append(st.number_input("درجتك", 0, 100, key=f"s{i}"))
    totals.append(st.number_input("الدرجة النهائية", 1, 100, key=f"t{i}"))
    diffs.append(st.selectbox("الصعوبة", ["سهل","متوسط","صعب"], key=f"d{i}"))

total_hours = st.number_input("عدد ساعات المذاكرة اليوم", 1, 16, 4)

# ---------- التحليل ----------
if st.button("📊 تحليل وبناء خطة مذاكرة"):

    data=[]

    for n,sc,to,df in zip(names,scores,totals,diffs):
        if n.strip()=="":
            continue

        percent = sc/to*100
        weakness = 100 - percent
        diff_num = diff_map[df]

        weight = weakness * diff_num
        data.append([n, percent, diff_num, weight])

    if not data:
        st.warning("ادخل مواد صحيحة")
        st.stop()

    df = pd.DataFrame(data, columns=["المادة","النسبة","الصعوبة","الوزن"])

    total_weight = df["الوزن"].sum()
    total_minutes = total_hours * 60

    df["دقائق المذاكرة"] = (df["الوزن"]/total_weight)*total_minutes
    df["دقائق المذاكرة"] = df["دقائق المذاكرة"].round().astype(int)

    df = df.sort_values("دقائق المذاكرة", ascending=False)

    # ---------- عرض ----------
    st.subheader("⏱️ خطة المذاكرة الذكية")

    for _,row in df.iterrows():
        st.success(f"{row['المادة']} — {row['دقائق المذاكرة']} دقيقة")

    st.subheader("📈 مستوى الأداء")
    st.bar_chart(df.set_index("المادة")["النسبة"])

    worst = df.iloc[0]["المادة"]
    st.info(f"🔎 أكثر مادة تحتاج تركيز: {worst}")
