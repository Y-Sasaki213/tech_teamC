import sqlite3

DB_NAME = "recruit.db"


# =========================
# DB接続用の関数
# =========================
def get_db_connection():
    """
    SQLiteに接続するための関数。

    row_factoryを設定すると、
    row["name"] のようにカラム名で値を取得できる。
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# DB初期化用
# =========================
def init_db():
    """
    schema.sqlを読み込んでDBテーブルを作成する。

    注意：
    schema.sql に DROP TABLE が書かれている場合、
    実行すると既存データは消える。
    """
    conn = get_db_connection()

    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()
