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
        
    ########## 读取数据集 ##########

    # # 1.读取CSV文件
    # df_comment = spark.read.csv("hdfs://node1:8020/data/comment_small.csv", header=True, inferSchema=True,encoding='gbk')
    # df_basic = spark.read.csv("hdfs://node1:8020/data/basic_info_small.csv", header=True, inferSchema=True,encoding='gbk')
    # # 2.查看数据结构
    # df_comment.show(5)
    # df_basic.show(5)
    # # 3.合并两张数据表
    # df_combined = df_comment.join(df_basic, on="school_name", how="left")
    # df_combined.show(5)
    
    # 1. 从Hive表中读取数据
    df_comment = spark.sql("SELECT * FROM db.tb_comment_info")
    df_basic = spark.sql("SELECT * FROM db.tb_basic_info")
    # 2.查看数据结构
    df_comment.show(5)
    df_basic.show(5)
    # 3. 合并两张数据表
    df_combined = df_comment.join(df_basic, on="school_name", how="left")
    df_combined.where(df_combined.school_name == "清华大学").show(5)
    # 将所有NULL值替换为0
    df_combined = df_combined.fillna(0)
        
    ########## 评论分词 ##########
    # 1.停用词表
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
    self_stopwords = {'不到','无需','多言','完老陶','自绝','我小天','只能',
                      '葡萄','敬酒','我国','公里','真的','gh','0.05','大可',
                      '报了名','治标不治本','水岸','一万多个','柿庄','提呀',
                      '水疗','科张','幽静','顶住','南麓','读城规','工作制',
                      '两点钟','二百名','南二','掐断','麾下','确保','离锡东',
                      '遍漆','脸进','脸是','8.40','桥过','一长'}
    stopwords.update(self_stopwords)

    # 2.自定义分词和去停用词的函数
    def tokenize(text):
        if text is None:  # 检查是否为 None
            return []  # 返回空列表或其他默认值
        tokens = jieba.analyse.extract_tags(text,topK=3)
        tokens = [word for word in tokens if word not in stopwords and len(word) > 1]
        return tokens

    # 3.将tokenize函数注册为UDF
    tokenize_udf = udf(tokenize, ArrayType(StringType()))

    # 4.对评论进行分词处理
    df_tokenized = df_combined.withColumn("tokens", tokenize_udf(df_combined["comment_content"]))
    df_tokenized.show(5)
    
    # 5.过滤掉 tokens 列中值为空的行
    df_filtered = df_tokenized.filter(col("tokens").isNotNull() & (size(col("tokens")) > 0))
    
    # 6.显示过滤后的结果
    # df_filtered.show(5)
    
    ########## 添加学校基本信息到tokens ##########
    # 1.将985、211和学校层次等信息加入 tokens，并提升权重
    def add_basic_info_tokens(tokens, is_985, is_211, school_level):
        basic_info = []
        if is_985 == 1:
            basic_info.append("985^9")
        if is_211 == 1:
            basic_info.append("211^4")
        if school_level:
            basic_info.append(f"{school_level}^7")
        return tokens + basic_info
    # 2.注册 UDF 增加基本信息字段
    add_basic_info_tokens_udf = udf(add_basic_info_tokens, ArrayType(StringType()))
    df_with_basic_info = df_filtered.withColumn("tokens", add_basic_info_tokens_udf(col("tokens"), col("school_985"), col("school_211"), col("school_type")))
    
    
    ########## 关键词TF-IDF值计算 ##########
    # 1.设定CountVectorizer特征维度
    count_vectorizer = CountVectorizer(inputCol="tokens", outputCol="rawFeatures", vocabSize=200)

    # 2.计算词频
    cv_model = count_vectorizer.fit(df_with_basic_info)
    df_tf = cv_model.transform(df_with_basic_info)
    df_tf.show(5)

    # 3.计算TF-IDF值
    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(df_tf)
    df_tfidf = idfModel.transform(df_tf)
    df_tfidf.select("tokens", "features").show(3)

    # 4.查看计算后的TF-IDF值
    df_tfidf.select("school_name", "tokens", "features").show(5)
    
    ########## 关键词权值计算 ##########
    # 1.将TF-IDF结果转为关键词和权重的结构
    def extract_keywords(row):
        keywords = row["tokens"]
        features = row["features"].toArray()
        result = []
        for word, weight in zip(keywords, features):
            # 检查是否有权重调整符号 '^'
            if len(word) > 2 and word[-2] == '^':
                # 提取权重因子（最后一个字符）
                weight_factor = float(word[-1])  # 倒数第一位为权重因子
                weight *= weight_factor  # 调整权重
                
                # 去除最后两位（即 '^' 和权重因子）
                word = word[:-2]  # 去掉倒数两位
            result.append(Row(school_name=row['school_name'],keyword=word, weight=float(weight)))
        return result

    # 2.展平关键词和权重数据
    df_keywords = df_tfidf.rdd.flatMap(extract_keywords).toDF()
    df_keywords.show(5)

    # 3.按高校汇总关键词权重
    df_keywords_grouped = df_keywords.groupBy("school_name","keyword").agg(F.avg("weight").alias("avg_weight"))
    df_keywords_grouped.where("avg_weight > 0").where("school_name = '清华大学'").orderBy(col("avg_weight").desc()).show(10)

    ########## 保存结果到hive数据表中 ##########
    # 1.将结果保存为 Hive 数据表
    df_keywords_grouped.where("avg_weight > 0").write\
        .mode("overwrite")\
        .saveAsTable("db.tb_ske")  