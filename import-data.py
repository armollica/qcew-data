#!/usr/bin/env python

import pandas as pd
import numpy as np
import sqlalchemy as sql
from glob import glob

engine = sql.create_engine('postgresql://scott:tiger@localhost:5432/qcew')

csv_dtype = {
  'area_fips': object,
  'own_code': object,
  'industry_code': object,
  'agglvl_code': object,
  'size_code': object,
  'year': object,
  'qtr': object,
  'disclosure_code': object,
  'qtrly_estabs': np.int32,
  'month1_emplvl': np.int32,
  'month2_emplvl': np.int32,
  'month3_emplvl': np.int32,
  'total_qtrly_wages': np.int64,
  'taxable_qtrly_wages': np.int64,
  'qtrly_contributions': np.int64,
  'avg_wkly_wage': np.int32,
  'lq_disclosure_code': object,
  'lq_qtrly_estabs': np.float32,
  'lq_month1_emplvl': np.float32,
  'lq_month2_emplvl': np.float32,
  'lq_month3_emplvl': np.float32,
  'lq_total_qtrly_wages': np.float32,
  'lq_taxable_qtrly_wages': np.float32,
  'lq_qtrly_contributions': np.float32,
  'lq_avg_wkly_wage': np.float32,
  'oty_disclosure_code': object,
  'oty_qtrly_estabs_chg': np.int32,
  'oty_qtrly_estabs_pct_chg': np.float32,
  'oty_month1_emplvl_chg': np.int32,
  'oty_month1_emplvl_pct_chg': np.float32,
  'oty_month2_emplvl_chg': np.int32,
  'oty_month2_emplvl_pct_chg': np.float32,
  'oty_month3_emplvl_chg': np.int32,
  'oty_month3_emplvl_pct_chg': np.float32,
  'oty_total_qtrly_wages_chg': np.int64,
  'oty_total_qtrly_wages_pct_chg': np.float32,
  'oty_taxable_qtrly_wages_chg': np.int64,
  'oty_taxable_qtrly_wages_pct_chg': np.float32,
  'oty_qtrly_contributions_chg': np.int64,
  'oty_qtrly_contributions_pct_chg': np.float32,
  'oty_avg_wkly_wage_chg': np.int32,
  'oty_avg_wkly_wage_pct_chg': np.float32
}

sql_dtype = {
  'area_fips': sql.types.TEXT,
  'own_code': sql.types.TEXT,
  'industry_code': sql.types.TEXT,
  'agglvl_code': sql.types.TEXT,
  'size_code': sql.types.TEXT,
  'year': sql.types.TEXT,
  'qtr': sql.types.TEXT,
  'disclosure_code': sql.types.TEXT,
  'qtrly_estabs': sql.types.INTEGER,
  'month1_emplvl': sql.types.INTEGER,
  'month2_emplvl': sql.types.INTEGER,
  'month3_emplvl': sql.types.INTEGER,
  'total_qtrly_wages': sql.types.BIGINT,
  'taxable_qtrly_wages': sql.types.BIGINT,
  'qtrly_contributions': sql.types.BIGINT,
  'avg_wkly_wage': sql.types.INTEGER,
  'lq_disclosure_code': sql.types.TEXT,
  'lq_qtrly_estabs': sql.types.REAL,
  'lq_month1_emplvl': sql.types.REAL,
  'lq_month2_emplvl': sql.types.REAL,
  'lq_month3_emplvl': sql.types.REAL,
  'lq_total_qtrly_wages': sql.types.REAL,
  'lq_taxable_qtrly_wages': sql.types.REAL,
  'lq_qtrly_contributions': sql.types.REAL,
  'lq_avg_wkly_wage': sql.types.REAL,
  'oty_disclosure_code': sql.types.TEXT,
  'oty_qtrly_estabs_chg': sql.types.INTEGER,
  'oty_qtrly_estabs_pct_chg': sql.types.REAL,
  'oty_month1_emplvl_chg': sql.types.INTEGER,
  'oty_month1_emplvl_pct_chg': sql.types.REAL,
  'oty_month2_emplvl_chg': sql.types.INTEGER,
  'oty_month2_emplvl_pct_chg': sql.types.REAL,
  'oty_month3_emplvl_chg': sql.types.INTEGER,
  'oty_month3_emplvl_pct_chg': sql.types.REAL,
  'oty_total_qtrly_wages_chg': sql.types.BIGINT,
  'oty_total_qtrly_wages_pct_chg': sql.types.REAL,
  'oty_taxable_qtrly_wages_chg': sql.types.BIGINT,
  'oty_taxable_qtrly_wages_pct_chg': sql.types.REAL,
  'oty_qtrly_contributions_chg': sql.types.BIGINT,
  'oty_qtrly_contributions_pct_chg': sql.types.REAL,
  'oty_avg_wkly_wage_chg': sql.types.INTEGER,
  'oty_avg_wkly_wage_pct_chg': sql.types.REAL
}

# Get list of files that end in *singlefile.csv
file_names = glob('*singlefile.csv')

# Import is done in chunks of size = chunksize.
# A single csv has roughly 3.7 million rows,
# so a chunksize of 25000 leads to about 149 chunks
chunksize = 25000

# Import into database file-by-file, chunk-by-chunk
for file_name in file_names:
  print 'Importing ' + file_name
  reader = pd.read_csv(file_name, iterator=True, chunksize=chunksize, dtype=csv_dtype)
  i = 0
  for chunk in reader:
    i += 1
    print 'Writing chunk %s' % i
    chunk.to_sql('data', engine, if_exists='append', index=False, dtype=sql_dtype)
