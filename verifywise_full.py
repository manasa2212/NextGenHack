# ---------------------------
# VerifyWise: Full Stack AI Scam & Misinformation Detector
# Final Year Project - Enhanced 3-Column Layout
# ---------------------------

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from transformers import pipeline
import tldextract
import pdfplumber
import pytesseract
from PIL import Image

# ---------------------------
# Initialize FastAPI
# ---------------------------
app = FastAPI(title="VerifyWise AI Scam & Misinformation Detector")

# ---------------------------
# Load Models
# ---------------------------
text_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
text_classifier = pipeline("text-classification", model=text_model_name)

# ---------------------------
# Input Schemas
# ---------------------------
class TextInput(BaseModel):
    text: str

class URLInput(BaseModel):
    url: str

# ---------------------------
# Helper Functions
# ---------------------------
def analyze_text(text):
    try:
        if len(text.split()) > 400:
            text = " ".join(text.split()[:400])
        result = text_classifier(text)[0]
        verdict = "Safe" if result['label'] == 'POSITIVE' else "Likely Scam / Fake Info"
        explanation = f"AI analyzed the text with confidence {result['score']:.2f}."
        lesson = "Verify information via official sources; avoid sharing OTPs or sensitive info."
        return {
            "verdict": verdict,
            "confidence": result['score'],
            "explanation": explanation,
            "lesson": lesson
        }
    except Exception as e:
        return {
            "verdict": "Error",
            "confidence": 0,
            "explanation": f"Error analyzing text: {str(e)}",
            "lesson": "Try again with shorter or valid input."
        }

def analyze_url(url):
    ext = tldextract.extract(url)
    domain = ext.domain + '.' + ext.suffix
    suspicious_keywords = ["login", "bank", "secure", "verify", "hospital", "upi", "payment", "crypto"]
    risk = any(k in domain.lower() for k in suspicious_keywords)
    verdict = "Likely Scam" if risk else "Safe"
    explanation = f"Domain analyzed: {domain}"
    lesson = "Always check official URLs; avoid clicking suspicious links."
    confidence = 0.85 if risk else 0.95
    return {
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation,
        "lesson": lesson
    }

def extract_text_from_file(file: UploadFile):
    filename = file.filename.lower()
    content = ""
    try:
        if filename.endswith(".pdf"):
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    content += page.extract_text() or ""
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            try:
                image = Image.open(file.file)
                content = pytesseract.image_to_string(image)
            except Exception:
                return None, "Error reading image: Tesseract not installed or not in PATH."
        else:
            content = file.file.read().decode("utf-8")
        return content, None
    except Exception as e:
        return None, str(e)

# ---------------------------
# API Endpoints
# ---------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<html>
<head>
<title>VerifyWise AI Detector</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

body {
  font-family: 'Roboto', sans-serif;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background: url('https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
  background-size: cover;
  color: #fff;
}

.overlay {
  background: rgba(0,0,0,0.7);
  min-height: 100vh;
  padding-bottom: 50px;
}

header {
  background: rgba(0,0,0,0.8);
  text-align: center;
  padding: 35px 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.6);
}

h1 {
  margin: 0;
  font-size: 36px;
  color: #ffdd59;
  text-shadow: 1px 1px 5px #000;
}

main {
  display: flex;
  justify-content: space-between;
  gap: 25px;
  max-width: 1300px;
  margin: 40px auto;
  flex-wrap: wrap;
}

.card {
  flex: 1;
  min-width: 350px;
  height: 650px;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.4);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 15px 35px rgba(0,0,0,0.45);
}

/* Enlarged Inputs */
textarea {
  width: 100%;
  height: 180px;
  padding: 18px;
  margin-top: 20px;
  border: 1px solid #ccc;
  border-radius: 14px;
  font-size: 16px;
  resize: vertical;
}

input[type=text] {
  width: 100%;
  height: 55px;
  padding: 16px;
  margin-top: 20px;
  border: 1px solid #ccc;
  border-radius: 14px;
  font-size: 16px;
}

input[type=file] {
  width: 100%;
  padding: 14px;
  margin-top: 20px;
  border: 1px solid #ccc;
  border-radius: 14px;
  font-size: 16px;
}

