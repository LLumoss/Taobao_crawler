from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
import mysql.connector
from mysql.connector import Error


# 加载保存的cookie
def load_cookies(driver, cookie_file):
    with open(cookie_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)


# 获取前五个商品名称和销量
def get_top_five_products(driver):
    product_xpaths = [
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[1]/div/div[1]/div[2]/div/span",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[2]/div/div[1]/div[2]/div/span",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[3]/div/div[1]/div[2]/div/span",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[4]/div/div[1]/div[2]/div/span",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[5]/div/div[1]/div[2]/div/span",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[6]/div/div[1]/div[2]/div/span",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[7]/div/div[1]/div[2]/div/span",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[8]/div/div[1]/div[2]/div/span",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[9]/div/div[1]/div[2]/div/span"
    ]

    # 使用新的销量 XPath 路径
    sales_xpaths = [
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[1]/div/div[1]/div[4]/span[2]",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[2]/div/div[1]/div[4]/span[2]",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[3]/div/div[1]/div[4]/span[2]",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[4]/div/div[1]/div[4]/span[2]",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[5]/div/div[1]/div[4]/span[2]",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[6]/div/div[1]/div[4]/span[2]",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[7]/div/div[1]/div[4]/span[2]",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[8]/div/div[1]/div[4]/span[2]",
        "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[3]/div/a[9]/div/div[1]/div[4]/span[2]"
    ]

    top_five_data = []

    for product_xpath, sales_xpath in zip(product_xpaths, sales_xpaths):
        product = driver.find_element(By.XPATH, product_xpath)
        sales = driver.find_element(By.XPATH, sales_xpath)
        product_name = product.text
        product_sales = sales.text
        top_five_data.append((product_name, product_sales))
        print(f"Product Name: {product_name}, Sales: {product_sales}")  # 输出商品名称和销量

    return top_five_data


# 数据库配置信息
db_config = {
    'host': 'localhost',
    'user': 'root',  # 替换为你的MySQL用户名
    'password': '2222',  # 替换为你的MySQL密码
    'database': 'tb_crawler'  # 替换为你的数据库名
}


# 连接数据库
def connect_to_db():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# 插入数据到数据库
def insert_product_data(product_data):
    connection = connect_to_db()
    if connection is not None:
        cursor = connection.cursor()
        for product_name, product_sales in product_data:
            query = "INSERT INTO top_products (product_name, sales, date) VALUES (%s, %s, CURDATE())"
            cursor.execute(query, (product_name, product_sales))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    connection.close()


# 主程序
def main():
    driver = webdriver.Chrome()
    driver.get('https://s.taobao.com/search?page=1&q=%E8%A1%A3%E6%9C%8D&tab=all')

    load_cookies(driver, 'taobao_cookies.pkl')  # 请替换为你的cookie文件名
    driver.refresh()

    time.sleep(5)

    sales_sort_xpath = "/html/body/div[4]/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div/div[1]/div/div/div/ul/li[2]/div"
    sales_sort_button = driver.find_element(By.XPATH, sales_sort_xpath)
    sales_sort_button.click()

    time.sleep(5)

    top_five_data = get_top_five_products(driver)
    insert_product_data(top_five_data)  # 插入数据到数据库

    driver.quit()


if __name__ == "__main__":
    main()
