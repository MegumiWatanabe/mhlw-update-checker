import requests
from bs4 import BeautifulSoup
import hashlib
import os
import json
from datetime import datetime

def get_page_content():
    url = "https://www.mhlw.go.jp/stf/shingi/shingi-chuo_128166-2.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 議事録テーブルを取得
    table = soup.find('table')
    if table:
        return str(table)
    return None

def check_for_updates():
    current_content = get_page_content()
    if not current_content:
        print("ページの取得に失敗しました")
        return
    
    # 現在のコンテンツのハッシュを計算
    current_hash = hashlib.md5(current_content.encode()).hexdigest()
    
    # 前回のハッシュを読み込み
    hash_file = "last_hash.txt"
    try:
        with open(hash_file, 'r') as f:
            last_hash = f.read().strip()
    except FileNotFoundError:
        last_hash = ""
    
    # 比較
    if current_hash != last_hash:
        print(f"更新を検知しました！ {datetime.now()}")
        print("厚労省の中央社会保険医療協議会のページが更新されています")
        
        # 新しいハッシュを保存
        with open(hash_file, 'w') as f:
            f.write(current_hash)
        
        # GitHub Actionsの出力に設定
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write(f"updated=true\n")
    else:
        print(f"更新なし {datetime.now()}")
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write(f"updated=false\n")

if __name__ == "__main__":
    check_for_updates()
