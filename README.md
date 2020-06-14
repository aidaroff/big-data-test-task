## DONE

1. parser
2. word counter

## TODOS

1. add plotting for top 10 words
2. push results to hdfs/kafka
3. add postgres connection
4. add NewsItem model with more metadata and save to pg
5. add rest endpoints
6. add word filters (words like `и`, `на` are not valuable enough of data)

## Instructions to get the program working locally (work in progress)

(now)
1. Make sure you have Python3.6+
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python main.py`

(work in progress)
1. `touch .hdfscli.cfg`
2. `export HDFSCLI_CONFIG=.hdfscli.cfg`
3. `pip install -r requirements.txt`
4. 

