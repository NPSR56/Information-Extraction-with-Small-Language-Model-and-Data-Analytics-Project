# Information Extraction with Small Language Model and Data Analytics

A Thai news NLP pipeline that performs Named Entity Recognition (NER) and Sentiment Analysis on online news articles, with an interactive analytics dashboard.

## Features

- **Web Scraping** — ดึงข่าวจาก Thairath และ Matichon อัตโนมัติ
- **Named Entity Recognition** — จับชื่อบุคคลด้วย WangchanBERTa (ThaiNER v2)
- **Sentiment Analysis** — วิเคราะห์ความรู้สึก positive / negative / neutral
- **Interactive Dashboard** — แสดงผลด้วย Streamlit

## Project Structure

```
project/
├── data/
│   ├── articles.csv                        # Raw scraped articles
│   └── articles_processed.csv             # Articles with NER + Sentiment
├── 01_scrape_and_ner_sentiment.ipynb      # Web scraping + NER + Sentiment
├── 03_dashboard.py                         # Streamlit dashboard
└── README.md
```

## Requirements

- Python 3.9+
- Anaconda (recommended)

## Installation

```bash
# 1. Clone โปรเจค
git clone https://github.com/NPSR56/Information-Extraction-with-Small-Language-Model-and-Data-Analytics-Project.git
cd Information-Extraction-with-Small-Language-Model-and-Data-Analytics-Project

# 2. Install dependencies
pip install pandas transformers torch sentencepiece pythainlp streamlit
```

## Usage

### Step 1 — Scrape + NER + Sentiment Analysis
เปิด `01_scrape_and_ner_sentiment.ipynb` ใน Jupyter แล้วรัน All Cells

ผลลัพธ์: `data/articles.csv` และ `data/articles_processed.csv`

> ครั้งแรกจะโหลด NER model ~500MB ใช้เวลาสักครู่

### Step 2 — Run Dashboard
```bash
python -m streamlit run 03_dashboard.py
```
เปิดเบราว์เซอร์ที่ `http://localhost:8501`

## Models Used

| Component | Model | Description |
|---|---|---|
| NER | `pythainlp/thainer-corpus-v2-base-model` | WangchanBERTa fine-tuned บน Thai NER v2.0 Corpus |
| Sentiment | Rule-based Lexicon | Thai positive/negative word list |

## NER Entity Types

| Tag | ความหมาย |
|---|---|
| PERSON | ชื่อบุคคล |
| ORGANIZATION | ชื่อองค์กร |
| LOCATION | สถานที่ |

## Data Sources

- [Thairath Online](https://www.thairath.co.th)
- [Matichon Online](https://www.matichon.co.th)

## Limitations

- Sentiment analysis ใช้ rule-based — ความแม่นยำจำกัด
- NER model อาจ error กับชื่อต่างประเทศทับศัพท์
- รองรับเฉพาะข่าวภาษาไทย

## Future Work

- Fine-tune sentiment model ภาษาไทยโดยเฉพาะ
- เพิ่มแหล่งข่าวอื่น เช่น Khaosod, Bangkok Post
- เพิ่ม entity type อื่น เช่น DATE, MONEY

## References

- Phatthiyaphaibun, W. (2022). Thai NER 2.0. Zenodo. https://doi.org/10.5281/zenodo.7761354
- Lowphansirikul, L., et al. (2021). WangchanBERTa. arXiv:2101.09635
- PyThaiNLP. https://pythainlp.github.io

