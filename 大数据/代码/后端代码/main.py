from flask import Flask, request, jsonify, render_template
from pyspark.sql import SparkSession
from flask import jsonify
from pyspark.sql import functions as F
from flask_cors import CORS,cross_origin
# import requests

app = Flask(__name__)
CORS(app)

# 初始化SparkSession
spark = SparkSession.builder.\
    appName("main").\
    master("local[*]").\
    config("spark.sql.warehouse.dir","hdfs://node1:8020/user/hive/warehouse").\
    config("hive.metastore.uris","thrift://node2:9083").\
    enableHiveSupport().\
    getOrCreate()
    

# 定义返回封装函数
def response(code=200, message='', data=None):
    """
    自定义返回结果的封装函数
    :param code: 状态码，默认为 200
    :param message: 提示信息，默认为空字符串
    :param data: 返回数据，默认为 None
    :return: Response 对象
    """
    response_data = {
        'code': code,
        'message': message,
        'data': data
    }
    return jsonify(response_data)


@app.route('/')
def fun_hello():
    return "hello word"

# 根据高校id 使用spark on hive查询对应高校关键词
@app.route("/keyword_school",methods=["POST"])
def get_keyword_by_school_id():
    # 1.从请求体中获取school_id参数
    name = request.json.get("school_name")
    # 2.通过 Spark on Hive 查询数据
    df = spark.sql(f"SELECT * FROM db.tb_ske where school_name='{name}'")
    # 3.输出data
    # 将 Spark DataFrame 转换为 Pandas DataFrame
    pandas_df = df.select("keyword", "avg_weight").toPandas()
    # 将 Pandas DataFrame 转换为字典
    keyword_weight_dict = pandas_df.set_index('keyword')['avg_weight'].to_dict()

    return response(code=200,message='success',data=keyword_weight_dict)  # 返回 JSON 格式的查询结果


# 首页：查看topN条数据,注意根据学校层次先进行一步过滤
@app.route("/bigdata/get_all_schools",methods=["POST"])
def get_all_schools():
    # 1.从请求体中获取topN参数
    topN = int(request.json.get("topN"))
    # 2.通过 Spark on Hive 查询数据
    # 2.1 查询基本信息表，并按照层次过滤，删除学校层次非'普通本科'的学校
    df_basic = spark.sql("SELECT * FROM db.tb_basic_info where school_level='普通本科' and school_985=1")
    # df_basic.show(5)
    # 2.2 查询高校评分表
    df_score = spark.sql("SELECT * FROM db.tb_sentiment_score")
    # df_score.show(5)
    # 2.3 inner join 只保留有评分的高校
    df_basic_score_joined = df_basic.join(df_score, on="school_name", how="inner")
    # df_joined.show(5)
    # 2.4 查询高校排名信息
    df_rank = spark.sql("select * from db.tb_rank_info")
    # 2.5 左连接融合高校排名信息
    df_joined = df_basic_score_joined.join(df_rank, on='school_name', how='left')
    # 2.6 获取topN
    df_top_n = df_joined.orderBy("sentiment_score", ascending=False).limit(topN)
    # 2.7 查询学校关键词
    # 获取 TopN 学校名称列表
    school_names = [row["school_name"] for row in df_top_n.collect()]
    school_names_str = ",".join([f"'{name}'" for name in school_names])  # 转换成 SQL 中的 IN 子句格式
    # 查询关键词表
    df_keyword = spark.sql(f"""
        SELECT school_name, keyword AS name, avg_weight AS value
        FROM db.tb_ske
        WHERE school_name IN ({school_names_str})
    """)
    # 转换关键词为嵌套结构
    df_keywords_grouped = df_keyword.groupBy("school_name").agg(
        F.collect_list(F.struct(F.col("name"), F.col("value"))).alias("keywords")
    )

    # 2.8 将关键词与 TopN 学校详细信息合并
    df_result = df_top_n.join(df_keywords_grouped, on="school_name", how="left")
    
    # # 转换为 JSON 格式并返回
    # result = [row.asDict() for row in df_result.collect()]
    # 转换为 JSON 格式并修正 keywords 格式
    result = []
    for row in df_result.collect():
        row_dict = row.asDict()
        if "keywords" in row_dict and row_dict["keywords"] is not None:
            # 将 keywords 转换为 [{"name": ..., "value": ...}]
            row_dict["keywords"] = [
                {"name": keyword["name"], "value": keyword["value"]}
                for keyword in row_dict["keywords"]
            ]
        result.append(row_dict)
    

    
    return response(code=200,message='success',data=result)  # 返回 JSON 格式的查询结果

# 模型匹配
from text2vec import SentenceModel
from tools.sim_match import find_top5_similar_schools


model = SentenceModel('./model/embedding_model')
embedding_data = './embedding_result/embedding_all_school.pkl'
# embedding_data ="/home/xyh/0_name_match/embedding_data/DJ_person_dic_0_10w.jsonl"

# 增加超时时间（以秒为单位）
app.config['SERVER_TIMEOUT'] = 3000  

@app.route('/search')
def home():
    return render_template('index.html')  # 渲染 index.html 页面


@app.route('/bigdata/predict', methods=['POST'])
def predict():
    try:
        real_name_json = request.get_json()
        real_name = real_name_json["key_word"]
        print('Keyword is: {}'.format(real_name))
        candidate_name=find_top5_similar_schools(model,embedding_data, real_name)

    except Exception as e:
        print('The error is: ',e)

    return (candidate_name)





@app.route("/bigdata/get_global_keywords",methods=['POST'])
def get_global_keywords():
    df_keyword = spark.sql("select * from db.tb_gske order by avg_weight desc limit 40")
    keywords_list = df_keyword.collect()
    keywords = [{"name":row.keyword,"value":row.avg_weight} for row in keywords_list]
    return response(code=200,message='success',data=keywords)


@app.route("/bigdata/get_province_count",methods=['POST'])
def get_province_count():
    df_province = spark.sql("select * from db.tb_province_count order by school_count desc limit 12")
    province_list = df_province.collect()
    provinces = [{"region":row.school_pos,"count":row.school_count} for row in province_list]
    return response(code=200,message='success',data=provinces)





if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True, port=8000)
