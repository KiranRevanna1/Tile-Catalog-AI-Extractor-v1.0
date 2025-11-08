# 🧱 Tile Catalog AI Extractor (v1.0)

An intelligent backend system that automatically extracts **product images**, **names**, **dimensions**, and **specifications** from PDF-based tile catalogs using **YOLOv8 object detection**, **OCR**, and **FastAPI**.

---

## 🚀 Features

✅ Convert PDF pages into high-resolution images  
✅ Detect product tiles using **YOLOv8**  
✅ Extract product text using **Tesseract OCR**  
✅ Automatically group product info (image + name + specs)  
✅ Return structured JSON data for frontend integration  
✅ Modular, clean, and extensible architecture  

---

## 🧩 Project Structure
  ``` bash
    tile-catalog-ai/
    ├── backend/
    │ ├── main.py # FastAPI entrypoint
    │ ├── extractor/
    │ │ ├── pdf_pipeline.py # PDF → YOLO → OCR pipeline
    │ │ ├── formatter.py # Structures extracted product data
    │ │ └── utils/ # (Helper utilities if needed)
    │ ├── routes/
    │ │ └── feedback.py # Placeholder for feedback/learning API
    │ ├── output/ # Generated images, crops, and results
    │ ├── uploads/ # Uploaded PDFs
    │ └── requirements.txt # Dependencies
  ```
---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
  ```bash
    git clone https://github.com/yourusername/tile-catalog-ai.git
    cd tile-catalog-ai/backend
  ```

### 2️⃣ Create a Virtual Environment

  ``` bash
    python -m venv venv
    venv\Scripts\activate   # (Windows)
    # or
    source venv/bin/activate  # (Mac/Linux)
  ```

### 3️⃣ Install Dependencies

  ``` bash
    pip install -r requirements.txt
  ```

### 4️⃣ Run the Server

  ``` bash
    uvicorn main:app --reload
  ```

### 5️⃣ Test the API

    Open Postman
    or any API client:

    -- POST → http://127.0.0.1:8000/extract

    -- Upload a PDF file
      ✅ Response → Structured JSON of products (with image paths)

---

## 🧪 Current Version (v1.0)

  ✅ Core pipeline working:

    -- PDF → Images → YOLO → OCR → Structured Output

🚧 Future Enhancements:

    -- Custom YOLO training for better accuracy
    --  Frontend visualization dashboard
    -- Database + Feedback learning

---

## 🧑‍💻 Author

    Kiran L
    Senior Full stack Developer & Contributor
    📧 Contact: kiranrevanna01@gmail.com
