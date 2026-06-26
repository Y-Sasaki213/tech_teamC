# 新卒採用管理ツール README

---

## ■ アプリ概要
本アプリケーションは、新卒採用における候補者の情報・進捗・対応状況を一元管理するためのツールです。  
候補者ごとの選考フェーズや次回対応日を可視化し、対応漏れを防ぐことを目的としています。

---

## ■ 主要機能
- 候補者の新規登録
- 候補者一覧表示・検索
- 候補者情報の詳細確認
- 候補者情報の編集・更新
- 選考フェーズの自動更新表示
- 次回選考日の表示
- アラート表示（対応遅延の検知）
- 選考外候補者の管理

---

## ■ セットアップ手順
1. このアプリのフォルダをPCにダウンロードします  
   （GitHubの場合は「Code」→「Download ZIP」でダウンロード）

2. ダウンロードしたZIPファイルを解凍します  
   （右クリック →「すべて展開」）

3. 解凍したフォルダを開きます

4. フォルダ内で右クリックし、以下を選択します  
   - ターミナルで開く  
   - PowerShellで開く  

5. 仮想環境を作成します

```bash
python -m venv .venv
```

6. 仮想環境を有効化します

```bash
.venv\Scripts\activate
```

7. 必要なパッケージをインストールします

```bash
pip install flask
```

---

## ■ 起動方法
1. フォルダ内で以下を実行します

```bash
python start.py
```

2. 表示されるURLをブラウザで開きます

```
http://127.0.0.1:5000
```

---

## ■ 役割分担
- 候補者情報の登録・更新：各担当者  
- 進捗管理・確認：リーダー  
- アラート確認・対応：各担当者  

---

## ■ 画面一覧
- 候補者一覧画面  
- 新規登録画面  
- 詳細画面  
- 編集画面  
- 選考外一覧画面  
- 使い方画面  

---

## ■ DB設計

### candidates テーブル
- id  
- name  
- owner  
- profile_url  
- contact_status  
- contact_memo  
- created_at  
- updated_at  
- last_updated_field  

---

### candidate_progress テーブル
- id  
- candidate_id  
- casual_event_staff  
- document_screening  
- initial_remind  
- first_interview_date  
- first_interviewer  
- first_meeting  
- first_tel  
- first_remind  
- first_period  
- second_interview_date  
- second_interviewer  
- second_tel  
- second_remind  
- transcript  
- second_period  
- final_period  
- final_interview_date  
- final_interview  
- pizza_party_plan  
- pizza_party_join  
- acceptance_estimate  
- offer_deadline  
