from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DB_NAME = "recruit.db"

# =========================
# DB接続用の関数
# =========================
def get_db_connection():
    """
    SQLiteに接続するための関数。
    row_factoryを設定すると、row["name"] のようにカラム名で値を取得できる。
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# 日付変換用
# =========================
def parse_date(date_text):
    """
    DBから取得した日付文字列を datetime 型に変換する関数。

    対応する形式：
    - 2026-06-15
    - 2026-06-15 10:30:00

    空文字やNoneの場合は None を返す。
    """
    if not date_text:
        return None

    # SQLiteのCURRENT_TIMESTAMP形式
    try:
        return datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pass

    # input type="date" の形式
    try:
        return datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        return None


def is_over_7_days(date_text):
    """
    指定された日付から7日以上経過しているか判定する。
    """
    target_date = parse_date(date_text)

    if target_date is None:
        return False

    now = datetime.now()

    return now - target_date >= timedelta(days=7)

def days_since(date_text):
    target_date = parse_date(date_text)

    if target_date is None:
        return None

    now = datetime.now()
    return (now - target_date).days

# =========================
# アラート判定ロジック
# =========================
def get_candidate_alerts(candidate):

    alerts = []

    waiting_statuses = [
        "学生返答待ち",
        "面接官の返答待ち",
        "学生待ち",
        "担当者待ち",
        "面接官待ち"
    ]

    contact_status = candidate["contact_status"]

    # -------------------------
    # パターンA：ステップ遅延
    # -------------------------
    if contact_status in waiting_statuses:

        # 一次 → 二次
        if (
            candidate["first_interview_date"]
            and is_over_7_days(candidate["first_interview_date"])
            and not candidate["second_interview_date"]
        ):
            days = days_since(candidate["first_interview_date"])
            alerts.append(
                f"一次面接から{days}日経過していますが、二次面接日が未入力です。"
            )

        # 二次 → 最終
        if (
            candidate["second_interview_date"]
            and is_over_7_days(candidate["second_interview_date"])
            and not candidate["final_interview"]
        ):
            days = days_since(candidate["second_interview_date"])
            alerts.append(
                f"二次面接から{days}日経過していますが、最終面接日が未入力です。"
            )

    # -------------------------
    # パターンB：単純経過
    # -------------------------
    date_fields = [
        ("一次面接日", candidate["first_interview_date"]),
        ("二次面接日", candidate["second_interview_date"]),
        ("最終面接日", candidate["final_interview"]),
        ("ピザパ予定日", candidate["pizza_party_plan"]),
        ("内定締切日", candidate["offer_deadline"]),
    ]

    for label, date_value in date_fields:
        if date_value and is_over_7_days(date_value):
            days = days_since(date_value)
            alerts.append(f"{label}から{days}日経過しています。")

    # -------------------------
    # 更新日ベース
    # -------------------------
    closed_statuses = ["お見送り", "内定承諾", "辞退"]

    if contact_status not in closed_statuses:
        if candidate["updated_at"] and is_over_7_days(candidate["updated_at"]):
            days = days_since(candidate["updated_at"])
            alerts.append(
                f"最終更新から{days}日経過しています。対応状況を確認してください。"
            )

    return alerts

@app.route("/")
def index():

    # 検索条件
    search_name = request.args.get("name", "")
    search_owner = request.args.get("owner", "")

    conn = get_db_connection()

    # SQL
    sql = """
        SELECT
            c.id,
            c.name,
            c.owner,
            c.contact_status,
            c.created_at,
            c.updated_at,
            p.first_interview_date,
            p.second_interview_date,
            p.final_interview,
            p.pizza_party_plan,
            p.offer_deadline
        FROM candidates c
        JOIN candidate_progress p
        ON c.id = p.candidate_id
        WHERE 1 = 1
    """

    params = []

    if search_name:
        sql += " AND c.name LIKE ?"
        params.append(f"%{search_name}%")

    if search_owner:
        sql += " AND c.owner LIKE ?"
        params.append(f"%{search_owner}%")

    sql += """
