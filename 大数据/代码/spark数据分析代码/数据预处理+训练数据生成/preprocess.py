from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql import Window

# 初始化Spark会话
spark = SparkSession.builder.\
appName("school_keyword_extraction").\
master("local[*]").\
config("spark.sql.warehouse.dir","hdfs://node1:8020/user/hive/warehouse").\
config("hive.metastore.uris","thrift://node2:9083").\
enableHiveSupport().\
getOrCreate()

# 读取Excel文件
basic_file = spark.read.format("com.crealytics.spark.excel").option("header", "true").option("dataAddress", "'Sheet1'!A2").load("/data/origin_basic_info.xlsx")
comment_file = spark.read.format("com.crealytics.spark.excel").option("header", "true").load("/data/origin_comment_info.xlsx")
rank_file = spark.read.format("com.crealytics.spark.excel").option("header", "true").load("/data/origin_rank_info.xlsx")
# 选择所需的列
new_basic = basic_file.select('学校', '省份', '水平层次', '办学类型', '985', '211', '双一流')
new_rank = rank_file.select('学校名称', '软科排名', '校友会排名', '武书连排名', 'QS世界排名', 'US世界排名')

# 过滤符合条件的数据
new_basic = new_basic.filter(col('学校').isin(comment_file.select('school_name').rdd.flatMap(lambda x: x).collect()))
new_rank = new_rank.filter(col('学校名称').isin(comment_file.select('school_name').rdd.flatMap(lambda x: x).collect()))

# 排序并筛选评论
window_spec = Window.partitionBy('bizId').orderBy(col('lightCount').desc())
new_comment = comment_file.withColumn("row_num", row_number().over(window_spec)).filter(col("row_num") <= 50).select('school_name', 'commentContent', 'publishTime')

# 填充缺失值和替换值
new_basic = new_basic.fillna(0)
new_basic = new_basic.replace({'985': {'是': 1, '否': 0}, '211': {'是': 1, '否': 0}, '双一流': {'是': 1, '否': 0}})

# 写入CSV文件
new_rank.coalesce(1).write.csv('/data/rank_info.csv', header=True, mode='overwrite')
new_basic.coalesce(1).write.csv('/data/basic_info.csv', header=True, mode='overwrite')
new_comment.coalesce(1).write.csv('/data/comment_info_short.csv', header=True, mode='overwrite')
comment_file.coalesce(1).write.csv('/data/comment_info.csv', header=True, mode='overwrite')

# 停止Spark会话
spark.stop()
