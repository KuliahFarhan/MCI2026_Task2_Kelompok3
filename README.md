
# MCI2026_Task2_Kelompok 3

## Overview

Project ini merupakan implementasi sederhana Data Engineering Pipeline menggunakan:

* Apache Airflow → orchestration pipeline
* ClickHouse → data warehouse
* Docker Compose → container orchestration
* Python ETL → extract, transform, load
* Metabase → visualisasi data

Pipeline akan:

```text
API Orders
→ Extract
→ Transform nested JSON
→ Load ke ClickHouse
→ Trigger via Airflow DAG
```

Dataset source:

```text
http://96.9.212.102:8000/orders
```

---

# Struktur Project

```text
MCI2026_Task2_Kelompok3/
│
├── dags/
│   └── orders_pipeline.py
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── sql/
│   ├── create_database.sql
│   └── create_table.sql
│
├── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# Technologies Used

| Technology     | Function                  |
| -------------- | ------------------------- |
| Python         | ETL scripting             |
| Apache Airflow | Workflow orchestration    |
| ClickHouse     | Analytical database       |
| Docker Compose | Container management      |
| Metabase       | Dashboard & visualization |

---

# Requirements

Sebelum menjalankan project pastikan sudah menginstall:

* Docker Desktop
* Git
* Python 3.11+
* VS Code (optional)

Cek instalasi:

```bash
python --version
docker --version
git --version
```

---

# Quick Start (Recommended Order)

Ikuti urutan berikut agar project dapat berjalan tanpa error dependency atau warehouse kosong.

```text
1. Clone repository
2. Jalankan Docker services
3. Install dependency Airflow
4. Setup ClickHouse database & table
5. Trigger DAG Airflow
6. Verifikasi data masuk ke ClickHouse
7. Jalankan Metabase
8. Connect Metabase ke ClickHouse
9. Build query & dashboard
```

Catatan penting:

Metabase tidak akan menampilkan data apabila DAG Airflow belum dijalankan.

Karena alur project:

```text
API → Airflow DAG → ClickHouse → Metabase
```

Jadi warehouse harus terisi terlebih dahulu sebelum visualisasi dibuat.

---

# Clone Repository

```bash
git clone https://github.com/<username>/MCI2026_Task2_Kelompok3.git
cd MCI2026_Task2_Kelompok3
```

---

# Menjalankan Docker Services

Jalankan seluruh service:

```bash
docker compose up -d
```

Cek container:

```bash
docker ps
```

Container yang seharusnya aktif:

```text
clickhouse-server
airflow
metabase
```

---

# Install Dependency pada Airflow

Karena dependency ETL digunakan di dalam container Airflow, install package berikut:

```bash
docker exec -it airflow pip install clickhouse-connect requests
```

---

# Setup ClickHouse

Masuk ke ClickHouse client:

```bash
docker exec -it clickhouse-server clickhouse-client --user admin --password admin123
```

---

# Membuat Database

Jalankan:

```sql
CREATE DATABASE IF NOT EXISTS mci_orders;
```

Pilih database:

```sql
USE mci_orders;
```

---

# Membuat Table

Jalankan isi file:

```text
sql/create_table.sql
```

Atau copy query berikut:

```sql
CREATE TABLE IF NOT EXISTS orders (
    order_id Int32,
    user_id Int32,
    order_number Int32,
    order_dow Int32,
    order_hour_of_day Int32,
    days_since_prior_order Float32,
    eval_set String,

    product_id Int32,
    product_name String,

    aisle_id Int32,
    aisle String,

    department_id Int32,
    department String,

    add_to_cart_order Int32,
    reordered Int32
)
ENGINE = MergeTree()
ORDER BY (order_id, product_id);
```

---

# Menjalankan ETL Manual

Untuk testing ETL tanpa Airflow:

```bash
python etl/extract.py
```

Jika berhasil:

```text
Berhasil insert ... rows ke ClickHouse
ETL pipeline berhasil dijalankan
```

---

# Verifikasi Data di ClickHouse

Masuk kembali ke ClickHouse:

```bash
docker exec -it clickhouse-server clickhouse-client --user admin --password admin123
```

Gunakan database:

```sql
USE mci_orders;
```

Cek jumlah data:

```sql
SELECT COUNT(*) FROM orders;
```

Cek sample data:

```sql
SELECT *
FROM orders
LIMIT 5;
```

---

# Menjalankan Airflow

Airflow UI tersedia di:

```text
http://localhost:8081
```

Login:

```text
Username: admin
Password: admin123
```

---

# Airflow DAG

DAG yang digunakan:

```text
orders_etl_pipeline
```

Langkah menjalankan DAG:

1. Aktifkan toggle DAG
2. Klik tombol ▶
3. Pilih Trigger DAG

Jika berhasil:

* task berubah menjadi hijau
* data otomatis masuk ke ClickHouse

---

# Menjalankan Metabase

Metabase UI:

```text
http://localhost:3000
```

Setup awal:

1. Create admin account
2. Add database
3. Pilih ClickHouse

---

# Konfigurasi ClickHouse di Metabase

Gunakan konfigurasi berikut:

| Field    | Value      |
| -------- | ---------- |
| Host     | clickhouse |
| Port     | 8123       |
| Database | mci_orders |
| Username | admin      |
| Password | admin123   |

---

# Contoh Query untuk Metabase

## Total Orders

```sql
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM orders;
```

---

## Top 10 Product

```sql
SELECT
    product_name,
    COUNT(*) AS total
FROM orders
GROUP BY product_name
ORDER BY total DESC
LIMIT 10;
```

---

## Top Department

```sql
SELECT
    department,
    COUNT(*) AS total
FROM orders
GROUP BY department
ORDER BY total DESC;
```

---

## Order Distribution by Hour

```sql
SELECT
    order_hour_of_day,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_hour_of_day
ORDER BY order_hour_of_day;
```

---

# Dashboard Recommendation

Dashboard minimal yang direkomendasikan:

1. Total Orders
2. Top Products
3. Top Departments
4. Order Distribution by Hour
5. Reordered vs Non-Reordered Products

---

# Common Errors

## Airflow DAG tidak muncul

Cek:

```bash
docker logs airflow
```

---

## Connection refused ClickHouse

Pastikan di:

```python
host='clickhouse'
```

bukan:

```python
host='localhost'
```

---

## ModuleNotFoundError pada Airflow

Install dependency:

```bash
docker exec -it airflow pip install clickhouse-connect requests
```

---

# Notes

Project ini menggunakan:

* SQLite metadata database Airflow
* SequentialExecutor

Karena project hanya digunakan untuk development dan tugas praktikum.

Untuk production environment disarankan:

* PostgreSQL metadata DB
* CeleryExecutor / KubernetesExecutor
* custom Docker image
* environment variables terpisah

---

# Contributors

Kelompok 3 - MCI 2026
