from flask import Flask, render_template, request, redirect, url_for

from db import get_db_connection, init_db
from alerts import get_candidate_alerts, get_popup_alerts

import sqlite3
import os


app = Flask(__name__)


# =========================
# 一覧画面 Read + 検索
# =========================

@app.route("/")
def index():
    search_name = request.args.get("name", "")
    search_owner = request.args.get("owner", "")

    conn = get_db_connection()

    sql = """
        SELECT
            c.id,
            c.name,
            c.owner,
            c.profile_url,
            c.contact_status,
            c.created_at,
            c.updated_at,
            c.last_updated_field,
            p.first_interview_date,
            p.second_interview_date,
            p.final_interview_date,
            p.final_interview,
            p.pizza_party_plan,
            p.offer_deadline,
            p.first_period,
            p.second_period,
            p.final_period
        
        
        FROM candidates c
        LEFT JOIN candidate_progress p
        ON c.id = p.candidate_id
        WHERE 1 = 1
          AND (
              c.contact_status IS NULL
              OR c.contact_status = ''
              OR c.contact_status NOT IN ('内定承諾', '辞退', 'お見送り', 'ミス')
              )


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
            COALESCE(c.owner, '') ASC,
            c.name ASC
    """

    candidates = conn.execute(sql, params).fetchall()
    conn.close()

    candidate_list = []

    for candidate in candidates:
        candidate_dict = dict(candidate)

        # =========================
        # 次回選考日を判定する処理
        # =========================
        current_phase = candidate_dict.get("last_updated_field")

        next_selection_date = ""

        if current_phase == "新規登録":
            next_selection_date = candidate_dict.get("first_interview_date")

        elif current_phase == "カジュアル面談/説明会":
            next_selection_date = candidate_dict.get("first_interview_date")

        elif current_phase == "書類選考":
            next_selection_date = candidate_dict.get("first_interview_date")

        elif current_phase == "一次面接":
            next_selection_date = candidate_dict.get("second_interview_date")

        elif current_phase == "二次面接":
            next_selection_date = candidate_dict.get("final_interview_date")

        elif current_phase == "最終面接":
            next_selection_date = candidate_dict.get("pizza_party_plan")

        elif current_phase == "内定":
            next_selection_date = candidate_dict.get("offer_deadline")

        candidate_dict["next_selection_date"] = next_selection_date or "-"

        alerts = get_candidate_alerts(candidate_dict)
        candidate_dict["alerts"] = alerts
        candidate_dict["has_alert"] = len(alerts) > 0
        candidate_dict["alert_count"] = len(alerts)

        candidate_list.append(candidate_dict)

    # アラートありの候補者を上に出しつつ、担当者名順に並べる
    candidate_list.sort(
        key=lambda x: (
            not x["has_alert"],
            x["owner"] or "",
            x["name"] or ""
        )
    )

    popup_alerts = get_popup_alerts(candidate_list)

    return render_template(
        "index.html",
        candidates=candidate_list,
        search_name=search_name,
        search_owner=search_owner,
        popup_alerts=popup_alerts,
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
    profile_url = request.form.get("profile_url")
    contact_status = request.form.get("contact_status")
    contact_memo = request.form.get("contact_memo")

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
    final_period = request.form.get("final_period")
    final_interview_date = request.form.get("final_interview_date")
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
            profile_url,
            contact_status,
            contact_memo,
            created_at,
            updated_at,
            last_updated_field
        )
        VALUES (?, ?, ?, ?, ?,
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)
    """, (name, owner, profile_url,contact_status, contact_memo, "新規登録"))


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
            final_interview_date,
            final_period,
            final_interview,
            pizza_party_plan,
            pizza_party_join,
            acceptance_estimate,
            offer_deadline
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?)
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
            final_interview_date,
            final_period,
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
# 詳細画面用：アラート対象項目の判定
# =========================
def build_alert_marks(alerts):
    """
    アラート文を見て、詳細画面のどの項目にマークを付けるか判定する。

    戻り値の例：
    {
        "basic": False,
        "first_interview": False,
        "second_interview": True,
        "second_period": True,
        "second_interview_date": True,
    }
    """

    marks = {
        "basic": False,

        "first_interview": False,
        "first_period": False,
        "first_interview_date": False,

        "second_interview": False,
        "second_period": False,
        "second_interview_date": False,

        "final_phase": False,
        "final_interview": False,

        "offer_deadline": False,
        "pizza_party_plan": False,
    }

    for alert in alerts:
        # 最終更新アラートは基本情報にマーク
        if "最終更新" in alert:
            marks["basic"] = True

        # 一次面接関連
        if "一次面接" in alert:
            marks["first_interview"] = True

            if "実施予定時期" in alert:
                marks["first_period"] = True
                marks["first_interview_date"] = True

            if "一次面接日" in alert:
                marks["first_interview_date"] = True

        # 二次面接関連
        if "二次面接" in alert:
            marks["second_interview"] = True

            if "実施予定時期" in alert:
                marks["second_period"] = True
                marks["second_interview_date"] = True

            if "二次面接日" in alert:
                marks["second_interview_date"] = True

        # 最終面接関連
        if "最終面接" in alert:
            marks["final_phase"] = True
            marks["final_interview"] = True

        # ピザパ関連
        if "ピザパ" in alert:
            marks["final_phase"] = True
            marks["pizza_party_plan"] = True

        # 内定締切関連
        if "内定" in alert or "締切" in alert:
            marks["final_phase"] = True
            marks["offer_deadline"] = True

    return marks

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
            c.profile_url,
            c.contact_status,
            c.contact_memo,
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

    alerts = get_candidate_alerts(candidate) or []
    alert_marks = build_alert_marks(alerts)

    return render_template(
    "detail.html",
    candidate=candidate,
    alerts=alerts,
    has_alert=len(alerts) > 0,
    alert_marks=alert_marks
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
            c.profile_url,
            c.contact_status,
            c.contact_memo,
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
    profile_url = request.form.get("profile_url")
    contact_status = request.form.get("contact_status")
    contact_memo = request.form.get("contact_memo")
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
    final_period = request.form.get("final_period")
    final_interview_date = request.form.get("final_interview_date")
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
        last_updated_field = "カジュアル面談/説明会"

    elif old_data["document_screening"] != document_screening:
        last_updated_field = "書類選考"

    elif old_data["first_interview_date"] != first_interview_date:
        last_updated_field = "一次面接"

    elif old_data["second_interview_date"] != second_interview_date:
        last_updated_field = "二次面接"

    elif old_data["final_interview_date"] != final_interview_date:
        last_updated_field = "最終面接"

    elif old_data["offer_deadline"] != offer_deadline:
        last_updated_field = "内定"

    # candidatesテーブルを更新
    cursor.execute("""
        UPDATE candidates
        SET
            name = ?,
            owner = ?,
            profile_url = ?,
            contact_status = ?,
            contact_memo = ?,
            updated_at = CURRENT_TIMESTAMP,
            last_updated_field = ?
        WHERE id = ?
    """, (name, owner,profile_url, contact_status, contact_memo, last_updated_field, id))

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
            final_period = ?,
            final_interview = ?,
            final_interview_date = ?,
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
        final_period,
        final_interview,
        final_interview_date,
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

    return redirect(url_for("addpage"))

# ============
# 使い方ページ
# ============

@app.route("/usage")
def usage_page():
    return render_template("usage.html")

# =========================
# その他記入欄
# =========================

def add_contact_memo_column():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE candidates ADD COLUMN contact_memo TEXT")
        conn.commit()
        print("contact_memo カラムを追加しました")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("contact_memo カラムはすでに存在しています")
        else:
            raise e
    finally:
        conn.close()

# ====================
# 選考外の一覧ページ
# ====================
@app.route("/addpage")
def addpage():
    conn = sqlite3.connect("recruit.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 内定承諾の候補者だけ取得
    cur.execute("""
        SELECT *
        FROM candidates
        WHERE contact_status = '内定承諾'
        ORDER BY updated_at DESC
    """)
    completed_candidates = cur.fetchall()

    # 辞退の候補者だけ取得
    cur.execute("""
        SELECT *
        FROM candidates
        WHERE contact_status = '辞退'
        ORDER BY updated_at DESC
    """)
    decline_candidates = cur.fetchall()

     # お見送りの候補者だけ取得
    cur.execute("""
        SELECT *
        FROM candidates
        WHERE contact_status = 'お見送り'
        ORDER BY updated_at DESC
    """)
    seeing_candidates = cur.fetchall()

     # ミスの候補者だけ取得
    cur.execute("""
        SELECT *
        FROM candidates
        WHERE contact_status = 'ミス'
        ORDER BY updated_at DESC
    """)
    miss_candidates = cur.fetchall()


    conn.close()

   
    return render_template(
        "addpage.html",
        completed_candidates=completed_candidates,
        decline_candidates=decline_candidates,
        seeing_candidates=seeing_candidates,
        miss_candidates=miss_candidates
    )


# 選考外ページへの移動

@app.route("/move_to_outside/<int:id>", methods=["POST"])
def move_to_outside(id):
    outside_status = request.form.get("outside_status")

    if outside_status == "":
        return "選考外ステータスを選択してください"

    conn = sqlite3.connect("recruit.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        UPDATE candidates
        SET contact_status = ?
        WHERE id = ?
    """, (outside_status, id))

    conn.commit()
    conn.close()

    return redirect(url_for("addpage"))


# =========================
# アプリ起動
# =========================
#add_contact_memo_column()


if __name__ == "__main__":
    if not os.path.exists("recruit.db"):
        init_db()   

    app.run(debug=True)


