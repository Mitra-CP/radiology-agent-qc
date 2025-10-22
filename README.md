# Radiology Agent QC: Intelligent Agents for Imaging Workflow Quality & Consistency

## 🧩 Problem Statement
Radiology teams need a reliable way to **monitor image quality, protocol adherence, metadata completeness, dose safety**, and **AI drift** across scanners, modalities, and sites—**without slowing down operations**. Manual spot‑checks miss subtle issues and don’t scale.

This repository provides a **reference implementation** of an **agentic system** that ingests imaging events and **automatically flags issues** with suggested fixes. It’s vendor‑neutral and designed to sit alongside **RIS/EMR, PACS/VNA, DICOM MWL, and AI services**.

## 📦 What’s Inside
- **Agents** for Protocol, Image Quality, Dose, Metadata, Drift, and Governance
- A **streaming pipeline** (simulated) that turns events into findings
- **Quality checks** using rules + basic image metrics (no‑reference surrogates)
- **Reproducible scripts**, tests, example data, and a clear step‑by‑step guide
- Optional FastAPI service to expose findings and health

> Note: This repo includes **synthetic sample data**. Swap in your own DICOM directories to run against real studies.

---

## 🗂️ Repository Structure
```
radiology-agent-qc/
├─ src/
│  ├─ agents/
│  │  ├─ protocol_agent.py
│  │  ├─ image_quality_agent.py
│  │  ├─ dose_agent.py
│  │  ├─ metadata_agent.py
│  │  ├─ drift_agent.py
│  │  └─ governance_agent.py
│  ├─ common/
│  │  ├─ models.py
│  │  ├─ dicom_utils.py
│  │  ├─ metrics.py
│  │  └─ rules.py
│  └─ pipelines/
│     ├─ ingest_simulator.py
│     └─ qc_pipeline.py
├─ configs/
│  ├─ rules.yaml
│  └─ paths.example.yaml
├─ data/
│  └─ sample/
│     ├─ metadata_sample.csv
│     └─ study_events.csv
├─ notebooks/
│  └─ 01_explore_metrics.ipynb
├─ tests/
│  ├─ test_agents.py
│  └─ test_metrics.py
├─ scripts/
│  ├─ run_qc.sh
│  └─ demo_run.py
├─ docker/
│  └─ Dockerfile
├─ requirements.txt
├─ LICENSE
├─ .gitignore
└─ README.md
```

---

## 🧪 Datasets
- **Sample CSVs** (in `data/sample/`) emulate imaging events and minimal DICOM metadata.
- To run on **real DICOM**: point `paths.dicom_root` in `configs/paths.example.yaml` to your folder. The code uses `pydicom`/`SimpleITK` to read pixel data & headers.

### External references (background & metrics)
We draw on concepts similar to **MRQy** (open‑source MRI QC for cohort variability and artifacts) for certain no‑reference metrics and metadata checks. See the paper for details on measures like **CJV, PSNR, SNR variants, EFC, FBER**, etc. (Sadri et al., 2020).

---

## 🛠️ Tools & Methods
- **Rule‑based checks**: simple, explainable policy violations (e.g., missing tags, laterality mismatch, protocol name off‑catalog).
- **No‑reference metrics** (skimage/SimpleITK): noise proxies, entropy focus criterion, contrast‑to‑noise proxies.
- **Drift detection**: rolling z‑scores/EWMA on repeat rates, protocol adherence, basic PSI proxy.
- **Great Expectations** for metadata completeness tests.
- **Agent orchestration** via a simple pipeline; optionally expose via **FastAPI**.

---

## ▶️ Quickstart (Step‑by‑Step)

### 1) Create environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure paths
Copy and edit:
```bash
cp configs/paths.example.yaml configs/paths.yaml
```
Set `dicom_root` to your local DICOM directory (or leave blank to use sample CSV flows).

### 3) Run the demo pipeline
```bash
python scripts/demo_run.py --use-sample
```
This will:
- simulate ingest of study events,
- run all agents,
- write findings to `outputs/findings.csv` and a JSONL audit log.

### 4) (Optional) Run FastAPI service
```bash
uvicorn src.pipelines.qc_pipeline:app --reload
```
Endpoints:
- `GET /health`
- `GET /findings`
- `GET /stats`

### 5) Explore metrics
Open the notebook:
```
notebooks/01_explore_metrics.ipynb
```

---

## ✅ Results (sample run)
- Findings are emitted with: `severity`, `category`, `metric`, `actual`, `expected`, `explanation`, `study_uid`.
- Example: `protocol_adherence` → “CT_ABD_WC expected slice_thickness 1–2.5mm; found 5.0mm; scanner=CT3; technologist=T42.”
- Example: `image_quality` → “High motion likelihood (EFC ↑); consider repeat before patient leaves.”

You can visualize weekly KPIs in the notebook (repeat rates, adherence, PSI proxy).

---

## 🧭 Reproducibility
- **Fully scripted run** via `scripts/run_qc.sh` or `python scripts/demo_run.py`.
- Deterministic seeds where applicable.
- Clear separation between **config**, **code**, **data**, and **outputs**.

---

## 🧰 Extending
- Add site‑specific **rules** in `configs/rules.yaml`.
- Implement new metrics in `src/common/metrics.py`.
- Plug in real event sources (Kafka, Orthanc) by replacing `ingest_simulator.py`.

---

## 🔐 Compliance Note
This reference implementation ships with **no PHI**. When using real data, ensure HIPAA controls (access, audit, de‑ID).

---

## 📚 Citation
If you use the MRI quality‑metric ideas, please cite the MRQy paper (Sadri et al., 2020).

---

## 📄 License
MIT (see LICENSE).

