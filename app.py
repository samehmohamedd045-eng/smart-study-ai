import streamlit as st
import pandas as pd

st.title("🎓 Smart Study Assistant AI")
st.write("نظام مساعد دراسة ذكي يحلل درجاتك ويقترح جدول مذاكرة حسب الأولوية")

subjects=[]
scores=[]
totals=[]
diffs=[]

n = st.number_input("عدد المواد",1,12,5)

for i in range(n):
    st.subheader(f"مادة {i+1}")
    subjects.append(st.text_input("اسم المادة",key=f"s{i}"))
    scores.append(st.number_input("درجتك",0,100,key=f"sc{i}"))
    totals.append(st.number_input("الدرجة النهائية",1,100,key=f"t{i}"))
    diffs.append(st.selectbox("الصعوبة",["سهل","متوسط","صعب"],key=f"d{i}"))

# تحويل الصعوبة لأرقام
diff_map = {"سهل":1,"متوسط":2,"صعب":3}

if st.button("تحليل ذكي"):

    data=[]

    for s,sc,t,d in zip(subjects,scores,totals,diffs):
        if s.strip()=="":
            continue
        percent = sc/t*100
        diff_num = diff_map[d]
        priority = (100-percent)+(diff_num*12)
        data.append([s,percent,diff_num,priority])

    if len(data)==0:
        st.warning("من فضلك أدخل مواد")
        st.stop()

    df = pd.DataFrame(data,columns=["المادة","النسبة","الصعوبة","priority"])
    df = df.sort_values("priority",ascending=False)

    st.subheader("📊 تحليل الأداء")
    st.dataframe(df)

    st.subheader("📅 جدول مذاكرة ذكي")

    max_p = df["priority"].max()
    min_p = df["priority"].min()

    for _,row in df.iterrows():
        ratio = (row["priority"]-min_p)/(max_p-min_p+0.0001)
        minutes = int(30 + ratio*70)   # من 30 إلى 100 دقيقة
        st.write(f"📘 {row['المادة']} → {minutes} دقيقة")

    st.subheader("📈 رسم بياني للمستوى")
    st.bar_chart(df.set_index("المادة")["النسبة"])

    # توصيات ذكية
    weak = df.iloc[0]["المادة"]
    st.success(f"🔎 أعلى أولوية للمذاكرة: {weak}")
