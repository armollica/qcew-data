# Pull QCEW data

This repo provides scripts that download all of the publicly 
available QCEW data after 1990 and import it into a database.

## What's the QCEW?
The [Quarterly Census of Employment and Wages (QCEW)](http://www.bls.gov/cew/) 
publishes quarterly counts of employment and wages as reported by employers. 
The census covers 98% of U.S. jobs and is broken out by industry and
by various geographic levels (county, metro area, state, national).
To look around at the data the BLS has a 
["data views" app](http://www.bls.gov/cew/apps/data_views/data_views.htm)
that lets you filter down to certain subsets of the data just for recent 
years (2012-2015).

## Downloading the data
Running the `download-data.sh` bash script will download and decompress all
of the QCEW "single file" csv's (see the BLS's 
[QCEW Data Files page](http://www.bls.gov/cew/datatoc.htm)). There are 
25 csv's that will be downloaded, one for each year from 1990 to 2015.
These are large files, in total they are about 36.4 GB uncompressed, so this
will take a long time to process.

## Importing into a database
Running the `import-data.py` python script will import the downloaded csv's
into a database. You will need to change the 
[SQLAlchemy engine configuration](http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html)
in this script (line 8) so that it points to your database. It is currently 
set up for a PostgreSQL database named "qcew." This is a large import job
so this will also take a long time to process. The import is done
in chunks to avoid running into memory issues. The default chunk size is
25,000 rows but this can be changed in the script.

## What do I need to run these scripts?
To run the `download-data.sh` bash script you'll need `bash` and a
couple other command line tools, `curl` and `unzip`. I believe these
come standard on Unix systems. On Windows you'll need to install them. There
are two easy options I know of, [Cygwin](https://www.cygwin.com/) and 
[MinGW](http://www.mingw.org/). MinGW also comes with git-bash which you can 
download at [git-scm.com/downloads](https://git-scm.com/downloads).

To run the `import-data.py` script you'll need 
[python](https://www.python.org/) and two modules, 
[pandas](http://pandas.pydata.org/) 
and 
[sqlalchemy](http://www.sqlalchemy.org/). You can install these with 