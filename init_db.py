# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
# print("数据库文件已创建")


# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# con.execute("""
#     CREATE OR REPLACE TABLE orders AS
#     SELECT *
#     FROM read_csv_auto('data/olist_orders_dataset.csv')
# """)
#
# print("orders表已创建")

# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# result = con.execute("""
#     SELECT COUNT(*) AS total_orders
#     FROM orders
# """).fetchall()
#
# print(result)


# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# con.execute("""
#     CREATE OR REPLACE TABLE orders AS
#     SELECT *
#     FROM read_csv_auto('data/olist_orders_dataset.csv')
# """)
#
# con.execute("""
#     CREATE OR REPLACE TABLE order_items AS
#     SELECT *
#     FROM read_csv_auto('data/olist_order_items_dataset.csv')
# """)
#
# con.execute("""
#     CREATE OR REPLACE TABLE order_payments AS
#     SELECT *
#     FROM read_csv_auto('data/olist_order_payments_dataset.csv')
# """)
#
# con.execute("""
#     CREATE OR REPLACE TABLE customers AS
#     SELECT *
#     FROM read_csv_auto('data/olist_customers_dataset.csv')
# """)
#
# con.execute("""
#     CREATE OR REPLACE TABLE products AS
#     SELECT *
#     FROM read_csv_auto('data/olist_products_dataset.csv')
# """)
#
# print("5张表已全部导入数据库")

#
# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# result = con.execute("SHOW TABLES").fetchdf()
#
# print(result)

# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT *
#     FROM orders
#     LIMIT 5
# """).fetchdf()
#
# print(df)

#
# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT *
#     FROM orders
#     LIMIT 1
# """).fetchdf()
#
# print(df.columns.tolist())




# 查正式表里的订单状态分布
# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT
#         order_status,
#         COUNT(*) AS order_count
#     FROM orders
#     GROUP BY order_status
#     ORDER BY order_count DESC
# """).fetchdf()
#
# print(df)


# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT *
#     FROM order_items
#     LIMIT 1
# """).fetchdf()
#
# print(df.columns.tolist())


# 总销售额
# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT
#         ROUND(SUM(price), 2) AS total_gmv
#     FROM order_items
# """).fetchdf()
#
# print(df)


# 只统计 orders.order_status = 'delivered' 的订单，并和 order_items 关联后求和。
# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT
#         ROUND(SUM(oi.price), 2) AS delivered_gmv
#     FROM orders o
#     JOIN order_items oi
#         ON o.order_id = oi.order_id
#     WHERE o.order_status = 'delivered'
# """).fetchdf()
#
# print(df)
# 粗略总额：13591643.7
# 已送达订单 GMV：13221498.11
#
# 这说明有一部分订单明细属于没真正完成成交的订单，所以如果直接全加，会高估销售额


# 客单价 AOV
# 定义成：
# AOV = delivered_gmv / delivered_orders
# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT
#         ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS aov
#     FROM orders o
#     JOIN order_items oi
#         ON o.order_id = oi.order_id
#     WHERE o.order_status = 'delivered'
# """).fetchdf()
#
# print(df)
#     aov
# 0  137.04


# 月度 GMV 趋势
# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT
#         DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
#         ROUND(SUM(oi.price), 2) AS monthly_gmv
#     FROM orders o
#     JOIN order_items oi
#         ON o.order_id = oi.order_id
#     WHERE o.order_status = 'delivered'
#     GROUP BY 1
#     ORDER BY 1
# """).fetchdf()
#
# print(df)


# 比较两种 GMV 口径,同一张表里同时输出：
# 全部订单金额
# delivered 订单金额
# 两者差额
# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT
#         ROUND(all_gmv, 2) AS all_gmv,
#         ROUND(delivered_gmv, 2) AS delivered_gmv,
#         ROUND(all_gmv - delivered_gmv, 2) AS diff_gmv
#     FROM (
#         SELECT
#             SUM(oi.price) AS all_gmv,
#             SUM(
#                 CASE
#                     WHEN o.order_status = 'delivered' THEN oi.price
#                     ELSE 0
#                 END
#             ) AS delivered_gmv
#         FROM orders o
#         JOIN order_items oi
#             ON o.order_id = oi.order_id
#     ) t
# """).fetchdf()
#
# print(df)


# 支付方式分布
# import duckdb
#
# con = duckdb.connect("ecommerce.duckdb")
#
# df = con.execute("""
#     SELECT
#         op.payment_type,
#         COUNT(DISTINCT o.order_id) AS order_count,
#         ROUND(SUM(op.payment_value), 2) AS total_payment_value
#     FROM orders o
#     JOIN order_payments op
#         ON o.order_id = op.order_id
#     WHERE o.order_status = 'delivered'
#     GROUP BY op.payment_type
#     ORDER BY total_payment_value DESC
# """).fetchdf()
#
# print(df)




# 各州订单数 Top 10
import duckdb

con = duckdb.connect("ecommerce.duckdb")

df = con.execute("""
    SELECT
        c.customer_state,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_state
    ORDER BY order_count DESC
    LIMIT 10
""").fetchdf()

print(df)