button {
  background: linear-gradient(135deg, #ff758c, #ff7eb3);
  color: white;
  border: none;
  border-radius: 14px;
  padding: 16px 28px;
  margin-top: 18px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: 0.4s;
}

button:hover {
  background: linear-gradient(135deg, #ff4e89, #ff3eb3);
}

.result {
  padding: 22px;
  margin-top: 20px;
  border-radius: 14px;
  font-size: 16px;
  flex: 1;
  overflow-y: auto;
  box-shadow: inset 0 0 15px rgba(0,0,0,0.1);
  max-height: 350px; /* Bigger result box */
}

#textResult { background: linear-gradient(to bottom, #f9f0ff, #f0e6ff); border-left: 6px solid #a64ca6; color: #333; }
#urlResult { background: linear-gradient(to bottom, #e0f7fa, #b2ebf2); border-left: 6px solid #00796b; color: #333; }
#fileResult { background: linear-gradient(to bottom, #fff3e0, #ffe0b2); border-left: 6px solid #ff9800; color: #333; }

@media (max-width: 1100px) {
  main { flex-direction: column; }
}
</style>
</head>
<body>
<div class="overlay">
<header>
<h1>🔎 VerifyWise AI Scam & Misinformation Detector</h1>
<p>Unique Interactive Three-Column Layout for FYP</p>
</header>
<main>
<div class="card">
<h3>📄 Analyze Text</h3>
<textarea id="textInput" placeholder="Paste text here..."></textarea>
<button onclick="analyzeText()">Analyze Text</button>
<div class="result" id="textResult">Results will appear here...</div>
</div>

<div class="card">
<h3>🌐 Analyze URL</h3>
<input type="text" id="urlInput" placeholder="Enter URL here...">
<button onclick="analyzeURL()">Analyze URL</button>
<div class="result" id="urlResult">Results will appear here...</div>
</div>

<div class="card">
<h3>📂 Analyze File (PDF/Image/Text)</h3>
<input type="file" id="fileInput">
<button onclick="analyzeFile()">Analyze File</button>
<div class="result" id="fileResult">Results will appear here...</div>
</div>
</main>
</div>

<script>
async function analyzeText() {
const text = document.getElementById("textInput").value;
document.getElementById("textResult").innerHTML = "Analyzing text... 🔍";
const response = await fetch("/analyze_text", {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify({ text })
});
const data = await response.json();
document.getElementById("textResult").innerHTML = formatResult(data);
}

async function analyzeURL() {
const url = document.getElementById("urlInput").value;
document.getElementById("urlResult").innerHTML = "Analyzing URL... 🌐";
const response = await fetch("/analyze_url", {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify({ url })
});
const data = await response.json();
document.getElementById("urlResult").innerHTML = formatResult(data);
}

async function analyzeFile() {
const file = document.getElementById("fileInput").files[0];
if (!file) { alert("Please select a file!"); return; }
document.getElementById("fileResult").innerHTML = "Extracting text from file... 📂";
const formData = new FormData();
formData.append("file", file);
const response = await fetch("/analyze_file", { method: "POST", body: formData });
const data = await response.json();
document.getElementById("fileResult").innerHTML = formatResult(data);
}

function formatResult(data) {
return `
<b>Verdict:</b> ${data.verdict}<br>
<b>Confidence:</b> ${(data.confidence * 100).toFixed(1)}%<br>
<b>Explanation:</b> ${data.explanation}<br>
<b>Lesson:</b> ${data.lesson}
`;
}
</script>
</body>
</html>
"""

@app.post("/analyze_text")
def analyze_text_endpoint(input: TextInput):
    return analyze_text(input.text)

@app.post("/analyze_url")
def analyze_url_endpoint(input: URLInput):
    return analyze_url(input.url)

@app.post("/analyze_file")
def analyze_file_endpoint(file: UploadFile = File(...)):
    text, error = extract_text_from_file(file)
    if error:
        return {
            "verdict": "Error",
            "confidence": 0,
            "explanation": f"Error reading file: {error}",
            "lesson": "Upload a valid text, PDF, or image file."
        }
    return analyze_text(text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("verifywise_full:app", host="127.0.0.1", port=8000, reload=True)
