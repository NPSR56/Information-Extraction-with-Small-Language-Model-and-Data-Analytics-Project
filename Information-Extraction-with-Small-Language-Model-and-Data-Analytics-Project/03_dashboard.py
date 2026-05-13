## 03_dashboard.py
import streamlit as st
import pandas as pd
import ast
from collections import Counter

st.set_page_config(page_title="News NER & Sentiment", layout="wide")
st.title("News Information Extraction Dashboard")
st.caption("โปรเจค Sentiment Analysis จากข่าวออนไลน์")

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\Ma work\project\Information-Extraction-with-Small-Language-Model-and-Data-Analytics-Project\data\articles_processed.csv", encoding="utf-8-sig")
    
    def parse_persons(x):
        if not isinstance(x, str) or x.strip() == '' or x.strip() == '[]':
            return []
        try:
            result = ast.literal_eval(x)
            return result if isinstance(result, list) else []
        except:
            return []
    
    df['persons'] = df['persons'].apply(parse_persons)
    return df

df = load_data()

# --- Sidebar filter ---
st.sidebar.header("ตัวกรอง")
sentiment_filter = st.sidebar.multiselect(
    "Sentiment",
    options=['positive', 'negative', 'neutral'],
    default=['positive', 'negative', 'neutral']
)
df_filtered = df[df['sentiment'].isin(sentiment_filter)]

# --- Metrics ---
st.subheader("ภาพรวม")
c1, c2, c3, c4 = st.columns(4)
c1.metric("ข่าวทั้งหมด",    len(df_filtered))
c2.metric("Positive",       len(df_filtered[df_filtered['sentiment'] == 'positive']))
c3.metric("Negative",       len(df_filtered[df_filtered['sentiment'] == 'negative']))
c4.metric("Neutral",        len(df_filtered[df_filtered['sentiment'] == 'neutral']))

st.divider()

# --- Charts ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Sentiment Distribution")
    sentiment_counts = df_filtered['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']
    st.bar_chart(sentiment_counts.set_index('sentiment'))

with col_right:
    st.subheader("บุคคลที่ถูกกล่าวถึงมากสุด Top 10")
    all_persons = [p for sublist in df_filtered['persons'] for p in sublist]
    if all_persons:
        top_df = pd.DataFrame(
            Counter(all_persons).most_common(10),
            columns=['ชื่อ', 'จำนวนครั้ง']
        )
        st.bar_chart(top_df.set_index('ชื่อ'))
    else:
        st.info("ไม่พบข้อมูลบุคคล")

st.divider()

# --- Person–Sentiment breakdown ---
st.subheader("บุคคล vs Sentiment")
rows = []
for _, row in df_filtered.iterrows():
    for person in row['persons']:
        rows.append({'ชื่อ': person, 'sentiment': row['sentiment']})

if rows:
    person_df = pd.DataFrame(rows)
    pivot = (person_df.groupby(['ชื่อ', 'sentiment'])
                      .size()
                      .unstack(fill_value=0)
                      .reset_index())
    # แสดงเฉพาะคนที่ถูกพูดถึงบ่อย >= 1 ครั้ง
    pivot['total'] = pivot.drop(columns='ชื่อ').sum(axis=1)
    pivot = pivot[pivot['total'] >= 1].sort_values('total', ascending=False)
    st.dataframe(pivot.drop(columns='total'), use_container_width=True)

st.divider()

# --- Raw data table ---
st.subheader("ตารางข้อมูลทั้งหมด")
st.dataframe(
    df_filtered[['title', 'sentiment', 'pos_score', 'neg_score', 'person_count', 'url']],
    use_container_width=True
)

# --- Article detail ---
st.subheader("อ่านบทความ")
selected = st.selectbox("เลือกบทความ", df_filtered['title'].tolist())
if selected:
    row = df_filtered[df_filtered['title'] == selected].iloc[0]
    st.markdown(f"**Sentiment:** `{row['sentiment']}`")
    st.markdown(f"**บุคคลที่พบ:** {', '.join(row['persons']) if row['persons'] else 'ไม่พบ'}")
    st.markdown(f"**URL:** {row['url']}")
    with st.expander("ดูเนื้อหาบทความ"):
        st.write(row['text'])


#หลังจากรันข้อมูลแล้วให้พิมพ์ "python -m streamlit run 03_dashboard.py" บนช่อง terminal เพื่อเปิด dashboard