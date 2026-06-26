DROP TABLE IF EXISTS candidate_progress;
DROP TABLE IF EXISTS candidates;

CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    owner TEXT,
    profile_url TEXT,
    contact_status TEXT NOT NULL DEFAULT '未連絡',
    contact_memo TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_field TEXT DEFAULT '新規登録'
);

CREATE TABLE candidate_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER NOT NULL,

    casual_event_staff TEXT,
    document_screening TEXT DEFAULT '未済',
    initial_remind TEXT DEFAULT '未済',

    first_interview_date TEXT,
    first_interviewer TEXT,
    first_meeting TEXT,
    first_tel TEXT DEFAULT '未済',
    first_remind TEXT DEFAULT '未済',
    first_period TEXT,

    second_interview_date TEXT,
    second_interviewer TEXT,
    second_tel TEXT DEFAULT '未済',
    second_remind TEXT DEFAULT '未済',
    transcript TEXT DEFAULT '未済',
    second_period TEXT,
    final_period TEXT,
    final_interview_date TEXT,
    final_interview TEXT,
    pizza_party_plan TEXT,
    pizza_party_join TEXT,
    acceptance_estimate TEXT,
    offer_deadline TEXT,

    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- =========================
-- デモ用データ（10件）
-- =========================

INSERT INTO candidates (id, name, owner, contact_status, created_at, updated_at, last_updated_field) VALUES
(1, '青木悠斗', '加藤', '未連絡', datetime('now', '-10 days'), datetime('now', '-10 days'), '一次面接'),
(2, '石井結菜', '冨永', '学生返答待ち', datetime('now', '-12 days'), datetime('now', '-12 days'), '二次面接'),
(3, '井上大翔', '山本', '面接官の返答待ち', datetime('now', '-15 days'), datetime('now', '-15 days'), '最終面接'),

(4, '上田葵', '北原', '未連絡', datetime('now'), datetime('now'), '書類選考'),
(5, '岡田陽菜', '加藤', '学生返答待ち', datetime('now'), datetime('now'), '一次面接'),
(6, '金子颯太', '冨永', '未連絡', datetime('now'), datetime('now'), '二次面接'),
(7, '木村結衣', '山本', '保留', datetime('now'), datetime('now'), '最終面接'),
(8, '小島拓海', '北原', '未連絡', datetime('now'), datetime('now'), '書類選考'),
(9, '斎藤蓮', '加藤', '学生返答待ち', datetime('now'), datetime('now'), '一次面接'),
(10, '清水陽翔', '冨永', '未連絡', datetime('now'), datetime('now'), 'カジュアル面談/説明会');


--  アラート対象（3件）
INSERT INTO candidate_progress (
candidate_id,
casual_event_staff,
document_screening,
initial_remind,
first_interview_date,
first_period,
second_interview_date,
second_period,
final_interview_date,
final_period
) VALUES
(1, '担当A', '済', '未済', date('now', '-10 days'), '6月中旬', NULL, NULL, NULL, NULL),
(2, '担当B', '済', '未済', '2026-06-10', NULL, NULL, '6月下旬', NULL, NULL),
(3, '担当C', '済', '未済', '2026-06-01', NULL, '2026-06-05', NULL, NULL, NULL);


--  通常データ（7件）
INSERT INTO candidate_progress (
candidate_id,
casual_event_staff,
document_screening,
initial_remind,
first_interview_date,
first_period,
second_interview_date,
second_period,
final_interview_date,
final_period,
pizza_party_plan,
offer_deadline
) VALUES
(4, NULL, '未済', '未済', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(5, NULL, '済', '済', '2026-07-01', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(6, NULL, '済', '済', '2026-06-20', NULL, '2026-07-05', NULL, NULL, NULL, NULL, NULL),
(7, NULL, '済', '済', '2026-06-20', NULL, '2026-06-30', NULL, '2026-07-10', NULL, NULL, NULL),
(8, NULL, '未済', '未済', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(9, NULL, '済', '未済', '2026-07-02', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(10, '担当D', '未済', '未済', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
