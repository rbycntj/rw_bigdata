# encoding:utf8
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.ml.feature import HashingTF, IDF
from pyspark.sql import functions as F
from pyspark.sql.functions import col, size
from pyspark.sql import Row
from pyspark.ml.feature import CountVectorizer
import jieba


if __name__=='__main__':
    # 初始化SparkSession
    spark = SparkSession.builder.\
        appName("school_keyword_extraction").\
        master("local[*]").\
        config("spark.sql.warehouse.dir","hdfs://node1:8020/user/hive/warehouse").\
        config("hive.metastore.uris","thrift://node2:9083").\
        config("spark.driver.memory", "8g"). \
        config("spark.executor.memory", "4g"). \
        config("spark.executor.instances", "4"). \
        config("spark.executor.cores", "2"). \
        config("spark.storage.memoryFraction", "0.3"). \
        config("spark.memory.storageFraction", "0.3"). \
        config("spark.shuffle.spill", "true"). \
        config("spark.shuffle.spill.compress", "true"). \
        enableHiveSupport().\
        getOrCreate()
        
    cn_stopwords_df = spark.read.option("encoding", "GBK").text("hdfs://node1:8020/data/cn_stopwords.txt")
    baidu_stopwords_df = spark.read.option("encoding", "GBK").text("hdfs://node1:8020/data/baidu_stopwords.txt")
    hit_stopwords_df = spark.read.option("encoding", "GBK").text("hdfs://node1:8020/data/hit_stopwords.txt")
    scu_stopwords_df = spark.read.option("encoding", "GBK").text("hdfs://node1:8020/data/scu_stopwords.txt")
    
    # 将 DataFrame 转换为 RDD
    cn_stopwords_rdd = cn_stopwords_df.rdd.map(lambda row: row[0])
    baidu_stopwords_rdd = baidu_stopwords_df.rdd.map(lambda row: row[0])
    hit_stopwords_rdd = hit_stopwords_df.rdd.map(lambda row: row[0])
    scu_stopwords_rdd = scu_stopwords_df.rdd.map(lambda row: row[0])

    # 使用 union 合并多个 RDD，并去重
    all_stopwords_rdd = cn_stopwords_rdd \
        .union(baidu_stopwords_rdd) \
        .union(hit_stopwords_rdd) \
        .union(scu_stopwords_rdd) \
        .distinct()  # 去重

    # 将合并后的 RDD 转换为停用词集合
    stopwords = set(all_stopwords_rdd.collect())
    print(stopwords)