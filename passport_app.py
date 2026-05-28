import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# إعدادات واجهة الموقع
st.set_page_config(page_title="مؤشر جوازات السفر العالمي", page_icon="🌐", layout="centered")

st.title(" مستكشف قوة جوازات السفر العالمية")
st.markdown(
    "مرحباً بكِ! هذا الموقع يقوم بسحب البيانات **مباشرة ولحظياً** من ويكيبيديا لتحليل وترتيب جوازات السفر عالمياً.")

url = "https://en.wikipedia.org/wiki/Henley_Passport_Index"

if st.button(" اسحب البيانات المباشرة الآن"):
    with st.spinner("جاري الاتصال بويكيبيديا وسحب البيانات... انتظر ثواني "):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.content, "html.parser")

            table = soup.find(lambda t: t.name == "table" and "Singapore" in t.text)

            if table:
                all_rows = []
                headers = [th.text.strip() for th in table.find_all("tr")[0].find_all(["th", "td"])]

                if not headers or len(headers) < 3:
                    headers = ["الترتيب", "الدول", "عدد الوجهات بدون فيزا"]

                # تجميع البيانات داخل الحلقة
                for row in table.find_all("tr")[1:]:
                    row_cells = row.find_all(["td", "th"])
                    cells = [c.text.strip() for c in row_cells]

                    if cells:
                        if len(cells) == len(headers):
                            all_rows.append(cells)

                # تحويل البيانات وعرضها (خارج حلقة الـ for ولكن داخل الـ if table)
                df = pd.DataFrame(all_rows, columns=headers)

                st.success(" تم سحب البيانات بنجاح وعرضها تلقائياً!")
                st.subheader(" جدول الترتيب العالمي الحقيقي")
                st.dataframe(df, use_container_width=True)

            else:
                st.error(" لم نتمكن من العثور على الجدول المطلوب.")

        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالإنترنت: {e}")

st.markdown("---")
st.caption(" تم تطوير وتصميم الواجهة بواسطة المبرمجة: **Saja Naeem Abdali** ")
