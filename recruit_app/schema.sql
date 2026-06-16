DROP TABLE IF EXISTS candidate_progress;
DROP TABLE IF EXISTS candidates;

CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    owner TEXT,
    contact_status TEXT NOT NULL DEFAULT '未連絡',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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

    final_interview TEXT,
    pizza_party_plan TEXT,
    pizza_party_join TEXT,
    acceptance_estimate TEXT,
    offer_deadline TEXT,

    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

