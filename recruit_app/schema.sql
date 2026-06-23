DROP TABLE IF EXISTS candidate_progress;
DROP TABLE IF EXISTS candidates;

CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    owner TEXT,
    contact_status TEXT NOT NULL DEFAULT '未連絡',
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

INSERT INTO candidates (
    name,
    owner,
    contact_status,
    created_at,
    updated_at,
    last_updated_field
)
VALUES (
    'テスト太郎',
    '佐々木',
    '担当者待ち',
    datetime('now', '-8 days'),
    datetime('now', '-8 days'),
    '一次面接'
);

INSERT INTO candidate_progress (
    candidate_id,
    first_interview_date,
    second_interview_date,
    final_interview,
    pizza_party_plan,
    offer_deadline
)
VALUES (
    1,
    date('now', '-8 days'),
    NULL,
    NULL,
    NULL,
    NULL
);
