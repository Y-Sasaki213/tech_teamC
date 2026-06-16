from datetime import datetime, timedelta


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
    """
    指定された日付から何日経過しているかを返す関数。
    """
    target_date = parse_date(date_text)

    if target_date is None:
        return None

    now = datetime.now()

    return (now - target_date).days


# =========================
# アラート判定ロジック
# =========================
def get_candidate_alerts(candidate):
    """
    候補者1人分のアラート一覧を作成する関数。

    戻り値の例：
    [
        "一次面接から10日経過していますが、二次面接日が未入力です。",
        "最終更新から8日経過しています。対応状況を確認してください。"
    ]
    """

    alerts = []

    # 対応待ちとして扱うステータス
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
    # 条件：
    # 1. 今のフェーズの日付が入力されている
    # 2. そこから7日以上経過している
    # 3. 次のフェーズの日付が未入力
    # 4. 連絡ステータスが待ち状態
    if contact_status in waiting_statuses:

        # 一次面接 → 二次面接
        if (
            candidate["first_interview_date"]
            and is_over_7_days(candidate["first_interview_date"])
            and not candidate["second_interview_date"]
        ):
            days = days_since(candidate["first_interview_date"])
            alerts.append(
                f"一次面接から{days}日経過していますが、二次面接日が未入力です。"
            )

        # 二次面接 → 最終面接
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
    # 任意の日付項目が入力されてから7日以上経過している場合
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
    # 候補者情報そのものが7日以上更新されていない場合
    closed_statuses = ["お見送り", "内定承諾", "辞退"]

    if contact_status not in closed_statuses:
        if candidate["updated_at"] and is_over_7_days(candidate["updated_at"]):
            days = days_since(candidate["updated_at"])
            alerts.append(
                f"最終更新から{days}日経過しています。対応状況を確認してください。"
            )

    return alerts
