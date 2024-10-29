from flask import Flask, jsonify, render_template
import mysql.connector
import plotly.express as px
import pandas as pd
import os

app = Flask(__name__)

# 数据库配置信息
db_config = {
    'host': 'localhost',
    'user': 'root',  # 替换为你的MySQL用户名
    'password': '2222',  # 替换为你的MySQL密码
    'database': 'tb_crawler'  # 替换为你的数据库名
}

# 从数据库获取产品数据
def get_product_data():
    try:
        connection = mysql.connector.connect(**db_config)
        query = "SELECT id, product_name, date, sales FROM top_products"
        df = pd.read_sql(query, connection)
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            connection.close()
    return df

# 生成树状图并保存为图片
@app.route('/generate_tree')
def generate_tree():
    df = get_product_data()
    if df.empty:
        return jsonify({'status': 'error', 'message': 'No data found in database'})

    # 使用 Plotly 生成树状图
    fig = px.treemap(df, path=['product_name'], values='sales', title="产品销量树状图")
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    fig.write_image("static/images/tree_map.png")
    return jsonify({'status': 'success', 'image_path': '/static/images/tree_map.png'})

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 获取产品数据的API
@app.route('/data')
def get_data():
    df = get_product_data()
    return df.to_json(orient='records')

if __name__ == "__main__":
    app.run(debug=True)
