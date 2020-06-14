import itertools    

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

from parser import generate_comments


COMMENTS_FILE = 'comments.csv'

generate_comments(COMMENTS_FILE)

context = pyspark.SparkContext('local[*]')
spark = SparkSession(context)

commentsFile = spark.read.text(COMMENTS_FILE)
wordCounts = commentsFile.select(
    explode(split(commentsFile.value, '\s+')).alias('word')
).groupBy('word').count()

words = iter(wordCounts.collect())
ordered_words = iter(sorted(words, key=lambda r: r.asDict()['count'], reverse=True))
first_10_words = list(itertools.islice(ordered_words, 10))
print(first_10_words)
