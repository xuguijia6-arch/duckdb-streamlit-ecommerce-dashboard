# DuckDB + Streamlit 电商交易分析仪表盘

这是一个基于 **DuckDB + Streamlit** 搭建的本地电商交易分析项目。  
项目使用 Olist 公开电商数据集，对订单、订单明细、支付方式、客户地区等数据进行分析，并通过 Streamlit 搭建可交互的仪表盘页面。

## 项目功能

当前版本已实现：

- 按订单状态筛选
- 核心 KPI 展示
  - 订单数
  - GMV
  - AOV
  - 覆盖州数
- 月度 GMV 趋势分析
- 支付方式分布分析
- 各州订单 Top 10 分析

## 技术栈

- Python 3.11
- DuckDB
- Streamlit
- Pandas

## 项目结构

```text
duckdb_streamlit_shop/
├─ data/
│  ├─ olist_orders_dataset.csv
│  ├─ olist_order_items_dataset.csv
│  ├─ olist_order_payments_dataset.csv
│  ├─ olist_customers_dataset.csv
│  └─ olist_products_dataset.csv
```
├─ app.py
├─ init_db.py
├─ test_duckdb.py
├─ ecommerce.duckdb
├─ requirements.txt
└─ README.md
```

## 数据下载与准备

本项目未直接上传原始数据文件到 GitHub，因此在运行项目前，需要先手动准备 `data/` 文件夹中的 CSV 数据。

### 需要准备的文件

请将以下文件放入项目根目录下的 `data/` 文件夹中：

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_products_dataset.csv`

### data 文件夹结构示例

```text
duckdb_streamlit_shop/
├─ data/
│  ├─ olist_orders_dataset.csv
│  ├─ olist_order_items_dataset.csv
│  ├─ olist_order_payments_dataset.csv
│  ├─ olist_customers_dataset.csv
│  └─ olist_products_dataset.csv
