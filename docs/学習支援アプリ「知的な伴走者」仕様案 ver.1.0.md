# 📘 学習支援アプリ「知的な伴走者」仕様書 ver.1.0

## 🎯 概要

本アプリは、学習者が日々の勉強を意味ある行動として進めるために、目標・計画・実行・ふりかえりのサイクルを視覚化・習慣化する**知的な学習支援アプリ**です。  
家庭教師の生徒のようにモチベーションが続かない学習者に対し、「今日の作戦」を立てる仕組みと、達成記録、振り返り、可視化された実績を提供します。

## 👥 想定ユーザー

| 区分 | 内容 |
|------|------|
| 学習者 | 主に中高生～大学生、自主学習や家庭教師の支援を受ける層 |
| 教師／講師 | 生徒にチケット（課題）を提案・共有する立場 |

## 🔄 想定使用フロー

### 初期設定フロー
1. **アカウント作成**
2. **目標設定**: 長期・中期・短期の目標を設定（全てを設定する必要はない）
3. **好み・得意分野の設定**: 現時点での好きなこと、得意なこと、嫌いなこと、苦手なことを設定
4. **アドバイス機能**: 2-3の情報から具体的なアドバイスを提供
5. **チケット作成**: 目標に向けてチケットを思いつくままに作成

### 日常使用フロー
```
チケット管理 → ストップウォッチ → ジャーナル → 今日の作戦
     ↑                                            ↓
     ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

## 🧩 機能一覧

### 1. 初期設定・プロフィール機能

| 機能 | 説明 |
|------|------|
| 目標設定 | 長期・中期・短期の学習目標を設定（任意項目） |
| 好み・特性設定 | 好きなこと・得意なこと・嫌いなこと・苦手なことを具体的に登録 |
| アドバイス機能 | 設定した情報から個別化された学習アドバイスを提供 |

### 2. チケット管理

| 機能 | 説明 |
|------|------|
| チケット作成 | 学習タスクを登録（タイトル・内容・目安時間・期限・目標連携） |
| 作成者／対象者分離 | 教師が生徒にチケットを割り当てられるようにする |
| ステータス管理 | 未着手／進行中／完了／保留の状態に分類可能 |
| 進捗表示 | 「3/4」形式での視覚的進捗表示 |
| テンプレート保存 | 汎用的な課題をテンプレートとして登録、再利用可能 |
| ワンオフ作成 | 一回限りの課題をテンプレなしで登録可 |
| チケット作成支援 | 目標連動型提案、苦手克服チケット、得意活用チケット |

### 3. 学習スケジュール管理

| 機能 | 説明 |
|------|------|
| 今日の作戦（朝） | 作戦名を設定し、やるべきチケットを「貼る」形式で予定に追加 |
| 作戦名ジェネレーター | 教科・気分・曜日別でユニークな作戦名を提案 |
| スケジュール帳表示 | チケットを日付ごとに整理、予定表示（カレンダーまたは時間割風） |
| 放置チケット表示 | 一定期間（例：7日）更新されていないチケットを通知・警告 |

### 4. 実行・記録

| 機能 | 説明 |
|------|------|
| ストップウォッチ | 学習開始時にチケットを選び、実行時間を計測・記録 |
| 集中度記録 | 1-5段階での集中度自己申告機能 |
| 時間ログ管理 | 学習時間ログを蓄積、後日参照やグラフ表示に活用 |
| 学習環境ログ | 場所・BGMの有無などの環境要素記録（オプション） |

### 5. ジャーナルとふりかえり

| 機能 | 説明 |
|------|------|
| 学習日報（夜） | 作戦名、達成度、気づきなどを記録する日報入力欄 |
| ハイブリッド形式 | ガイド付きプレースホルダーとランダム質問機能 |
| 翌日の作戦準備 | 翌日の予定チケットをあらかじめ選択・計画 |

### 6. 可視化・分析

| 機能 | 説明 |
|------|------|
| 目標進捗の可視化 | ゴールごとの進捗バーとチケット完了率表示 |
| 集中度ヒートマップ | 時間帯別・日別の集中度を色分け表示 |
| 学習時間グラフ | recharts を使用した時間推移グラフ |
| 達成感の演出 | チケット完了時のマイクロアニメーション、連続学習日数表示 |

## 🗂️ データモデル設計

### 主要モデル

| モデル | 概要 | 主要フィールド |
|--------|------|----------------|
| `User` | Django標準の認証ユーザー | username, email, password |
| `Goal` | 長期・中期・短期の学習目標 | title, description, term_type, target_date, user |
| `UserPreference` | ユーザーの好み・特性 | user, category, subject, detail |
| `Ticket` | 個別の学習課題 | title, content, estimated_time, deadline, status, goal, creator, assignee |
| `TicketTemplate` | 再利用用の課題テンプレート | title, content, estimated_time, creator |
| `StopwatchLog` | チケットごとの学習時間ログ | ticket, user, start_time, end_time, concentration_level, environment_notes |
| `JournalEntry` | 日報・作戦記録 | user, date, strategy_name, achievement_level, insights, completed_tickets |
| `StrategyName` | 作戦名の履歴・お気に入り | user, name, category, is_favorite |

### モデル関連性
- `Goal` ↔ `Ticket`: 1対多（1つの目標に複数のチケット）
- `User` ↔ `UserPreference`: 1対多
- `Ticket` ↔ `StopwatchLog`: 1対多
- `User` ↔ `JournalEntry`: 1対多（日付でユニーク）

## 💻 技術スタック

### バックエンド
| 技術 | 用途 |
|------|------|
| Django | Webフレームワーク |
| Django-Ninja or DRF | REST API開発 |
| MySQL | データベース |

### フロントエンド
| 技術 | 用途 |
|------|------|
| Next.js or React | フロントエンドフレームワーク |
| TypeScript | 型安全性の確保 |

### UI/UX
| 技術 | 用途 |
|------|------|
| TailwindCSS | スタイリング |
| shadcn/ui | UIコンポーネントライブラリ |
| lucide-icons | アイコン |
| recharts | グラフ・チャート表示 |

### インフラ
| 技術 | 用途 |
|------|------|
| Docker | ローカル・開発環境 |
| Vercel（将来的） | フロントエンドデプロイ |

## 🎨 UX強化機能

### 1. 🎯 目標とチケットの接続可視化
- チケット詳細に「この課題は〇〇目標に関連」のタグ表示
- `Goal` ごとの進捗バー（チケット完了率）を表示
- 「今、自分はどこに向かっているか」が一目で分かる"旅の地図"感の提供

### 2. 🔥 集中度ログの表示
- ユーザー自身が「自己申告集中度（1〜5段階）」を日／週ごとに入力
- カレンダーやグラフで色分け表示し、「集中の蓄積」が見える化
- 試験前の週は"集中エネルギー貯金週間"として視覚的に強調

### 3. 🧠 ジャーナルのハイブリッド形式
- 入力欄にガイド的なプレースホルダー：
  - 「例）今日一番頑張ったことは？」
  - 「困ったことは？」
- ランダム質問機能（例：「今日の天気に例えると？」☀️🌧️）
- 日記習慣を楽しみながら継続できる仕組みづくり

### 4. 🕐 ヒートマップ＋学習環境ログ
- ストップウォッチログ＋集中度から、時間帯別ヒートマップを生成
- 「どの時間帯に集中できているか」がひと目でわかる
- オプションで「場所」「BGMの有無」などのメモ欄、最適学習環境の発見に活用

### 5. 🎭 作戦名ジェネレーター
- 教科／気分／曜日別でユニークな作戦名を提案
- 例：
  - テンション低 →「低空飛行だけど着地は決める」
  - 数学 →「関数王への道」
- ランダムボタン＆お気に入り登録機能付き
- 作戦名から日々の学習を"物語化"する習慣づけ

### 6. 🧑‍🏫 指導支援パネルの拡張
- 生徒の学習状況をCSV/PNGとして出力（面談用資料、保護者報告にも応用）
- 放置チケットや作戦名履歴などから「声かけヒント」を自動生成
- 例：「今日は気分転換に○○作戦でいってみよう！」など
- 教師の指導負担を軽減しつつ、生徒との関係性を深める

### 7. 🌟 達成感の演出
- チケット完了時のマイクロアニメーション
- 連続学習日数の表示（ストリーク機能）
- 月末の「今月のハイライト」自動生成

### 8. 🤝 ソーシャル要素（軽度）
- 同じ目標を持つ学習者との匿名での進捗共有
- 教師からの「いいね」やコメント機能

### 9. 🎵 学習環境の最適化支援
- 集中度とBGM/環境音の相関分析
- 最適な学習時間帯の提案機能

## 🚀 アドバイス機能の詳細

### 実装方針
- **ルールベース**: 好き×苦手の組み合わせパターンを事前定義
- **テンプレート化**: 汎用的なアドバイステンプレートを用意
- **将来的にML**: 学習データが蓄積されたら機械学習による個別最適化

### アドバイス例
```
設定例:
好き: 図形、パズル
得意: 暗記
嫌い: 計算、文章題
目標: 数学のテストで80点以上

