# 📘 学習支援アプリ「知的な伴走者」統合要件定義書 ver.2.0

## 🎯 概要

本アプリは、学習者の**感情と行動の両面**をサポートする次世代学習支援システムです。従来の時間管理に加えて、学習時の感情状態を記録・分析し、個別最適化されたリカバリー機能と教師-生徒間のコミュニケーション強化により、**持続可能な学習習慣の確立**を目指します。

### 🌟 コアコンセプト
- **感情ドリブン学習**: 学習前後の感情変化を記録し、最適な学習スタイルを発見
- **予防的リカバリー**: 挫折パターンを検出し、事前に適切な介入を提供
- **ストーリー化された成長**: 学習進捗を物語として可視化し、継続意欲を維持
- **教師の指導最適化**: データに基づいた効果的な声かけとコミュニケーション

## 👥 想定ユーザー

| 区分 | 詳細 | 利用シーン |
|------|------|------------|
| **学習者** | 中高生～大学生、自主学習・家庭教師の支援を受ける層 | 日常の学習記録、感情管理、目標達成 |
| **教師／講師** | 家庭教師、塾講師、学習コーチ | 生徒の学習状況把握、適切な指導タイミング |
| **保護者** | 生徒の学習サポートを行う親 | 学習進捗の確認、家庭での声かけ |

## 🔄 統合使用フロー

### 日常使用フロー（感情連動型）
```
感情チェック → 今日の作戦 → チケット選択 → ストップウォッチ + 感情記録
     ↓             ↓              ↓                    ↓
作戦名提案 → チケット管理 → 集中度記録 → 感情変化分析
     ↓             ↓              ↓                    ↓
リカバリー → 教師への通知 → ジャーナル → 週次ふりかえり
```

### 予防的介入フロー
```
パターン検出 → 自動アラート → リカバリープラン → 実行支援
     ↓             ↓              ↓              ↓
継続監視 → 効果測定 → プラン調整 → 成功体験化
```

## 🧩 統合機能一覧

### 1. 感情ドリブン学習記録システム

#### 感情タグシステム
| 機能 | 説明 | 実装詳細 |
|------|------|----------|
| **学習前感情ログ** | 😫😐😄💪😴の5段階で開始前の気分を記録 | チケット開始時の必須入力 |
| **学習後感情ログ** | 🎉😌😓🤔💯の5段階で終了後の達成感を記録 | ストップウォッチ終了時の必須入力 |
| **感情パターン分析** | 感情×集中度×達成率の相関分析 | 週次レポートで可視化 |
| **気分連動作戦名** | 現在の気分から最適な作戦名を提案 | 機械学習による個別化 |

#### 感情データモデル
```python
class EmotionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    emotion_before = models.CharField(max_length=10)  # 😫😐😄💪😴
    emotion_after = models.CharField(max_length=10)   # 🎉😌😓🤔💯
    environment_factors = models.JSONField(default=dict)  # 場所、BGM、天気等
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 2. 適応型リカバリーシステム

#### 自動介入システム
| 条件 | 介入タイミング | 提案内容 | 実装方法 |
|------|----------------|----------|----------|
| **7日間未更新チケット** | 8日目の朝9時 | チケット細分化提案 | Celeryタスク |
| **目標進捗率30%以下** | 目標期限の50%時点 | 目標再設定ガイド | 進捗率監視 |
| **集中度3日連続低下** | 翌日の学習開始前 | 環境変更・休憩提案 | パターン検出 |
| **作戦名の偏り** | 週次ふりかえり時 | 新しい作戦名提案 | 多様性分析 |
| **感情パターンの悪化** | 連続3日間ネガティブ | 学習方法変更提案 | 感情トレンド分析 |

#### リカバリーシステムモデル
```python
class RecoveryPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trigger_condition = models.CharField(max_length=100)  # "7day_inactive"
    plan_type = models.CharField(max_length=50)  # "ticket_breakdown"
    suggestions = models.JSONField()  # 提案内容
    is_accepted = models.BooleanField(default=False)
    effectiveness_score = models.FloatField(null=True)  # 効果測定
    created_at = models.DateTimeField(auto_now_add=True)
