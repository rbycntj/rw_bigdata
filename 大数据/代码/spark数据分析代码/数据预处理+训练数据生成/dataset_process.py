from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# 创建 SparkSession 对象
spark = SparkSession.builder.\
appName("school_keyword_extraction").\
master("local[*]").\
config("spark.sql.warehouse.dir","hdfs://node1:8020/user/hive/warehouse").\
config("hive.metastore.uris","thrift://node2:9083").\
enableHiveSupport().\
getOrCreate()

# 读取 CSV 文件
tmp = spark.read.csv('/data/comment_info.csv', header=True, inferSchema=True)

print("Finish reading")

# 选择需要的列
train_data = tmp.select('school_name', 'commentContent', 'score')

# 将 score 列转换为大于5则为1，否则为0
train_data = train_data.withColumn('score', when(col('score') > 5, 1).otherwise(0).cast('int'))

# 保存到 CSV 文件
train_data.coalesce(1).write.csv('/data/comment_dataset', mode='overwrite', header=True)

print("Finish writing")

# 停止 SparkSession
spark.stop()