↓ AIアドバイス例
「図形好きを活かして、二次関数をグラフでイメージ化してみよう」
「文章題は一旦図に描いてパズル感覚で解いてみる作戦はどう？」
```

### チケット作成支援
- **目標連動型提案**: 設定した目標から逆算したチケット候補を提示
- **苦手克服チケット**: 嫌い/苦手要素を小分けにした取り組みやすいタスク
- **得意活用チケット**: 得意分野を使って他分野を学ぶクロス学習

## 📅 開発スケジュール（案）

| 期間 | マイルストーン |
|------|----------------|
| ～7月上旬 | 要件確定、モデル・画面構成検討 |
| 7月中旬 | MVP構築（チケット管理＋ストップウォッチ＋ジャーナル） |
| 7月下旬 | スケジューリングUI、テンプレート登録、ダッシュボード統合 |
| 8月上旬 | アドバイス機能、可視化機能の実装 |
| 8月中旬 | UX強化機能、指導支援パネルの実装 |

## 🔜 今後の拡張案（スコープ外）

- PWA対応（オフライン学習記録、プッシュ通知）
- 機械学習によるおすすめ学習計画サジェスト
- より高度な通知機能（締切／放置警告／リマインダー）
- チーム学習機能の拡張
- 学習データの詳細分析・レポート機能

## 🗣️ 技術的考慮事項

### セキュリティ
- ユーザー認証・認可の実装
- 教師-生徒間のデータアクセス制御
- 個人学習データの保護

### パフォーマンス
- 大量の学習ログデータの効率的な処理
- リアルタイムストップウォッチ機能の実装
- グラフ描画の最適化

### 拡張性
- APIのバージョニング戦略
- モジュラー設計による機能追加の容易性
- 学習データのバックアップ・エクスポート機能

## 💡 MVP優先機能

1. **ユーザー認証・プロフィール設定**
2. **基本的なチケット管理**
3. **ストップウォッチ機能**
4. **シンプルなジャーナル機能**
5. **作戦名設定機能**

追加機能は段階的に実装し、ユーザーフィードバックを基に優先順位を調整する方針とする。