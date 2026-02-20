########
## Data Ingestion V1.0.0
########

####################
#inports
###################
import click
import pandas as pd
from utils.globalVariables import prefix, dtype, parse_dates
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import sys
import os




@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option("--year", default=2021, type=int, help="Year of the taxi data (used to build URL)")
@click.option("--month", default=1, type=int, help="Month of the taxi data (1-12)")
@click.option("--chunksize", default=100000, type=int, help="Number of rows to process per chunk")
@click.option("--target-table", default="yellow_taxi_data", help="Name of the Postgres table to write to")
@click.option("--url", default=None, help="URL of the CSV file (overrides year/month computation)")
def run(pg_user, pg_pass,pg_host, pg_port, pg_db ,year, month, chunksize, target_table, url):

    ########################
    # globals from environment
    #######################
    PG_PASSWORD = pg_pass
    PG_USERNAME = pg_user
    HOSTNAME = pg_host
    PG_PORT = pg_port
    PG_DB = pg_db

    # if the URL wasn't supplied, build it using the year/month
    if url is None:
        month_str = f"{month:02d}"
        url = f"{prefix}yellow_tripdata_{year}-{month_str}.csv.gz"

    first = True

    #######
    #connect to sqlengine
    ######
    
    con_string  =  rf'postgresql://{PG_USERNAME}:{PG_PASSWORD}@{HOSTNAME}:{PG_PORT}/{PG_DB}'
    engine = create_engine(con_string)



    df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=chunksize,
)

    
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False
        else:
            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists='append'
            )

if __name__ == "__main__":
    run()
    




