from flask import Flask, render_template, request, redirect, url_for

from db import get_db_connection, init_db
from alerts import get_candidate_alerts


app = Flask(__name__)


# =========================
# 一覧画面 Read + 検索
# =========================
@app.route("/")
def index():
    # 検索条件をGETパラメータから取得
    search_name = request.args.get("name", "")
    search_owner = request.args.get("owner", "")

    conn = get_db_connection()

    # ベースSQL
    sql = """
        SELECT
            c.id,
            c.name,
            c.owner,
            c.contact_status,
            c.created_at,
            c.updated_at,
            c.last_updated_field,
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

    # 採用者氏名で部分一致検索
    if search_name:
        sql += " AND c.name LIKE ?"
        params.append(f"%{search_name}%")

    # 担当者名で部分一致検索
    if search_owner:
        sql += " AND c.owner LIKE ?"
        params.append(f"%{search_owner}%")

    # 待ち状態の候補者を上に出しつつ、更新日が新しい順に並べる
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

        # 候補者ごとのアラートを取得
        alerts = get_candidate_alerts(candidate)

        candidate_dict["alerts"] = alerts
        candidate_dict["has_alert"] = len(alerts) > 0
        candidate_dict["alert_count"] = len(alerts)

        candidate_list.append(candidate_dict)

    # アラートありの候補者を一番上に表示する
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

    # candidatesテーブルに基本情報を登録
    cursor.execute("""
        INSERT INTO candidates (
            name,
            owner,
            contact_status,
            created_at,
            updated_at
            last_updated_field
        )
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (name, owner, contact_status, "新規登録"))

    # 直前に登録した候補者IDを取得
    candidate_id = cursor.lastrowid

    # candidate_progressテーブルに採用フロー情報を登録
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
# 詳細画面 Read？
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
            c.last_updated_field,
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
            c.last_updated_field,
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

    # 更新前のデータを取得
    old_data = conn.execute("""
    SELECT *
    FROM candidate_progress
    WHERE candidate_id = ?
""", (id,)).fetchone()


    last_updated_field = "変更なし"

    #if casual_event_staff:       #入力されているだけで更新扱い
        #last_updated_field = "カジュアル面談"

    if old_data["casual_event_staff"] != casual_event_staff:
        last_updated_field = "カジュアル面談"

    elif old_data["document_screening"] != document_screening:
        last_updated_field = "書類選考"

    elif old_data["first_interview_date"] != first_interview_date:
        last_updated_field = "一次面接"

    elif old_data["first_meeting"] != first_meeting:
        last_updated_field = "座談会"

    elif old_data["second_interview_date"] != second_interview_date:
        last_updated_field = "二次面接"

    elif old_data["transcript"] != transcript:
        last_updated_field = "成績証明"

    elif old_data["final_interview"] != final_interview:
        last_updated_field = "最終面接"

    elif old_data["pizza_party_join"] != pizza_party_join:
        last_updated_field = "ピザパ参加"

    elif old_data["acceptance_estimate"] != acceptance_estimate:
        last_updated_field = "承諾目安"

    elif old_data["offer_deadline"] != offer_deadline:
        last_updated_field = "内定〆切"

    # candidatesテーブルを更新
    cursor.execute("""
        UPDATE candidates
        SET
            name = ?,
            owner = ?,
            contact_status = ?,
            updated_at = CURRENT_TIMESTAMP,
            last_updated_field = ?
        WHERE id = ?
    """, (name, owner, contact_status, last_updated_field, id))

    # candidate_progressテーブルを更新
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

# ============
# 使い方ページ
# ============

@app.route("/usage")
def usage_page():
    return render_template("usage.html")



# =========================
# アプリ起動
# =========================
if __name__ == "__main__":
    # 初回DB作成時だけ使う場合は、下のコメントを外す
    # init_db()

  conn = get_db_connection()



  app.run(debug=True)
