# tech_teamC
anaai　ワロタ
mio　あほ
sasa パイセン
## 概要
チーム開発研修用のプロジェクト
 
## 開発ルール
 
### ブランチ
- `main`：本番
- `feature/your-feature-name`：作業用
 
### コミット
- `feat:` 新機能を追加するとき
- `fix:` 不具合を修正するとき
- `docs:` ドキュメントを更新するとき
 
### PRルール
- レビュー必須
- 内容記載必須
 
## セットアップ
 
```bash
git clone https://github.com/Y-Sasaki213/tech_teamC.git
cd Tech_Team_dev
```
 
## 開発フロー
 
### 1. ブランチ作成
 
```bash
git checkout -b feature/your-feature-name
```
 
### 2. 作業
機能追加や修正を行います。
 
### 3. コミット
 
```bash
git status
git add path/to/changed-file
git commit -m "docs: add development workflow section to README"
```
 
### 4. Push
 
```bash
git push origin feature/your-feature-name
```
<<<<<<< Updated upstream
 
### 5. PR作成
- 変更内容を記載して pull request を作成する
- レビューを依頼する
=======

2. 表示されるURLをブラウザで開きます

```
http://127.0.0.1:5000
```

---

## ■ 役割分担

本プロジェクトでは、各メンバーがそれぞれの強みを活かして以下の担当を行いました。

### 佐々木 優人（プロジェクト統括・バックエンド）
- 全体進捗の管理（WBS作成・タスク統括）
- 並び替え機能の実装（一覧のソート機能）
- アラート機能の実装・調整（右下通知含む）
- README作成・ドキュメント整備

---

### 穴井 伶弥（バックエンド・データ設計）
- 詳細画面（detail.html）の設計・実装
- アラート条件ロジックの設計・改善
- データベース設計補助（ER図含む）
- 外部リンク（URL機能）実装

---

### 萩原　美桜（フロントエンド・UI設計）
- 一覧画面（index.html）のUI設計・改善
- 検索UI・表示項目の最適化
- フェーズ表示仕様の設計
- CSS設計・スタイリング（ホバー・分割含む）
- 編集画面のUI改善

---

### 林 航世（フォームUI・UX改善・資料作成）
- 新規登録・編集画面（new/edit）のUI実装
- フォームUIの操作性改善（アコーディオンなど）
- README・発表資料の作成
- ER図作成

---

## ■ チーム共通で実施した内容
- アーキテクチャ設計
- テスト・不具合修正
- 発表資料作成
``
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
>>>>>>> Stashed changes
