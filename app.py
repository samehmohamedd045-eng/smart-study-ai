import streamlit as st
import pandas as pd

st.title("🎓 Smart Study Assistant AI")

st.write("أدخل بيانات المواد لتحليل الأداء وبناء جدول مذاكرة ذكي")

subjects=[]
scores=[]
totals=[]
diffs=[]

n = st.number_input("عدد المواد",1,10,3)

for i in range(n):
    st.subheader(f"مادة {i+1}")
    subjects.append(st.text_input("اسم المادة",key=i))
    scores.append(st.number_input("درجتك",0,100,key=i+20))
    totals.append(st.number_input("الدرجة النهائية",1,100,key=i+40))
    diffs.append(st.selectbox("الصعوبة",[1,2,3],key=i+60))

if st.button("تحليل ذكي"):

    data=[]
 
    for s,sc,t,d in zip(subjects,scores,totals,diffs):
        percent = sc/t*100
        priority = (100-percent)+(d*10)
        data.append([s,percent,d,priority])

    df=pd.DataFrame(data,columns=["المادة","النسبة","الصعوبة","أولوية"])

    df=df.sort_values("أولوية",ascending=False)

    st.subheader("📅 جدول مذاكرة ذكي حسب الأولوية")

max_p = df["أولوية"].max()
min_p = df["أولوية"].min()

for i,row in df.iterrows():
    ratio = (row["أولوية"]-min_p)/(max_p-min_p+0.01)
    minutes = int(30 + ratio*60)   # من 30 إلى 90 دقيقة
    st.write(f"ذاكر {row['المادة']} — {minutes} دقيقة")


    st.bar_chart(df.set_index("المادة")["النسبة"])
