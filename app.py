import sqlite3
import csv
import numpy as np
from flask import Flask, render_template, request, jsonify
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

    global hover_times
    hover_times = {}
    global file_counter
    file_counter += 1

    # 先頭行のラベルを除く
    recipe_list_deleted_label = recipe_list[1:]

    # シードを固定
    # random.seed(1)

    # ランダムに10件のレシピを取得
    result_list = random.sample(recipe_list_deleted_label, 20)
    
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

# ファイルのカウンターを初期化
file_counter = 0

# /update_hover_time ルート
@app.route('/update_hover_time', methods=['POST'])
def update_hover_time():

    # ルート関数内でリクエストやセッションにアクセスする
    # (これはリクエストのコンテキスト内です)
    data = request.get_json()
    recipe_name = data.get('recipe')
    hover_time = data.get('time')

    hover_times[recipe_name] = hover_time

    # CSV ファイルにデータを保存
    save_hover_time_to_csv(hover_times)

    return jsonify(success=True)

def save_hover_time_to_csv(hover_times):
    global file_counter
    csv_filename = get_current_filename('./result/B_hover_times_', 'csv')

    with open(csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['recipe_name', 'hover_time'])  # ヘッダーを書き込む
        for recipe_name, hover_time in hover_times.items():
            writer.writerow([recipe_name, hover_time])

    print(f'Data saved to {csv_filename}')

def get_current_filename(base_name, extension):
    global file_counter
    filename = f"{base_name}_{file_counter}.{extension}"
    return filename


if __name__ == "__main__":
    app.run(debug=True, port=3000)