```

### 3. ストーリー化された進捗システム

#### 学習ジャーニー可視化
| 機能 | 説明 | UI例 |
|------|------|------|
| **現在の章立て** | 学習フェーズを物語風に表現 | "第3章: 基礎固めの試練" |
| **キャラクター診断** | 学習パターンから性格タイプを分析 | "あなたは集中スナイパー型！" |
| **達成バッジ** | マイルストーン達成で獲得 | "7日連続達成マスター" |
| **成長曲線** | 感情×時間×達成率の3D可視化 | インタラクティブなグラフ |

#### ストーリーシステムモデル
```python
class UserCharacterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    character_type = models.CharField(max_length=50)  # "コツコツ型"
    current_chapter = models.CharField(max_length=100)  # "基礎固め編"
    experience_points = models.IntegerField(default=0)
    badges = models.JSONField(default=list)
    personality_traits = models.JSONField(default=dict)  # 学習特性
    last_updated = models.DateTimeField(auto_now=True)
```

### 4. 教師-生徒間コミュニケーション強化

#### インタラクションシステム
| 機能 | 説明 | 実装方法 |
|------|------|----------|
| **ワンクリック声かけ** | 定型文での素早い励まし | テンプレート選択UI |
| **学習ハイライト共有** | 週次の成果を教師と共有 | 自動レポート生成 |
| **進捗アラート** | 生徒の学習状況変化を通知 | WebSocket通知 |
| **セッション記録** | 面談内容をデジタル化 | 音声→テキスト変換 |
| **感情状態共有** | 生徒の感情変化を教師に通知 | プライバシー配慮型 |

#### コミュニケーションモデル
```python
class TeacherStudentInteraction(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_interactions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_interactions')
    interaction_type = models.CharField(max_length=50)  # "encouragement", "feedback"
    content = models.TextField()
    student_response = models.TextField(blank=True)
    emotional_context = models.JSONField(default=dict)  # 感情的背景
    created_at = models.DateTimeField(auto_now_add=True)
```

### 5. 高度な学習分析機能

#### パターン分析システム
| 分析軸 | 内容 | 活用方法 |
|--------|------|----------|
| **時間帯別集中度** | 1時間単位の集中度分析 | 最適時間帯提案 |
| **教科別感情変化** | 科目ごとの感情パターン | 苦手科目の取り組み方改善 |
| **環境要因分析** | 場所・BGM・天気の影響 | 個人最適環境の発見 |
| **作戦名効果測定** | 作戦名による達成率変化 | 効果的な作戦名推薦 |
| **感情-成果相関** | 感情状態と学習成果の関係 | 最適学習状態の発見 |

#### 週次ふりかえりシステム
```python
class WeeklyReflection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateField()
    best_strategy_name = models.CharField(max_length=100)
    top_concentration_times = models.JSONField()  # ["09:00-10:00", "14:00-15:00"]
    emotional_highlights = models.JSONField()  # [{"day": "月", "emotion": "😄", "reason": "数学が解けた"}]
    emotional_lowlights = models.JSONField()  # 感情的な課題
    next_week_goals = models.TextField()
    satisfaction_score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    improvement_areas = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 6. 拡張されたチケット管理システム

#### 基本機能
| 機能 | 説明 | 新規追加点 |
|------|------|-----------|
| **感情連動チケット** | 現在の感情状態に最適なチケットを提案 | 感情タグとの連携 |
| **作成者／対象者分離** | 教師が生徒にチケットを割り当て | 承認ワークフロー |
| **動的進捗表示** | 感情変化も含めた進捗可視化 | 感情グラフ統合 |
| **テンプレート保存** | 感情パターン付きテンプレート | 成功パターンの再利用 |

#### 強化されたチケットモデル
```python
class Ticket(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    estimated_time = models.IntegerField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tickets')
    difficulty_level = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    optimal_emotions = models.JSONField(default=list)  # 最適な感情状態
    success_patterns = models.JSONField(default=dict)  # 成功パターン
    created_at = models.DateTimeField(auto_now_add=True)
```

### 7. ゲーミフィケーション要素

#### 多様なストリーク機能
| ストリーク種別 | 条件 | 報酬 | 実装 |
|----------------|------|------|------|
| **連続ログイン** | 7日連続アクセス | "継続力バッジ" | 日次チェック |
| **連続集中** | 集中度4以上を5日連続 | "集中マスター" | 集中度監視 |
| **連続達成** | チケット完了を10日連続 | "達成王バッジ" | 完了数監視 |
| **連続日記** | ジャーナル記入を14日連続 | "内省の達人" | 日記投稿監視 |
| **感情改善** | 週次で感情スコア向上 | "成長マスター" | 感情トレンド分析 |

#### 動的な称号システム
```python
class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # emoji or icon name
    condition_type = models.CharField(max_length=50)  # "streak", "total", "pattern"
    condition_value = models.JSONField()  # {"type": "consecutive_days", "count": 7}
    rarity = models.CharField(max_length=20)  # "common", "rare", "legendary"
    emotional_requirements = models.JSONField(default=dict)  # 感情条件

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField(default=True)
    emotional_context = models.JSONField(default=dict)  # 獲得時の感情状態
```

### 8. 拡張されたジャーナル機能

#### 感情重視のジャーナル
| 機能 | 説明 | 実装方法 |
|------|------|----------|
| **感情分析付き日記** | 感情変化を含むジャーナル | 自然言語処理 |
| **質問ガイド** | 感情に応じた質問を自動生成 | 感情状態連動 |
| **成長ストーリー** | 感情変化を物語として記録 | テンプレート化 |
| **教師との共有** | 感情状態を含む学習記録共有 | プライバシー制御 |

#### 統合ジャーナルモデル
```python
class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    strategy_name = models.CharField(max_length=100)
    achievement_level = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    insights = models.TextField()
    completed_tickets = models.ManyToManyField(Ticket)
    emotional_journey = models.JSONField(default=list)  # 感情の変化記録
    environmental_notes = models.TextField(blank=True)
    tomorrow_preparation = models.TextField(blank=True)
    ai_suggestions = models.JSONField(default=dict)  # AI提案
    created_at = models.DateTimeField(auto_now_add=True)
```

## 💻 技術スタック（統合版）

### バックエンド強化
| 技術 | 用途 | バージョン | 新規追加理由 |
|------|------|-----------|-------------|
| Django | Webフレームワーク | 5.1.4 | 基盤システム |
| Django-Ninja | REST API開発 | 1.3.0 | 高速API開発 |
| Celery | 非同期タスク処理 | 5.4.0 | リカバリープラン生成 |
| Redis | キャッシュ・リアルタイム | 5.2.0 | 感情データ高速処理 |
| PostgreSQL | メインデータベース | 14.0+ | 複雑なクエリ最適化 |
| Scikit-learn | 機械学習 | 1.3.0 | 感情パターン分析 |

### フロントエンド強化
| 技術 | 用途 | バージョン | 新規追加理由 |
|------|------|-----------|-------------|
| Next.js | フロントエンドフレームワーク | 14.2.15 | SSR/SSG最適化 |
| React | UIライブラリ | 18.3.1 | コンポーネント基盤 |
| TypeScript | 型安全性 | 5.6.3 | 品質保証 |
| SWR | データフェッチング | 2.2.5 | リアルタイム更新 |
| TailwindCSS | スタイリング | 3.4.14 | 高速UI開発 |
| Framer Motion | アニメーション | 11.11.17 | 感情表現強化 |
| Recharts | グラフ・チャート | 2.12.7 | 感情データ可視化 |
| Three.js | 3D可視化 | r128 | 3D感情マップ |

### 新規技術スタック
| 技術 | 用途 | 説明 |
|------|------|------|
| **Socket.IO** | リアルタイム通信 | 教師-生徒間の即時通知 |
| **Chart.js** | 複雑なグラフ | 感情変化の詳細可視化 |
| **Tone.js** | 音声処理 | 学習環境音の分析 |
| **TensorFlow.js** | クライアント側ML | 感情予測モデル |

## 🎨 統合UI/UX設計

### 感情に響くビジュアルデザイン
- **アダプティブカラー**: 感情状態に応じた動的カラーパレット
- **マイクロアニメーション**: 感情タグ選択時の直感的フィードバック
- **ストーリーボード**: 学習進捗の漫画風可視化
- **アバターシステム**: 感情状態を反映するキャラクター

### 感情連動インターフェース
```javascript
// 感情タグ選択時のアニメーション
const emotionTagAnimation = {
  hover: 'scale(1.2) rotate(5deg)',
  selected: 'bounce 0.5s ease-in-out',
  feedback: 'pulse 1s infinite',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
}

// 感情状態に応じたテーマカラー
const emotionColorMap = {
  '😫': { primary: '#ff6b6b', secondary: '#ffeaa7' },
  '😐': { primary: '#74b9ff', secondary: '#81ecec' },
  '😄': { primary: '#00b894', secondary: '#55efc4' },
  '💪': { primary: '#e17055', secondary: '#fdcb6e' },
  '😴': { primary: '#a29bfe', secondary: '#fd79a8' }
}
```

## 📊 成功指標の設定

### 定量的指標
| 指標 | 目標値 | 測定方法 | 重要度 |
|------|--------|----------|--------|
| **継続率** | 30日後の利用継続率 > 70% | ログイン履歴分析 | 最重要 |
| **感情改善率** | 学習前後の感情スコア向上率 > 40% | 感情ログ分析 | 最重要 |
| **学習時間** | 1日平均学習時間 > 2時間 | ストップウォッチデータ | 重要 |
| **達成率** | チケット完了率 > 80% | チケット状態分析 | 重要 |
| **教師満足度** | 指導効率改善実感 > 80% | アンケート調査 | 重要 |

### 定性的指標
- **学習への取り組み姿勢の変化**: 主体的な学習行動の増加
- **自己効力感の向上**: 「自分にもできる」という感覚の強化
- **感情調整能力の向上**: ネガティブな感情を建設的に活用
- **教師との関係性改善**: より深いコミュニケーション
- **学習習慣の定着**: 外発的動機から内発的動機への転換

## 🔧 実装アーキテクチャ

### 感情分析パイプライン
```python
class EmotionAnalysisPipeline:
    def __init__(self):
        self.emotion_classifier = self.load_emotion_model()
        self.pattern_analyzer = PatternAnalyzer()
        
    def analyze_emotional_journey(self, user_id, timeframe='week'):
        """感情変化の分析"""
        emotions = EmotionLog.objects.filter(user_id=user_id, 
                                           created_at__gte=timeframe)
        return self.pattern_analyzer.detect_patterns(emotions)
    
    def predict_optimal_study_time(self, user_id):
        """最適学習時間の予測"""
        historical_data = self.get_user_learning_patterns(user_id)
        return self.emotion_classifier.predict_best_time(historical_data)
    
    def generate_recovery_plan(self, user_id, trigger_condition):
        """個別化されたリカバリープラン生成"""
        user_profile = self.get_user_profile(user_id)
        emotion_patterns = self.analyze_emotional_journey(user_id)
        return self.create_personalized_plan(user_profile, emotion_patterns)
```

### リアルタイム通知システム
```javascript
// WebSocket接続による即座通知
const notificationTypes = {
  EMOTION_ALERT: 'emotion_state_change',
  ENCOURAGEMENT: 'teacher_encouragement',
  ACHIEVEMENT: 'badge_earned',
  RECOVERY: 'recovery_plan_suggested',
  PATTERN_DETECTED: 'learning_pattern_identified'
}

class EmotionNotificationManager {
  constructor() {
    this.socket = io('/emotion-updates');
    this.setupEventListeners();
  }
  
  setupEventListeners() {
    this.socket.on('emotion_state_change', this.handleEmotionChange);
    this.socket.on('recovery_plan_suggested', this.showRecoveryPlan);
  }
  
  handleEmotionChange(data) {
    this.updateUITheme(data.emotion);
    this.suggestOptimalActions(data);
  }
}
```

## 🚀 段階的実装計画

### Phase 1: 感情連動MVP (8週間)
1. **基本感情タグシステム**
   - 学習前後の感情記録
   - 感情データの基本可視化
   - 感情連動作戦名提案

2. **基本リカバリー機能**
   - 7日間未更新チケット検出
   - 簡単な介入メッセージ
   - 基本的なチケット細分化提案

3. **教師向け基本機能**
   - 生徒の感情状態ダッシュボード
   - ワンクリック声かけテンプレート
   - 基本的な進捗レポート

### Phase 2: 高度な分析機能 (10週間)
1. **感情パターン分析**
   - 時間帯×感情×集中度の相関分析
   - 教科別感情変化パターン
   - 個人最適化された学習時間提案

2. **ストーリー化機能**
   - 学習ジャーニーの可視化
   - キャラクター診断システム
   - 達成バッジとストリーク機能

3. **高度なリカバリー**
   - 機械学習による挫折予測
   - 個別化されたリカバリープラン
   - 効果測定とプラン最適化

### Phase 3: AI・ソーシャル機能 (12週間)
1. **機械学習統合**
   - 感情予測モデル
   - 自然言語処理によるジャーナル分析
   - 個別最適化された学習戦略提案

2. **ソーシャル機能**
   - 匿名での学習進捗共有
   - ピアラーニング支援
   - 学習コミュニティ形成

3. **高度な可視化**
   - 3D感情マップ
   - AR/VR学習環境
   - 音声・画像認識機能

## 🎪 ブランディング戦略

### 統合キャッチコピー
- **メイン**: "感情も、時間も、成長も。すべてがつながる学習体験"
- **サブ**: "今日の気持ちから、明日の可能性へ"
- **機能訴求**: "あなたの感情が、最高の学習戦略を教えてくれる"

### ユーザーストーリー（統合版）
```
高校2年生のAさん:
「数学が大嫌いで😫マークばかりつけてたけど、
アプリが『今日は軽めの計算問題から始めよう』って提案してくれて、
最後に🎉マークになった時の達成感が忘れられない！
今では『数学征服大作戦』が一番楽しい時間になってる。」

家庭教師のBさん:
「生徒の感情変化がリアルタイムで分かるから、
『今日は調子悪そうだから、好きな図形問題から始めよう』とか、
最適なタイミングで声をかけられるように。
生徒との関係も深くなったし、指導の質も上がった。」

保護者のCさん:
「子供の学習状況が感情も含めて見えるから、
『今日は頑張ったね』って具体的に声をかけられる。
親子のコミュニケーションも良くなった。」
```

## 🔮 将来のビジョン

### 3年後の姿
- **感情AI**: 高度な感情認識・予測システム
- **学習生態系**: 教師・生徒・保護者・AIが連携した学習環境
- **社会的インパクト**: 学習格差の解消と教育の質向上
- **グローバル展開**: 多言語・多文化対応システム

### 5年後の姿
- **感情教育**: 感情管理スキルの教育プラットフォーム
- **個別最適化**: 完全個別化された学習カリキュラム
- **社会実装**: 学校教育への正式導入
- **研究貢献**: 感情と学習の関係に関する学術的発見

---

## 📝 更新履歴

### ver.2.0 (2025/07/06)
- **感情ドリブン学習**: 感情タグシステムの完全統合
- **予防的リカバリー**: 自動介入システムの実装
- **ストーリー化**: 学習ジャーニーの可視化機能
- **教師支援強化**: 感情状態を含む指導支援システム
- **高度な分析**: 感情パターン分析機能の追加
- **ゲーミフィケーション**: 感情連動型バッジシステム
- **技術スタック強化**: 機械学習・リアルタイム通信の統合

### ver.1.1 (2025/07/06)
- **技術スタック更新**: Next.js 14を採用、React 18対応
- **ライブラリ更新**: 全体的なバージョンアップ（Django 5.1、最新UI库）
- **認証システム**: NextAuth.js導入によるセキュア認証
- **パフォーマンス強化**: SSR/SSG対応、リアルタイム更新最適化
- **UX改善**: Framer Motion、Confetti効果の追加
- **開発効率向上**: TypeScript完全対応、型安全性の確保
- **PWA対応準備**: 将来的なオフライン機能の基盤整備

### ver.1.0 (2025/06/30)
- 初版リリース