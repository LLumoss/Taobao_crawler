import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

from fbprophet import Prophet

# df = pd.read_csv('test_data.csv', encoding='gbk')

# 读取 CSV 文件
df = pd.read_csv('test.csv')

# 确保数据中包含商品名称这一列
# 假设列名为 'product_name'
if 'product_name' not in df.columns:
    raise ValueError("CSV 文件中没有 'product_name' 列。")

# 使用 jieba 进行中文分词
def chinese_tokenizer(text):
    return list(jieba.cut(text))

# 创建 TF-IDF 向量化器，指定分词器
vectorizer = TfidfVectorizer(tokenizer=chinese_tokenizer)

# 将商品名称转换为 TF-IDF 矩阵
tfidf_matrix = vectorizer.fit_transform(df['product_name'])

# 获取词汇表
feature_names = vectorizer.get_feature_names_out()

# 打印每个商品名称的关键词
for i, product in enumerate(df['product_name']):
    print(f"商品：{product}")
    tfidf_scores = tfidf_matrix[i].toarray()[0]  # 获取当前商品的 TF-IDF 得分
    # 将关键词及其得分组合，并按得分排序
    keywords = sorted(zip(feature_names, tfidf_scores), key=lambda x: x[1], reverse=True)[:3]
    # 过滤掉得分为零的关键词
    keywords = [kw for kw, score in keywords if score > 0]
    print("关键词：", keywords)




# 1. 读取 CSV 文件，假设文件名为 'sales_data.csv'
df = pd.read_csv('test.csv')

# 2. 将 CSV 文件中的列进行重新命名，并正确处理日期格式
df['ds'] = pd.to_datetime(df['date'], dayfirst=True)  # 设置 dayfirst=True 处理 DD/MM/YYYY 格式
df['y'] = df['sell']  # 将 'sell' 列重命名为 'y'

# 只保留 Prophet 需要的两列：ds 和 y
df = df[['ds', 'y']]

# 3. 创建 Prophet 模型
model = Prophet()

# 4. 训练模型
model.fit(df)

# 5. 生成未来日期并预测，假设预测未来30天
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# 6. 打印并可视化预测结果
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
model.plot(forecast)
plt.show()

# 假设你已经有数据并进行了 Prophet 预测
fig = m.plot(forecast)

# 保存图片到 static/images 文件夹
fig.savefig('static/images/prophet_prediction.png')

