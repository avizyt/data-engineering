#!/usr/bin/env python
# coding: utf-8
import time
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:4321/ny_taxi')

df_iter = pd.read_csv("./yellow_tripdata_2021-01.csv", iterator=True, chunksize=100000)

df = next(df_iter)


df.tpep_pickup_datetime =  pd.to_datetime((df.tpep_pickup_datetime))
df.tpep_dropoff_datetime =  pd.to_datetime((df.tpep_dropoff_datetime))

df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

engine.connect()




print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

while True:
    t_start = time.time()

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime((df.tpep_pickup_datetime))
    df.tpep_dropoff_datetime = pd.to_datetime((df.tpep_dropoff_datetime))

    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    t_end = time.time()

    print(f"inserted another chunk...{t_end - t_start:.3f} seconds")

