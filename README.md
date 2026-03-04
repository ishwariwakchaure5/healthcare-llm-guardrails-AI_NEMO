# 🏥 Healthcare LLM Guardrails System  
### Secure, Safety-Focused Healthcare Conversational AI using NVIDIA NeMo Guardrails

---

## 📌 Project Overview

Healthcare LLM Guardrails is a safety-first conversational AI system designed for healthcare-related queries.  
The system combines:

- 🔐 NVIDIA NeMo Guardrails (Colang-based safety rules)
- 🤖 OpenAI GPT backend (LLM reasoning)
- 🧠 Advanced NLP (spaCy + TextBlob)
- 🛡️ Custom rule-based medical safety engine
- 🌐 Flask-based Web Interface

This project ensures that the AI:
- Does NOT provide medical diagnoses
- Does NOT prescribe medications
- Does NOT give treatment plans
- Prevents prompt injection attacks
- Detects personal data exposure (PII)
- Handles self-harm content safely
- Provides only educational medical information

---

## 🏗️ System Architecture

User → Flask Web Interface → NeMo Guardrails →  
Colang Safety Rules → OpenAI LLM Backend →  
Response Validation → Final Safe Response  

Additionally:
- Semantic analysis layer using spaCy
- Sentiment analysis using TextBlob
- Rule-based fallback if LLM fails
- Statistics tracking for blocked/allowed queries

---

## 🧠 AI Stack Used

### 🔹 Primary AI Framework
**NVIDIA NeMo Guardrails**

Used for:
- Healthcare safety rules
- Prompt injection prevention
- Privacy enforcement
- Controlled LLM outputs

---

### 🔹 Language Model Backend
**OpenAI GPT Models**

Used for:
- Natural language understanding
- Educational health explanations
- Contextual responses

Environment variable required:
```
OPENAI_API_KEY
```

---

### 🔹 NLP & Semantic Analysis
- spaCy (Advanced entity detection & intent classification)
- TextBlob (Sentiment analysis)
- Regex-based rule detection
- Custom intent detection engine

---

### 🔹 Custom Medical Knowledge Engine
File: `comprehensive_ai.py`

Includes:
- Medical terms database
- Symptom mapping
- Disease mapping
- Treatment category filtering
- Word-by-word query analysis

---

## 🔐 Safety Guardrails Implemented

### 1️⃣ Diagnosis Blocking
Prevents:
- “Do I have cancer?”
- “Diagnose my symptoms”
- “What disease do I have?”

---

### 2️⃣ Prescription Blocking
Prevents:
- “What medication should I take?”
- “Prescribe antibiotics”
- “What dosage should I use?”

---

### 3️⃣ Treatment Advice Blocking
Prevents:
- “How do I cure my condition?”
- “What treatment do I need?”

---

### 4️⃣ Prompt Injection Prevention
Blocks:
- “Ignore previous instructions”
- “Act as a doctor”
- “Override safety rules”

---

### 5️⃣ Privacy Protection
Detects:
- SSN
- Patient IDs
- Insurance numbers
- Personal medical records

---

### 6️⃣ Self-Harm Detection
Responds with:
- 988 Crisis Helpline
- Emergency instructions

---

## 📁 Project Structure

```
├── app.py                  # CLI Healthcare AI with Guardrails
├── app_nemo.py             # NeMo Guardrails demo version
├── nemo_web_interface.py   # Flask Web Application
├── comprehensive_ai.py     # Custom medical knowledge engine
├── config/                 # NeMo configuration files
├── rails/                  # Colang safety rule files
├── templates/              # HTML templates
├── requirements.txt        # Project dependencies
```

---

## 🚀 Installation

### 1️⃣ Create Virtual Environment
```bash
python -m venv healthcare-ai-env
```

### 2️⃣ Activate Environment
Windows:
```bash
healthcare-ai-env\Scripts\activate
```

Mac/Linux:
```bash
source healthcare-ai-env/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set API Key
```bash
export OPENAI_API_KEY=your_api_key_here
```
Windows:
```bash
set OPENAI_API_KEY=your_api_key_here
```

---

## ▶️ Running the Application

### CLI Version
```bash
python app.py
```

### NeMo Demo Version
```bash
python app_nemo.py
```

### Web Interface
```bash
python nemo_web_interface.py
```

Open browser:
```
http://localhost:5000
```

---

## 📊 System Capabilities

| Feature | Supported |
|----------|------------|
| Medical Education | ✅ |
| Diagnosis | ❌ Blocked |
| Prescription | ❌ Blocked |
| Treatment Advice | ❌ Blocked |
| Prompt Injection Protection | ✅ |
| PII Detection | ✅ |
| Crisis Detection | ✅ |
| Sentiment Analysis | ✅ |
| Fallback Rule Engine | ✅ |

---

## 🎯 Intended Use

This system is designed for:

- Healthcare AI safety research
- LLM guardrail experimentation
- AI safety engineering portfolios
- Academic projects
- Secure medical chatbot prototypes

It is NOT intended for:
- Real medical diagnosis
- Prescription generation
- Clinical deployment

---

## ⚠️ Healthcare Disclaimer

This AI provides general health information for educational purposes only.  
It is not a substitute for professional medical advice, diagnosis, or treatment.  
Always consult qualified healthcare professionals for medical concerns.  

In case of emergency, call emergency services immediately.

---

## 🛠️ Technical Highlights

- Hybrid Guardrail Architecture
- Semantic Intent Detection
- Colang Rule Integration
- LLM + Rule-Based Safety Hybrid
- Async Processing with asyncio
- Structured Logging
- Real-Time Safety Monitoring
- Web Dashboard Statistics

---

## 👩‍💻 Author

Ishwari Wakchaure  
Healthcare AI Safety Engineering Project  

