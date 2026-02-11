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

/* النص العام أسود */
h1,h2,h3,h4,h5,h6,p,label {
    color: black !important;
}

/* إجبار نص selectbox يكون أبيض */
div[data-baseweb="select"] * {
    color: white !important;
}

/* زر */
.stButton>button {
    background-color: white;
    color: black;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------- عنوان ----------
st.title("🧠 Sameh Smart Study Assistant")
st.caption("Developed by Sameh Mohamed — Smart Study AI Project")

page = st.radio("القائمة", ["المخطط الذكي", "About المشروع"])

# =========================
# المخطط الذكي
# =========================
if page == "المخطط الذكي":

    st.write("تحليل الدرجات + الصعوبة = توزيع وقت مذاكرة ذكي")

    with st.expander("كيف يعمل النظام؟"):
        st.write("""
        نحسب نسبة درجتك  
        نحدد مستوى الضعف  
        نضرب في معامل الصعوبة  
        نحسب وزن لكل مادة  
        نوزع الوقت حسب الوزن
        """)

    num_subjects = st.number_input("عدد المواد", 1, 12, 3)

    diff_map = {"سهل":1, "متوسط":2, "صعب":3}
    rows = []

    for i in range(int(num_subjects)):
        st.subheader(f"المادة {i+1}")

        name = st.text_input("اسم المادة", key=f"n{i}")
        score = st.number_input("درجتك", 0, 100, key=f"s{i}")
        total = st.number_input("الدرجة النهائية", 1, 100, key=f"t{i}")
        diff = st.selectbox("الصعوبة", ["سهل","متوسط","صعب"], key=f"d{i}")

        if name.strip():
            percent = score / total * 100
            weakness = max(1, 100 - percent)
            weight = weakness * diff_map[diff]
            rows.append([name, percent, weight])

    hours = st.number_input("ساعات المذاكرة", 1, 16, 4)

    if st.button("احسب الخطة"):

        if not rows:
            st.warning("ادخل مواد")
            st.stop()

        df = pd.DataFrame(rows, columns=["المادة","النسبة","الوزن"])

        total_weight = df["الوزن"].sum()
        total_minutes = hours * 60

        df["دقائق"] = (df["الوزن"]/total_weight)*total_minutes
        df["دقائق"] = df["دقائق"].round()

        df = df.sort_values("دقائق", ascending=False)

        st.subheader("⏱️ الخطة")

        for _, r in df.iterrows():
            st.markdown(f"""
            <div style="
                background:white;
                padding:15px;
                border-radius:12px;
                margin-bottom:10px;
                color:black;">
                <h3>📘 {r['المادة']}</h3>
                <p>⏱️ {int(r['دقائق'])} دقيقة</p>
                <p>📊 {round(r['النسبة'],1)}%</p>
            </div>
            """, unsafe_allow_html=True)

        top = df.iloc[0]["المادة"]
        st.info(f"🎯 ابدأ بمادة: {top}")

        st.bar_chart(df.set_index("المادة")["النسبة"])

# =========================
# About
# =========================
else:
    st.header("📘 About")

    st.write("""
    Sameh Smart Study Assistant

    مساعد مذاكرة ذكي يعتمد على تحليل الأداء
    لتوزيع وقت المذاكرة.

    التقنيات:
    Python + Streamlit + Pandas

    Developed by Sameh Mohamed
    """)
