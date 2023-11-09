import sqlite3
import csv
import numpy as np
from flask import Flask, render_template, request, escape
from sklearn import preprocessing
from datetime import datetime
import random


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/resultB", methods = ["POST"])
def resultB():
    # テンプレートに結果を渡してレンダリング
    recommended_recipes = recommended_recipe_list()
    return render_template('results.html', recommended_recipes=recommended_recipes)

def mood_sql():
    # データベースに接続
    conn = sqlite3.connect("recipe.db")
    cursor = conn.cursor()

    # データベースからデータを取得
    cursor.execute('SELECT * FROM recipe')
    result = cursor.fetchall()

    # 取得したデータをリストに格納
    recipe_list = []
    for row in result:
        recipe_list.append(list(row))

    # データベース接続を閉じる
    cursor.close()
    conn.close()
    return recipe_list


def recommended_recipe_list():
    # データベースからデータを取得
    recipe_list = mood_sql()

    # 先頭行のラベルを除く
    recipe_list_deleted_label = recipe_list[1:]

    # シードを固定
    random.seed(1)

    # ランダムに10件のレシピを取得
    result_list = random.sample(recipe_list_deleted_label, 10)
    
    write_csv(result_list)

    return result_list

# リストをcsvファイルに書き込む
def write_csv(list):
    DATE = datetime.now().strftime("%Y%m%d_%H%M%S")
    FILE_NAME = "./result/data_"+DATE+".csv"
    with open(FILE_NAME, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in list:
            writer.writerow([row[0]])
        f.close()

if __name__ == "__main__":
    app.run(debug=True, port=3000)