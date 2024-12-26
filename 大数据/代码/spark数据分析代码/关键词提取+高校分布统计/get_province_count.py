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
import jieba.analyse

if __name__=='__main__':
    # 初始化SparkSession
    spark = SparkSession.builder.\
        appName("global_keyword_extraction").\
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
        
        
    # 切换到目标数据库
    spark.sql("USE db")

    # 执行 SQL 查询并直接统计
    result_df = spark.sql("""
        SELECT 
            school_pos, 
            COUNT(*) AS school_count
        FROM tb_basic_info
        GROUP BY school_pos
    """)

    # 创建目标表（如果不存在）
    spark.sql("""
        CREATE TABLE IF NOT EXISTS tb_province_count (
            school_pos STRING,
            school_count INT
        )
    """)

    # 将结果写入目标表（覆盖模式）
    result_df.write.mode("overwrite").saveAsTable("tb_province_count")

    print("Data successfully written to tb_province_count.")