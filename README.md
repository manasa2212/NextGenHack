# 🔎 VerifyWise – AI Scam & Misinformation Detector

**Final Year Project – Full Stack Web Application**

---

## **Project Overview**
VerifyWise is an **AI-powered web application** that helps users detect scams, phishing, and misinformation from **text, URLs, and files**. With the rise of online fraud and fake news, VerifyWise ensures users can **quickly verify information safely**.  

It features a **modern three-column interface** for interactive analysis of:  
1. **Text** – Paste or type content to analyze its credibility.  
2. **URLs** – Check if a website is potentially suspicious.  
3. **Files** – Upload PDFs, images, or text files; the system extracts content and evaluates it.  

---

## **Key Features**
- **AI-Powered Text Classification:** Fine-tuned DistilBERT model for reliable text analysis.  
- **URL Safety Detection:** Identifies suspicious domains using keyword and domain analysis.  
- **File Content Analysis:** OCR integrated for PDFs/images to extract text for evaluation.  
- **User Education:** Provides explanations and actionable lessons to avoid scams.  
- **Interactive Three-Column Layout:** Easy-to-use interface for non-technical users.  

---

## **Unique Selling Points (USP)**
- **All-in-One Verification**: Analyze text, URLs, and files in one platform.  
- **Real-Time AI Analysis**: Fast, accurate, and reliable scam detection.  
- **Educational Feedback**: Helps users understand risks and avoid misinformation.  
- **Modern UI**: Interactive, responsive, and visually appealing interface.  

---

## **Technologies Used**
- **Backend:** FastAPI, Python  
- **AI Models:** Hugging Face Transformers (`distilbert-base-uncased-finetuned-sst-2-english`)  
- **File Processing:** pdfplumber, pytesseract, PIL  
- **Frontend:** HTML, CSS, JavaScript  
- **Utilities:** tldextract  

commands
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

uvicorn verifywise_full:app --reload
Open your browser at: http://127.0.0.1:8000

## **Project Structure**
