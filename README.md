# AI-NIDS: Real-time Network Intrusion Detection System
### Hệ thống Phát hiện Xâm nhập Mạng Ứng dụng Học máy Thời gian thực

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit%201.32%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn%20%7C%20XGBoost-F7931E.svg?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Architecture](https://img.shields.io/badge/Design-IEEE%201016%20%7C%20C4%20Model-0F2C59.svg)](DESIGN_DOCS.md)
[![Dataset](https://img.shields.io/badge/Dataset-UNSW--NB15-20BEFF.svg?logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/dhoogla/unswnb15)

---

## 📌 1. Giới thiệu Dự án (Project Overview)

**AI-NIDS** là giải pháp phần mềm phát hiện xâm nhập mạng thông minh dựa trên kỹ thuật Học máy hiện đại, ứng dụng tập dữ liệu chuẩn hóa **UNSW-NB15** (Kaggle: `dhoogla/unswnb15`). Hệ thống cung cấp bảng điều khiển giám sát thời gian thực giúp chuyên viên an ninh (SOC/SecOps) phát hiện kịp thời các cuộc tấn công tinh vi (như *DoS, Fuzzers, Backdoor, Exploit, Generic, Reconnaissance*).

Dự án được thiết kế tuân thủ nghiêm ngặt chuẩn quốc tế **IEEE 1016-2009 / ISO/IEC/IEEE 42010** kết hợp mô hình kiến trúc **C4 Model** (Simon Brown) và **Arc42 for Machine Learning**.

---

## 👥 2. Đơn vị Thực hiện (Team Members & Mentors)

**Đơn vị:** Nhóm 03 – Chương trình Thực tập Doanh nghiệp DTG 2026

| STT | Họ và Tên | Chuyên ngành / Vai trò đảm nhiệm | Module phụ trách |
| :---: | :--- | :--- | :--- |
| 1 | **Nguyễn Duy Thuận** | Kỹ thuật phần mềm (*Trưởng nhóm*) | Kiến trúc Backend, REST API Gateway, Schema Validation & Tích hợp |
| 2 | **Dương Hoàng Bảo Long** | Kỹ thuật phần mềm | Giao diện Giám sát Streamlit, Trực quan hóa Plotly & Xuất Báo cáo |
| 3 | **Văn Đức Cường** | Trí tuệ nhân tạo | Huấn luyện & Đánh giá Mô hình Học máy (XGBoost / Random Forest) |
| 4 | **Trần Thị Thu Hiền** | Trí tuệ nhân tạo | Pipeline Tiền xử lý, Chuẩn hóa Z-score & Trích chọn Đặc trưng |
| 5 | **Trần Ngọc Hải** | Khoa học dữ liệu | Phân tích Thám cứu Dữ liệu (EDA), Xử lý Khuyết thiếu & Mã hóa |

- **Cán bộ hướng dẫn Doanh nghiệp (DTG):** Anh Nguyễn Văn Hải | Anh Nguyễn Minh Huy
- **Kho tài liệu & Dữ liệu (Drive):** [Google Drive Project Folder](https://drive.google.com/drive/u/0/folders/1HlrreFLtmLEWQMcGSaUQbU43mdl77MT6)

---

## 🎯 3. Chỉ tiêu Kỹ thuật Mục tiêu (Target Objectives)

Để giải quyết bản chất **mất cân bằng dữ liệu (Imbalanced Data)** trong an ninh mạng, nhóm thiết lập bộ chỉ số mục tiêu kỹ thuật:
- **Recall (Detection Rate):** $\ge 96.5\%$ (Tiêu chí tối thượng nhằm giảm thiểu rủi ro bỏ lọt tấn công, $FNR \le 3.5\%$).
- **Precision:** $\ge 94.0\%$ (Kiểm soát báo động giả trên lớp Normal, $FPR \le 5.0\%$).
- **F1-Score (Macro / Weighted):** $\ge 95.0\%$.
- **ROC-AUC & PR-AUC:** $\ge 0.98$ (Khả năng phân tách xác suất ranh giới nhị phân).
- **Accuracy (Độ chính xác nhị phân tổng thể):** $\ge 95.0\%$.

### Hiệu năng & Chuẩn đo lường Độ trễ (Latency Benchmark)
- **Pure Inference Latency:** $< 15\text{ms}$ cho 1 luồng; $< 1.2\text{s}$ cho lô $10.000$ bản ghi.
- **End-to-End Latency:** $< 50\text{ms}$ cho 1 luồng; $< 2.5\text{s}$ cho lô $10.000$ bản ghi.
- **Môi trường tham chiếu:** CPU Intel Core i5/i7 gen 11+ / AMD Ryzen 5/7 (4C/8T), 16GB RAM DDR4.

---

## 🏛️ 4. Kiến trúc Hệ thống (System Architecture)

### 4.1. Sơ đồ Ngữ cảnh Hệ thống (C4 Model - Level 1: System Context)
![C4 Context](docs/diagrams/c4_context.png)

### 4.2. Sơ đồ Kiến trúc Vùng chứa 3 Tầng (C4 Model - Level 2: Container Architecture)
![C4 Container](docs/diagrams/c4_container.png)

Hệ thống được tổ chức thành 3 tầng:
1. **Frontend Presentation Container (Port 8501):** Streamlit Web App cho phép kéo-thả tệp CSV, hiển thị bảng xem trước, thẻ KPI và biểu đồ Donut Plotly.
2. **Backend API Gateway & Core Service Container (Port 8000):** FastAPI Server điều phối endpoints, xác thực schema Pydantic, bảo mật CORS, Rate Limiting và Mock Engine.
3. **ML Inference Component (In-Process Module):** Chạy trực tiếp trong Backend thông qua Scikit-Learn và mô hình XGBoost hoặc Random Forest (`nids_pipeline.joblib`), trả về `predicted_label` và `risk_score` $[0.0 - 1.0]$.
4. **Kiến trúc Lưu trữ (Storage):** Prototype sử dụng Local Volume Mount (`/artifacts`, `/data`); Production roadmap mở rộng sang Shared Object Storage (MinIO / AWS S3) và Redis Cache.

### 4.3. Sơ đồ Phân rã Thành phần (C4 Model - Level 3: Component Decomposition)
![C4 Components](docs/diagrams/c4_components.png)

### 4.4. Quy trình Luồng Dữ liệu Toàn trình 7 Bước (Realtime ML Dataflow)
![7-Step Dataflow](docs/diagrams/dataflow_7step.png)

### 4.5. Sơ đồ Trình tự UML (Sequence Diagram)
![Sequence Diagram](docs/diagrams/sequence_diagram.png)

### 4.6. Sơ đồ Máy Trạng thái Vòng đời (State Machine Diagram)
![State Machine](docs/diagrams/state_machine.png)

---

## 📊 5. Hợp đồng Dữ liệu (Data Contract - UNSW-NB15)

Dữ liệu đầu vào tiếp nhận 47 trường thông tin theo chuẩn UNSW-NB15:
- **Trường định danh bản ghi (`id`):** Được giữ trong schema để theo dõi dòng nhưng **loại bỏ khỏi không gian đặc trưng của mô hình** nhằm triệt tiêu rò rỉ dữ liệu (Data Leakage).
- **46 Đặc trưng mạng thực tế:** Giao thức (`proto`), Dịch vụ (`service`), Trạng thái (`state`), Thời lượng (`dur`), Lưu lượng (`sbytes`, `dbytes`, `sttl`, `dttl`), Gói tin (`spkts`, `dpkts`, ...), TCP (`swin`, `dwin`, ...), Cửa sổ kết nối (`ct_srv_src`, `ct_state_ttl`, ...).
- **2 Cột Ground Truth (`label`, `attack_cat`):** Được tách riêng hoàn toàn khi suy luận trực tiếp; chỉ dùng làm nhãn đối chiếu tính Confusion Matrix nếu tệp dữ liệu test có sẵn.

### Quy chuẩn Điểm Rủi ro (Risk Score)
- **Backend API:** `risk_score` là số thực float trong đoạn $[0.0 - 1.0]$ biểu diễn xác suất $P(Y=1|X)$ từ `predict_proba()`.
- **Phân loại cấp độ:** `Low` $[0.0 - 0.3)$, `Medium` $[0.3 - 0.7)$, `High` $[0.7 - 1.0]$.
- **Frontend Streamlit:** Quy đổi hiển thị trực quan sang phần trăm (`risk_score * 100%`).

---

## 📁 6. Cấu trúc Thư mục Dự án (Repository Structure)

```text
DTG_ProjectGroup3/
├── backend/                  # Dịch vụ API Backend (FastAPI) - Nguyễn Duy Thuận
│   ├── app/
│   │   ├── api/              # Định tuyến endpoints: upload, predict, export
│   │   ├── core/             # Cấu hình CORS, RateLimit, Logging, Security
│   │   ├── schemas/          # Pydantic Schemas (UNSW-NB15, Predictions)
│   │   └── services/         # InferenceService, MockEngine, ReportGenerator
│   ├── main.py               # Điểm khởi chạy máy chủ FastAPI (Port 8000)
│   └── requirements.txt      # Thư viện phụ thuộc Backend
├── frontend/                 # Giao diện Giám sát (Streamlit) - Dương Hoàng Bảo Long
│   ├── app.py                # Dashboard chính: Kéo thả file, biểu đồ Plotly
│   ├── components/           # UploadView, MetricCards, Charts, ExportWidget
│   └── requirements.txt      # Thư viện phụ thuộc Frontend
├── ml_pipeline/              # Động cơ Trí tuệ Nhân tạo - Cường, Hiền, Hải
│   ├── notebooks/            # Jupyter Notebooks: EDA, Feature Selection, Training
│   ├── src/                  # Mã nguồn Pipeline: Preprocessing & Evaluator
│   └── artifacts/            # nids_pipeline.joblib (Mô hình đóng gói)
├── data/                     # Tập dữ liệu mẫu UNSW-NB15 phục vụ thử nghiệm
│   └── sample_unsw_test.csv  # File mẫu 20 dòng kiểm thử định dạng chuẩn
├── tests/                    # Kịch bản kiểm thử tự động (Unit Test & Integration Test)
│   ├── test_api.py           # Kiểm thử các endpoint FastAPI
│   └── test_pipeline.py      # Kiểm thử chuỗi tiền xử lý dữ liệu
├── docs/                     # Tài liệu thiết kế kỹ thuật (IEEE 1016 & C4 Model)
│   ├── diagrams/             # 6 sơ đồ kiến trúc PNG 300 DPI
│   ├── Nhom3_tuan1_DesignDocs.pdf  # Bản PDF xuất bản chính thức (10 trang)
│   └── Nhom3_tuan1_DesignDocs.docx # Bản Word có thể chỉnh sửa
├── .gitignore                # Danh mục loại trừ tệp nhị phân và cache
├── DESIGN_DOCS.md            # Bản đặc tả kỹ thuật dạng Markdown (kèm Mermaid)
└── README.md                 # Tài liệu hướng dẫn tổng quan hệ thống
```

---

## 🚀 7. Hướng dẫn Cài đặt & Vận hành (Quickstart)

### Bước 1: Clone kho mã nguồn
```bash
git clone https://github.com/VNDT1625/DTG_ProjectGroup3.git
cd DTG_ProjectGroup3
```

### Bước 2: Khởi chạy Backend (FastAPI - Port 8000)
```bash
# Mở Terminal 1
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
- API Docs (Swagger UI): http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

### Bước 3: Khởi chạy Frontend (Streamlit - Port 8501)
```bash
# Mở Terminal 2
cd frontend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py --server.port 8501
```
- Web Dashboard: http://localhost:8501

---

## 🛡️ 8. An ninh & Gia cố Hệ thống (Security & Hardening)
1. **Kiểm soát Tệp tải lên:** Kiểm tra MIME type (`text/csv`), phần mở rộng `.csv`, giới hạn dung lượng $\le 50\text{MB}$ hoặc $\le 100.000$ dòng.
2. **Chống CSV Formula Injection:** Tự động khử khuẩn các ô dữ liệu bắt đầu bằng `=`, `+`, `-`, `@` trước khi xuất file CSV/XLSX.
3. **Chống Path Traversal:** Mã hóa tên tệp bằng UUID v4 ngẫu nhiên (`fl_sample_uuid4_2026`).
4. **Bảo vệ Cổng API:** Cấu hình CORS Middleware chỉ cho phép origin Frontend, áp dụng Rate Limiting chống DoS API.

---

## 📅 9. Lộ trình Triển khai Dự án (Roadmap)
- **Tuần 1 (Hiện tại):** Hoàn thành tài liệu thiết kế kiến trúc chuẩn IEEE 1016, 6 sơ đồ C4/UML; tải khung cấu trúc dự án cơ bản lên GitHub; giao diện Streamlit cơ sở và Mock Data Engine.
- **Tuần 2:** Đội ngũ AI hoàn thành huấn luyện mô hình XGBoost hoặc Random Forest trên UNSW-NB15, xuất artifact `nids_pipeline.joblib` hoàn chỉnh.
- **Tuần 3:** Tích hợp trực tiếp (End-to-End) giữa FastAPI Backend và ML Pipeline; hoàn thiện tính năng xuất báo cáo đa định dạng XLSX và PDF.
- **Tuần 4:** Kiểm thử tải, tối ưu hóa giao diện người dùng, đóng gói Docker hoàn chỉnh và báo cáo nghiệm thu doanh nghiệp DTG.

---
*Bản quyền tài liệu thuộc về Nhóm 03 – Khóa thực tập Doanh nghiệp DTG 2026.*
