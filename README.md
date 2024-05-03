<p align="center">
<img src="" width="100%">
<br>
<h1 align="center">TaskSphere</h1>
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
  - [メイン機能の実行](#メイン機能の実行)
  - [サンプルコード](#サンプルコード)
- [コントリビューション](#コントリビューション)
- [ライセンス](#ライセンス)
- [お問い合わせ](#お問い合わせ)

## 概要

TaskSphereは、GitHub ProjectsとGoogleカレンダーをシームレスに統合する革新的なプロジェクト管理ツールです。効率的なタスク管理とスケジューリングのための中央集中型プラットフォームを提供することで、チームがタスクの計画、組織化、実行する方法を革新することを目指しています。

TaskSphereを使用すると、GitHub ProjectsをGoogleカレンダーと簡単に同期できるため、会議やイベントと並行してタスクを可視化および管理できます。プロジェクトのタイムラインを把握し、チームメンバーにタスクを割り当て、二度と締め切りを逃すことはありません！

## 特徴

- GitHub ProjectsとGoogleカレンダーのシームレスな同期
- プロジェクトのタイムラインと締め切りを可視化するための直感的なカレンダービュー
- コラボレーティブなタスクの割り当てと追跡
- 今後のタスクとイベントの自動リマインダーと通知
- 洞察に満ちたプロジェクト分析と進捗状況の追跡
- 安全な認証とデータ保護

## インストール方法

### 前提条件

- Python 3.6以降がインストールされていること
- GitHubアカウントとパーソナルアクセストークンを持っていること
- Googleアカウントとサービスアカウントの認証情報を持っていること

### 手順

1. TaskSphereリポジトリをクローンします：
   ```
   git clone https://github.com/Sunwood-ai-labs/TaskSphere.git
   ```

2. 必要な依存関係をインストールします：
   ```
   cd TaskSphere
   pip install -r requirements.txt
   ```

3. 必要な環境変数を設定します：
   - `GITHUB_PERSONAL_ACCESS_TOKEN`：GitHubのパーソナルアクセストークン
   - `GITHUB_USER_LOGIN`：GitHubのユーザー名
   - `GITHUB_PROJECT_NUMBER`：同期するGitHubプロジェクトの番号
   - `GOOGLE_APPLICATION_CREDENTIALS`：Googleサービスアカウントの認証情報ファイルへのパス
   - `CALENDAR_ID`：同期するGoogleカレンダーのID

## 使い方

### メイン機能の実行

TaskSphereの主要機能を実行するには、以下のコマンドを実行します：

```
python modules/GithubToGoogleCalendar.py
```

このコマンドを実行すると、GitHub ProjectsからタスクをフェッチしてGoogleカレンダーにイベントとして同期します。環境変数が適切に設定されていることを確認してください。

### サンプルコード

`example`ディレクトリには、TaskSphereの機能を示すサンプルコードが含まれています：

- `01_github_project_info.py`：GitHubプロジェクトの情報を取得する方法を示すサンプルコード
- `02_get_github_project_field_ids.py`：GitHubプロジェクトのフィールドIDを取得する方法を示すサンプルコード
- `03_github_project_items.py`：GitHubプロジェクトのアイテムを取得する方法を示すサンプルコード
- `04_github_project_manager.py`：GitHubプロジェクトを管理する方法を示すサンプルコード
- `05_github_project_tool.py`：GitHubプロジェクトを操作するツールを示すサンプルコード
- `06_calendar_event_scheduler.py`：Googleカレンダーにイベントをスケジュールする方法を示すサンプルコード

これらのサンプルを参考にして、TaskSphereの使い方を学ぶことができます。

## コントリビューション

コミュニティからのコントリビューションを歓迎します！TaskSphereに貢献したい場合は、以下の手順に従ってください：

1. リポジトリをフォークします
2. 新機能またはバグ修正用の新しいブランチを作成します
3. 変更を加え、説明的なメッセージでコミットします
4. 変更をフォークしたリポジトリにプッシュします
5. メインのTaskSphereリポジトリにプルリクエストを送信します

コードがプロジェクトのコーディング規則に準拠し、適切なテストが含まれていることを確認してください。

## ライセンス

TaskSphereは[MITライセンス](https://github.com/Sunwood-ai-labs/TaskSphere/blob/main/LICENSE)の下でリリースされています。

## お問い合わせ

ご質問、ご提案、フィードバックがある場合は、お気軽に[contact@sunwood-ai-labs.com](mailto:contact@sunwood-ai-labs.com)までお問い合わせください。

TaskSphereを使用して、プロジェクト管理をより効率的で生産的なものにしましょう！