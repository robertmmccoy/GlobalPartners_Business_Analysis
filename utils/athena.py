import pandas as pd
from pyathena import connect

def get_connection():
    return connect(
        s3_staging_dir="s3://globalpartners-gold-robert/athena-results/",
        region_name="us-east-1"
    )

def run_query(sql):
    conn = get_connection()
    return pd.read_sql(sql, conn)
