import os
import sys
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, Word2Vec, StringIndexer
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# 初始化Spark会话
spark = SparkSession.builder \
    .appName("OptimizedTextClassificationModelTraining") \
    .config("spark.driver.extraJavaOptions", "-Dfile.encoding=UTF-8") \
    .config("spark.executor.extraJavaOptions", "-Dfile.encoding=UTF-8") \
    .getOrCreate()

# 设置日志级别为ERROR
spark.sparkContext.setLogLevel("ERROR")

# 加载训练数据
weibo_senti_df = spark.read.csv("/data/comment_dataset/comment_data.csv", header=True, inferSchema=True)

# 数据清洗和检查
weibo_senti_df = weibo_senti_df.filter(weibo_senti_df["commentContent"].isNotNull())
weibo_senti_df = weibo_senti_df.withColumn("commentContent", weibo_senti_df["commentContent"].cast("string"))

# 划分数据集
train_df, test_df = weibo_senti_df.randomSplit([0.7, 0.3], seed=42)

# 构建Pipeline
tokenizer = Tokenizer(inputCol="commentContent", outputCol="rawWords")
stop_words_remover = StopWordsRemover(inputCol="rawWords", outputCol="filteredWords")
word2vec = Word2Vec(vectorSize=128, minCount=5, inputCol="filteredWords", outputCol="features")
label_stringIdx = StringIndexer(inputCol="score", outputCol="labelIndex")
classifier = RandomForestClassifier(featuresCol="features", labelCol="labelIndex", numTrees=100)

pipeline = Pipeline(stages=[tokenizer, stop_words_remover, word2vec, label_stringIdx, classifier])

# 训练模型
model = pipeline.fit(train_df)

# 模型评估
test_predictions = model.transform(test_df)
print(test_predictions)
evaluator = MulticlassClassificationEvaluator(labelCol="labelIndex", predictionCol="prediction", metricName="accuracy")
test_accuracy = evaluator.evaluate(test_predictions)
print(f"Test Dataset Accuracy: {test_accuracy}")

# 模型保存
model_path = "hdfs://node1:8020/data/model_data_optimized"
model.write().overwrite().save(model_path)

# 停止Spark会话
spark.stop()
