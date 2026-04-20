# import duckdb
#
# con = duckdb.connect()
#
# result = con.execute("""
#     SELECT *
#     FROM read_csv_auto('data/olist_orders_dataset.csv')
#     LIMIT 5
# """).fetchdf()
#
# print(result)

# import duckdb
#
# con = duckdb.connect()
#
# df = con.execute("""
#     SELECT *
#     FROM read_csv_auto('data/olist_orders_dataset.csv')
#     LIMIT 1
# """).fetchdf()
#
# print(df.columns.tolist())

import duckdb

con = duckdb.connect()

df = con.execute("""
    SELECT
        order_status,
        COUNT(*) AS order_count
    FROM read_csv_auto('data/olist_orders_dataset.csv')
    GROUP BY order_status
    ORDER BY order_count DESC
""").fetchdf()

print(df)