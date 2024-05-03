<p align="center">
<img src="https://media.githubusercontent.com/media/Sunwood-ai-labs/TaskSphere/main/docs/TaskSphAIre_icon.jpeg" width="100%">
<br>
<h1 align="center">TaskSphAIre</h1>
<h2 align="center">
  ～Your Tasks, In Sync, In Sphere～

[![TaskSphere - Sunwood-ai-labs](https://img.shields.io/static/v1?label=TaskSphere&message=Sunwood-ai-labs&color=blue&logo=github)](https://github.com/Sunwood-ai-labs/TaskSphere "Go to GitHub repo")
[![stars - Sunwood-ai-labs](https://img.shields.io/github/stars/Sunwood-ai-labs/TaskSphere?style=social)](https://github.com/Sunwood-ai-labs/TaskSphere)
[![forks - Sunwood-ai-labs](https://img.shields.io/github/forks/Sunwood-ai-labs/TaskSphere?style=social)](https://github.com/Sunwood-ai-labs/TaskSphere)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/Sunwood-ai-labs/TaskSphere)](https://github.com/Sunwood-ai-labs/TaskSphere)
[![GitHub Top Language](https://img.shields.io/github/languages/top/Sunwood-ai-labs/TaskSphere)](https://github.com/Sunwood-ai-labs/TaskSphere)
[![GitHub Release](https://img.shields.io/github/v/release/Sunwood-ai-labs/TaskSphere?sort=date&color=red)](https://github.com/Sunwood-ai-labs/TaskSphere)
[![GitHub Tag](https://img.shields.io/github/v/tag/Sunwood-ai-labs/TaskSphere?color=orange)](https://github.com/Sunwood-ai-labs/TaskSphere)


  <br>

</h2>

</p>

>[!IMPORTANT]
>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

## 目次

- [目次](#目次)
- [概要](#概要)
- [特徴](#特徴)
- [インストール方法](#インストール方法)
  - [前提条件](#前提条件)
  - [手順](#手順)
- [使い方](#使い方)
- [サンプルコード](#サンプルコード)
- [ライセンス](#ライセンス)
- [お問い合わせ](#お問い合わせ)



## 概要

TaskSphAIreは、GitHub ProjectsからタスクをAIモデルで分解し、Googleカレンダーにスケジュールを自動的に同期するアプリケーションです。プロジェクト管理とタスクのスケジューリングを効率化し、生産性の向上を目指します。

## 特徴

- GitHub ProjectsからタスクをAIモデルで分解
- 分解したタスクをGoogleカレンダーにスケジュールとして自動同期
- 直感的なカレンダービューでプロジェクトのタイムラインを可視化
- Docker環境でアプリケーションを実行可能


## インストール方法

### 前提条件

- Docker、docker-composeがインストール済みであること
- GitHubアカウントとパーソナルアクセストークンを持っていること
- Googleアカウントとサービスアカウントの認証情報を持っていること

### 手順

1. TaskSphereリポジトリをクローンします：
   ```
   git clone https://github.com/Sunwood-ai-labs/TaskSphere.git
   ```

2. プロジェクトのディレクトリに移動します：
   ```
   cd TaskSphere
   ```

3. 環境変数ファイル `.env` を作成し、以下の変数を設定します：
   ```
   GITHUB_PERSONAL_ACCESS_TOKEN=<GitHubのパーソナルアクセストークン>
   GITHUB_USER_LOGIN=<GitHubのユーザー名>
   GITHUB_PROJECT_NUMBER=<同期するGitHubプロジェクトの番号>
   GOOGLE_APPLICATION_CREDENTIALS=key.json
   CALENDAR_ID=<同期するGoogleカレンダーのID>
   ```

4. Googleサービスアカウントの認証情報ファイル `key.json` をプロジェクトのルートディレクトリに配置します。

5. Dockerイメージをビルドし、コンテナを起動します：
   ```
   docker-compose up -d
   ```

6. アプリケーションのコンテナに入ります：
   ```
   docker-compose exec app bash
   ```

これで、TaskSphAIreの環境が整いました。

## 使い方

1. コンテナ内で以下のコマンドを実行し、TaskSphAIreを起動します：
   ```
   python modules/TaskSphAIre.py
   ```

   これにより、GitHub ProjectsからタスクをAIモデルで分解し、Googleカレンダーにスケジュールが自動的に同期されます。

2. 同期が完了したら、Googleカレンダーを開いて、スケジュールされたタスクを確認します。

## サンプルコード

`example`ディレクトリには、TaskSphAIreの機能を示すサンプルコードが含まれています：

- `01_github_project_info.py`：GitHubプロジェクトの情報を取得するサンプルコード。環境変数からアクセストークン、ユーザーログイン、プロジェクト番号を取得し、GraphQLクエリを使用してプロジェクトのタイトルとIDを取得します。

- `02_get_github_project_field_ids.py`：GitHubプロジェクトのフィールドIDを取得するサンプルコード。プロジェクト情報とフィールド情報を取得するためのGraphQLクエリを使用し、フィールドの名前、ID、オプション、反復情報を表示します。

- `03_github_project_items.py`：GitHubプロジェクトのアイテムを取得するサンプルコード。プロジェクト情報とアイテム情報を取得するためのGraphQLクエリを使用し、アイテムのID、フィールド値、コンテンツ情報（タイトル、本文、担当者）を表示します。

- `04_github_project_manager.py`：GitHubプロジェクトを管理するサンプルコード。プロジェクト情報とアイテム情報を取得し、アイテムをプロジェクトに追加する機能（既存の課題やプルリクエストの追加、新しいドラフト課題の追加）を提供します。

- `05_github_project_tool.py`：GitHubプロジェクトを操作するサンプルコード。プロジェクト情報、アイテム情報、フィールド情報を取得し、アイテムのフィールド値を更新する機能を提供します。

- `06_calendar_event_scheduler.py`：Googleカレンダーにイベントをスケジュールするサンプルコード。サービスアカウントの認証情報を使用してGoogleカレンダーAPIに接続し、イベントを作成して詳細を表示します。

- `07_fancy_litellm.py`：LLMを使用してレスポンスを生成するサンプルコード。異なるモデル（groq/llama3-70b-8192, groq/gemma-7b-it, anthropic/claude-3-haiku-20240307）を使用してプロンプトに対するレスポンスを生成し、結果を表示します。

これらのサンプルコードを参考にして、TaskSphAIreの機能を理解し、カスタマイズすることができます。

## ライセンス

TaskSphAIreは[MITライセンス](https://github.com/Sunwood-ai-labs/TaskSphere/blob/main/LICENSE)の下でリリースされています。

## お問い合わせ

ご質問、ご提案、フィードバックがある場合は、お気軽に[contact@sunwood-ai-labs.com](mailto:contact@sunwood-ai-labs.com)までお問い合わせください。

TaskSphAIreを使用して、プロジェクト管理をより効率的で生産的なものにしましょう！