# import streamlit as st
#
# st.title("电商交易分析仪表盘")
# st.write("这是我的第一个 DuckDB + Streamlit 项目页面。")


# import streamlit as st
# import duckdb
#
# st.title("电商交易分析仪表盘")
#
# con = duckdb.connect("ecommerce.duckdb")
#
# delivered_orders = con.execute("""
#     SELECT COUNT(*)
#     FROM orders
#     WHERE order_status = 'delivered'
# """).fetchone()[0]
#
# st.metric("已送达订单数", f"{delivered_orders:,}")






# # 月度 GMV 趋势图
# import streamlit as st
# import duckdb
#
# st.title("电商交易分析仪表盘")
#
# # 连接本地数据库文件
# con = duckdb.connect("ecommerce.duckdb")
#
# # KPI1：已送达订单数
# delivered_orders = con.execute("""
#     SELECT COUNT(*)
#     FROM orders
#     WHERE order_status = 'delivered'
# """).fetchone()[0]
#
# # KPI2：只按 delivered 口径统计的 GMV
# delivered_gmv = con.execute("""
#     SELECT ROUND(SUM(oi.price), 2)
#     FROM orders o
#     JOIN order_items oi
#         ON o.order_id = oi.order_id
#     WHERE o.order_status = 'delivered'
# """).fetchone()[0]
#
# # KPI3：客单价 = GMV / 去重后的订单数
# aov = con.execute("""
#     SELECT ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2)
#     FROM orders o
#     JOIN order_items oi
#         ON o.order_id = oi.order_id
#     WHERE o.order_status = 'delivered'
# """).fetchone()[0]
#
# # KPI4：覆盖州数
# states_count = con.execute("""
#     SELECT COUNT(DISTINCT c.customer_state)
#     FROM orders o
#     JOIN customers c
#         ON o.customer_id = c.customer_id
#     WHERE o.order_status = 'delivered'
# """).fetchone()[0]
#
# col1, col2, col3, col4 = st.columns(4)
#
# col1.metric("已送达订单数", f"{delivered_orders:,}")
# col2.metric("GMV", f"{delivered_gmv:,.2f}")
# col3.metric("AOV", f"{aov:,.2f}")
# col4.metric("覆盖州数", f"{states_count:,}")
#
# # 月度 GMV 趋势
# monthly_gmv = con.execute("""
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
# st.subheader("月度 GMV 趋势")
# st.line_chart(monthly_gmv.set_index("month"))
#
# # 支付方式分布表
# payment_df = con.execute("""
#     SELECT
#         CASE
#             WHEN op.payment_type = 'credit_card' THEN '信用卡'
#             WHEN op.payment_type = 'boleto' THEN '银行票据'
#             WHEN op.payment_type = 'voucher' THEN '代金券'
#             WHEN op.payment_type = 'debit_card' THEN '借记卡'
#             ELSE op.payment_type
#         END AS 支付方式,
#         COUNT(DISTINCT o.order_id) AS 订单数,
#         ROUND(SUM(op.payment_value), 2) AS 支付总额
#     FROM orders o
#     JOIN order_payments op
#         ON o.order_id = op.order_id
#     WHERE o.order_status = 'delivered'
#     GROUP BY op.payment_type
#     ORDER BY 支付总额 DESC
# """).fetchdf()
# st.subheader("支付方式分布")
# st.dataframe(payment_df, use_container_width=True)
#
# # 各州订单 Top 10
# state_df = con.execute("""
#     SELECT
#         c.customer_state AS 州,
#         COUNT(DISTINCT o.order_id) AS 订单数
#     FROM orders o
#     JOIN customers c
#         ON o.customer_id = c.customer_id
#     WHERE o.order_status = 'delivered'
#     GROUP BY c.customer_state
#     ORDER BY 订单数 DESC
#     LIMIT 10
# """).fetchdf()
#
# st.subheader("各州订单 Top 10")
# st.bar_chart(state_df.set_index("州"))



# 优化，美观
import streamlit as st
import duckdb

st.set_page_config(page_title="电商交易分析仪表盘")

st.title("电商交易分析仪表盘")

status_map = {
    "已送达": "delivered",
    "已发货": "shipped",
    "已取消": "canceled",
    "缺货/不可用": "unavailable",
    "已开票": "invoiced",
    "处理中": "processing",
    "已创建": "created",
    "已批准": "approved"
}

status_label = st.selectbox("选择订单状态", list(status_map.keys()))
status_option = status_map[status_label]

# 连接本地数据库文件
con = duckdb.connect("ecommerce.duckdb")
def run_query(sql):
    return con.execute(sql)

# KPI1：当前状态订单数
order_count = run_query(f"""
    SELECT COUNT(*)
    FROM orders
    WHERE order_status = '{status_option}'
""").fetchone()[0]

# KPI2：当前状态下的 GMV
gmv = run_query(f"""
    SELECT ROUND(SUM(oi.price), 2)
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = '{status_option}'
""").fetchone()[0]
if gmv is None:
    gmv = 0

# KPI3：当前状态下的客单价
aov = run_query(f"""
    SELECT ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2)
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = '{status_option}'
""").fetchone()[0]
if aov is None:
    aov = 0

# KPI4：当前状态下覆盖州数
states_count = run_query(f"""
    SELECT COUNT(DISTINCT c.customer_state)
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = '{status_option}'
""").fetchone()[0]
if states_count is None:
    states_count = 0

# 当前状态下的月度 GMV 趋势
monthly_gmv = run_querye(f"""
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
        ROUND(SUM(oi.price), 2) AS monthly_gmv
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = '{status_option}'
    GROUP BY 1
    ORDER BY 1
""").fetchdf()

# 当前状态下的支付方式分布
payment_df = run_query(f"""
    SELECT
        CASE
            WHEN op.payment_type = 'credit_card' THEN '信用卡'
            WHEN op.payment_type = 'boleto' THEN '银行票据'
            WHEN op.payment_type = 'voucher' THEN '代金券'
            WHEN op.payment_type = 'debit_card' THEN '借记卡'
            ELSE op.payment_type
        END AS 支付方式,
        COUNT(DISTINCT o.order_id) AS 订单数,
        ROUND(SUM(op.payment_value), 2) AS 支付总额
    FROM orders o
    JOIN order_payments op
        ON o.order_id = op.order_id
    WHERE o.order_status = '{status_option}'
    GROUP BY op.payment_type
    ORDER BY 支付总额 DESC
""").fetchdf()

# 当前状态下的各州订单 Top 10
state_df = run_query(f"""
    SELECT
        c.customer_state AS 州,
        COUNT(DISTINCT o.order_id) AS 订单数
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = '{status_option}'
    GROUP BY c.customer_state
    ORDER BY 订单数 DESC
    LIMIT 10
""").fetchdf()

col1, col2, col3, col4 = st.columns(4)

col1.metric(f"{status_label}订单数", f"{order_count:,}")
col2.metric("GMV", f"{gmv:,.2f}")
col3.metric("AOV", f"{aov:,.2f}")
col4.metric("覆盖州数", f"{states_count:,}")

st.subheader(f"{status_label}订单月度 GMV 趋势")
st.line_chart(monthly_gmv.set_index("month"))

st.subheader(f"{status_label}订单支付方式分布")
if payment_df.empty:
    st.info("当前订单状态下没有支付方式数据。")
else:
    st.dataframe(payment_df, use_container_width=True, hide_index=True)

st.subheader(f"{status_label}订单各州 Top 10")
if state_df.empty:
    st.info("当前订单状态下没有各州分布数据。")
else:
    st.dataframe(state_df, use_container_width=True, hide_index=True)