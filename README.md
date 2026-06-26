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
 
### 5. PR作成
- 変更内容を記載して pull request を作成する
- レビューを依頼する

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

