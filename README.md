# Ceratec-PDP-Scraper
A Python-based web scraping project to extract Product Detail Page (PDP) data from Ceratec Surfaces product pages.

This project is built specifically around the Ceratec PDP structure (example: *Alchemy* series) and demonstrates how to reliably collect structured product data for e-commerce, cataloging, or analytics use cases.

---

## 🔍 Example Product Page

```
https://www.ceratec.com/fr/RSS-2048-Alchemy-2
```

---

## 📌 Data Points Extracted

The scraper follows the navigation and data mapping shown in the provided screenshots and documentation.

| #  | Field                           |
| -- | ------------------------------- |
| 1  | Product URL                     |
| 2  | Product Title                   |
| 3  | Breadcrumbs                     |
| 4  | Product Description             |
| 5  | Image URLs (all variants)       |
| 6  | Color of Variant                |
| 7  | Color Grouping                  |
| 8  | Surface Finish / Material       |
| 9  | Dimension / Size Grouping       |
| 10 | Technical Documents (PDF links) |

---

## 📂 Project Structure

```
ceratec-pdp-scraper/
│
├── pdp_ceratec.py          # Main scraper logic
├── constants.py           # Headers & cookies
├── Navigatin_document.pptx # Navigation & field mapping reference
├── Pending_todo_Website.txt
├── product_data_*.csv     # Output (CSV)
├── product_data_*.xlsx    # Output (Excel)
└── README.md
```

---

## ⚙️ Tech Stack

* Python 3.9+
* requests
* beautifulsoup4
* pandas

---

## 🚀 How to Run

### 1️⃣ Install Dependencies

```bash
pip install requests beautifulsoup4 pandas
```

### 2️⃣ Run the Scraper

```bash
python pdp_ceratec.py
```

### 3️⃣ Output

The script automatically generates timestamped files:

* `product_data_YYYYMMDD_HHMMSS.csv`
* `product_data_YYYYMMDD_HHMMSS.xlsx`

---

## 🧠 How It Works

* Sends a browser-like request using realistic headers
* Parses the HTML with BeautifulSoup
* Extracts variant attributes using label-based matching
* Collects technical document download links
* Stores structured output using Pandas

---

## 🧩 Key Functions

* `get_product_title()`
* `get_breadcrumbs()`
* `get_description()`
* `get_image_urls()`
* `get_color_grouping_by_tag()`
* `get_size_grouping()`
* `get_material()`
* `get_technical_document()`

---

## 📎 Notes

* Cookies are optional but included for stability
* Script retries requests automatically
* Easy to scale for multiple product URLs

---

## 📈 Use Cases

* E-commerce catalog scraping
* Product data enrichment
* Variant image & color extraction
* Market research & analytics

---

## 👤 Author

**Shoeb Ahmed**
Web Scraping | Python | Data Extraction

---

## ⚠️ Disclaimer

This project is for **educational and portfolio purposes only**. Please respect website terms of service before scraping.

---

⭐ If this helped you, consider starring the repository!