ORDER BY
    (c.contact_status IN (
        '学生返答待ち',
        '面接官の返答待ち',
        '学生待ち',
        '担当者待ち',
        '面接官待ち'
    )) DESC,
    c.updated_at DESC
"""


    candidates = conn.execute(sql, params).fetchall()
    conn.close()

    candidate_list = []

    for candidate in candidates:
        candidate_dict = dict(candidate)

        alerts = get_candidate_alerts(candidate)

        candidate_dict["alerts"] = alerts
        candidate_dict["has_alert"] = len(alerts) > 0
        candidate_dict["alert_count"] = len(alerts)

        candidate_list.append(candidate_dict)

    candidate_list.sort(
      key=lambda x: (x["has_alert"], x["updated_at"]),
      reverse=True
)


    return render_template(
        "index.html",
        candidates=candidate_list,
        search_name=search_name,
        search_owner=search_owner
    )
# =========================
# 新規登録画面
# =========================
@app.route("/candidates/new")
def new_candidate():
    return render_template("new.html")


# =========================
# 新規登録処理 Create
# =========================
@app.route("/candidates/create", methods=["POST"])
def create_candidate():
    name = request.form.get("name")
    owner = request.form.get("owner")
    contact_status = request.form.get("contact_status")

    casual_event_staff = request.form.get("casual_event_staff")
    document_screening = request.form.get("document_screening")
    initial_remind = request.form.get("initial_remind")

    first_interview_date = request.form.get("first_interview_date")
    first_interviewer = request.form.get("first_interviewer")
    first_meeting = request.form.get("first_meeting")
    first_tel = request.form.get("first_tel")
    first_remind = request.form.get("first_remind")
    first_period = request.form.get("first_period")

    second_interview_date = request.form.get("second_interview_date")
    second_interviewer = request.form.get("second_interviewer")
    second_tel = request.form.get("second_tel")
    second_remind = request.form.get("second_remind")
    transcript = request.form.get("transcript")
    second_period = request.form.get("second_period")

    final_interview = request.form.get("final_interview")
    pizza_party_plan = request.form.get("pizza_party_plan")
    pizza_party_join = request.form.get("pizza_party_join")
    acceptance_estimate = request.form.get("acceptance_estimate")
    offer_deadline = request.form.get("offer_deadline")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates (
            name,
            owner,
            contact_status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (name, owner, contact_status))

    candidate_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO candidate_progress (
            candidate_id,
            casual_event_staff,
            document_screening,
            initial_remind,
            first_interview_date,
            first_interviewer,
            first_meeting,
            first_tel,
            first_remind,
            first_period,
            second_interview_date,
            second_interviewer,
            second_tel,
            second_remind,
            transcript,
            second_period,
            final_interview,
            pizza_party_plan,
            pizza_party_join,
            acceptance_estimate,
            offer_deadline
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_id,
        casual_event_staff,
        document_screening,
        initial_remind,
        first_interview_date,
        first_interviewer,
        first_meeting,
        first_tel,
        first_remind,
        first_period,
        second_interview_date,
        second_interviewer,
        second_tel,
        second_remind,
        transcript,
        second_period,
        final_interview,
        pizza_party_plan,
        pizza_party_join,
        acceptance_estimate,
        offer_deadline
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# =========================
# 詳細画面 Read
# =========================
@app.route("/candidates/<int:id>")
def detail_candidate(id):
    conn = get_db_connection()

    candidate = conn.execute("""
        SELECT
            c.id AS candidate_id,
            c.name,
            c.owner,
            c.contact_status,
            c.created_at,
            c.updated_at,
            p.*
        FROM candidates c
        JOIN candidate_progress p
        ON c.id = p.candidate_id
        WHERE c.id = ?
    """, (id,)).fetchone()

    conn.close()

    if candidate is None:
        return "候補者が見つかりませんでした", 404

    alerts = get_candidate_alerts(candidate)

    return render_template(
        "detail.html",
        candidate=candidate,
        alerts=alerts,
        has_alert=len(alerts) > 0
    )


# =========================
# 編集画面
# =========================
@app.route("/candidates/<int:id>/edit")
def edit_candidate(id):
    conn = get_db_connection()

    candidate = conn.execute("""
        SELECT
            c.id AS candidate_id,
            c.name,
            c.owner,
            c.contact_status,
            c.created_at,
            c.updated_at,
            p.*
        FROM candidates c
        JOIN candidate_progress p
        ON c.id = p.candidate_id
        WHERE c.id = ?
    """, (id,)).fetchone()

    conn.close()

    if candidate is None:
        return "候補者が見つかりませんでした", 404

    return render_template("edit.html", candidate=candidate)


# =========================
# 更新処理 Update
# =========================
@app.route("/candidates/<int:id>/update", methods=["POST"])
def update_candidate(id):
    name = request.form.get("name")
    owner = request.form.get("owner")
    contact_status = request.form.get("contact_status")

    casual_event_staff = request.form.get("casual_event_staff")
    document_screening = request.form.get("document_screening")
    initial_remind = request.form.get("initial_remind")

    first_interview_date = request.form.get("first_interview_date")
    first_interviewer = request.form.get("first_interviewer")
    first_meeting = request.form.get("first_meeting")
    first_tel = request.form.get("first_tel")
    first_remind = request.form.get("first_remind")
    first_period = request.form.get("first_period")

    second_interview_date = request.form.get("second_interview_date")
    second_interviewer = request.form.get("second_interviewer")
    second_tel = request.form.get("second_tel")
    second_remind = request.form.get("second_remind")
    transcript = request.form.get("transcript")
    second_period = request.form.get("second_period")

    final_interview = request.form.get("final_interview")
    pizza_party_plan = request.form.get("pizza_party_plan")
    pizza_party_join = request.form.get("pizza_party_join")
    acceptance_estimate = request.form.get("acceptance_estimate")
    offer_deadline = request.form.get("offer_deadline")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE candidates
        SET
            name = ?,
            owner = ?,
            contact_status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (name, owner, contact_status, id))

    cursor.execute("""
        UPDATE candidate_progress
        SET
            casual_event_staff = ?,
            document_screening = ?,
            initial_remind = ?,
            first_interview_date = ?,
            first_interviewer = ?,
            first_meeting = ?,
            first_tel = ?,
            first_remind = ?,
            first_period = ?,
            second_interview_date = ?,
            second_interviewer = ?,
            second_tel = ?,
            second_remind = ?,
            transcript = ?,
            second_period = ?,
            final_interview = ?,
            pizza_party_plan = ?,
            pizza_party_join = ?,
            acceptance_estimate = ?,
            offer_deadline = ?
        WHERE candidate_id = ?
    """, (
        casual_event_staff,
        document_screening,
        initial_remind,
        first_interview_date,
        first_interviewer,
        first_meeting,
        first_tel,
        first_remind,
        first_period,
        second_interview_date,
        second_interviewer,
        second_tel,
        second_remind,
        transcript,
        second_period,
        final_interview,
        pizza_party_plan,
        pizza_party_join,
        acceptance_estimate,
        offer_deadline,
        id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("detail_candidate", id=id))


# =========================
# 削除 Delete
# =========================
@app.route("/candidates/<int:id>/delete", methods=["POST"])
def delete_candidate(id):
    conn = get_db_connection()

    conn.execute("DELETE FROM candidates WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))

# =========================
# DB初期化用
# =========================
def init_db():
    """
    schema.sqlを読み込んでDBテーブルを作成する。
    注意：
    DROP TABLE がある場合、実行すると既存データは消える。
    """
    conn = get_db_connection()

    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()




# =========================
# アプリ起動
# =========================
if __name__ == "__main__":
    app.run(debug=True)
    # 初回DB作成時だけ使う
    # init_db()
