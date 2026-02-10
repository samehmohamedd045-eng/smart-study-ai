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

# ---------- قائمة الصفحات ----------
page = st.radio("القائمة", ["المخطط الذكي", "About المشروع"])


# =========================
# صفحة المخطط الذكي
# =========================
if page == "المخطط الذكي":

    st.write("الخوارزمية تعتمد على تحليل درجتك + مستوى الصعوبة لتوزيع وقت المذاكرة تلقائيًا")

    with st.expander("كيف يعمل النظام الذكي؟"):
        st.write("""
        🔹 يحسب نسبة درجتك في كل مادة  
        🔹 يحدد مستوى الضعف = 100 − النسبة  
        🔹 يضرب الضعف × عامل الصعوبة  
        🔹 ينتج وزن لكل مادة  
        🔹 يوزع الوقت حسب الوزن  
        🔹 يعطي توصية بأهم مادة تبدأ بها
        """)

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

        df = df.sort_values("دقائق", ascending=False)

        st.subheader("⏱️ خطة المذاكرة")

        # ---------- عرض بالكروت ----------
        for _, r in df.iterrows():
            st.markdown(f"""
            <div style="
                background:#4b5563;
                padding:15px;
                border-radius:12px;
                margin-bottom:12px;
                box-shadow:0 4px 8px rgba(0,0,0,0.25);
            ">
                <h3>📘 {r['المادة']}</h3>
                <p>⏱️ وقت المذاكرة: {int(r['دقائق'])} دقيقة</p>
                <p>📊 مستواك: {round(r['النسبة'],1)}%</p>
            </div>
            """, unsafe_allow_html=True)

        # ---------- نصيحة ذكية ----------
        top_subject = df.iloc[0]["المادة"]
        st.info(f"🎯 نصيحة ذكية: ابدأ مذاكرتك اليوم بمادة {top_subject} لأنها الأعلى احتياجًا للوقت.")

        # ---------- رسم ----------
        st.subheader("📊 مستوى الدرجات")
        st.bar_chart(df.set_index("المادة")["النسبة"])


# =========================
# صفحة About
# =========================
elif page == "About المشروع":

    st.header("📘 About المشروع")

    st.write("""
    🧠 **Sameh Smart Study Assistant**

    مساعد دراسي ذكي يساعد الطلاب على توزيع وقت المذاكرة
    بناءً على تحليل الدرجات ومستوى صعوبة المواد.

    🔬 **فكرة الذكاء:**
    - حساب نسبة الأداء
    - تحديد مستوى الضعف
    - حساب وزن لكل مادة
    - توزيع وقت المذاكرة تلقائيًا
    - تقديم توصية ببداية المذاكرة

    ⚙️ **التقنيات المستخدمة:**
    Python — Streamlit — Pandas — Data Analysis

    👨‍💻 **تطوير:**
    Sameh Mohamed

    🎯 **هدف المشروع:**
    المذاكرة بذكاء بدل المذاكرة بعدد ساعات فقط.
    """)
