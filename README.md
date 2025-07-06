# Simple Chat App で学ぶ DDD × Clean Architecture

**このドキュメントはAIによって生成されたものです。**

このアプリケーションは、**Domain-Driven Design (DDD)** と **Clean Architecture** の原則を組み合わせた実践的なチャットアプリケーションです。本資料では、実際のコードを参照しながら両方のアーキテクチャパターンの融合を解説します。

## 目次
- [DDDとClean Architectureとは](#ddとclean-architectureとは)
- [アーキテクチャ概要](#アーキテクチャ概要)
- [Clean Architectureの4層構造](#clean-architectureの4層構造)
- [ドメイン層（エンタープライズビジネスルール）](#ドメイン層エンタープライズビジネスルール)
- [ユースケース層（アプリケーションビジネスルール）](#ユースケース層アプリケーションビジネスルール)
- [インターフェースアダプター層](#インターフェースアダプター層)
- [フレームワーク・ドライバー層](#フレームワークドライバー層)
- [ポート・アダプターパターン](#ポートアダプターパターン)
- [依存性逆転の原則（DIP）](#依存性逆転の原則dip)
- [実際の動作フロー](#実際の動作フロー)
- [DDDとClean Architectureの融合メリット](#ddとclean-architectureの融合メリット)

## DDDとClean Architectureとは

### Domain-Driven Design (DDD)
複雑なソフトウェアの設計手法で、ビジネスドメインの知識をコードに直接反映させることを重視します。エンティティ、値オブジェクト、リポジトリなどのパターンを用いてビジネスロジックを表現します。

### Clean Architecture
Uncle Bobが提唱したアーキテクチャで、依存性逆転の原則により内側の層（ビジネスロジック）を外側の層（技術的詳細）から独立させることを目指します。

## アーキテクチャ概要

このアプリケーションは、DDDの戦術的パターンをClean Architectureの4層構造に配置した設計となっています：

```
┌─────────────────────────────────────────────┐
│    Frameworks & Drivers (最外層)            │
│  ┌─────────────────────────────────────────┐ │
│  │    Interface Adapters                   │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │    Use Cases                        │ │ │
│  │  │  ┌─────────────────────────────────┐ │ │ │
│  │  │  │    Enterprise Business Rules   │ │ │ │
│  │  │  │         (Domain)                │ │ │ │
│  │  │  └─────────────────────────────────┘ │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

各層のディレクトリ構造：
```
app/
├── domain/                 # Enterprise Business Rules (DDD ドメイン層)
│   ├── chat/
│   │   ├── entity/        # DDD エンティティ
│   │   ├── value_object/  # DDD 値オブジェクト
│   │   └── repository/    # DDD リポジトリ抽象
│   └── shared/
├── usecase/               # Use Cases (Clean Architecture ユースケース層)
│   ├── stream/           # ユースケース実装
│   └── ports/            # Clean Architecture ポート
│       ├── input/        # 入力ポート
│       └── output/       # 出力ポート
└── infrastructure/       # Frameworks & Drivers + Interface Adapters
    ├── fastapi/          # Webフレームワーク
    ├── memory/           # データ永続化
    └── openai/           # 外部API
```

## Clean Architectureの4層構造

### 1. Enterprise Business Rules（エンタープライズビジネスルール）
**→ DDDのドメイン層に対応**

最も内側の層で、ビジネスの核となるルールを含みます。フレームワークやデータベースの詳細に一切依存しません。

### 2. Use Cases（ユースケース/アプリケーションビジネスルール）
**→ DDDのアプリケーション層に対応**

アプリケーション固有のビジネスルールを含み、エンタープライズビジネスルールを協調させてユースケースを実現します。

### 3. Interface Adapters（インターフェースアダプター）
**→ DDDのアプリケーション層の一部**

データをユースケースやエンティティにとって便利な形式から、外部エージェンシー（データベース、Web等）にとって便利な形式に変換します。

### 4. Frameworks & Drivers（フレームワーク・ドライバー）
**→ DDDのインフラストラクチャ層に対応**

データベース、Webフレームワークなどの外部ツールの詳細を含みます。

## ドメイン層（エンタープライズビジネスルール）

Clean Architectureの最内層で、DDDのドメイン層に相当します。ビジネスの核となるルールを表現し、外部の技術的詳細に一切依存しません。

### エンティティ (Entity)

**Chat エンティティ** (`app/domain/chat/entity/chat.py`)
```python
class Chat:
    def __init__(self, id: Id, title: Title, steps: list[Step], created_at: Time, updated_at: Time):
        self._id = id
        self._title = title
        self._steps = steps
        self._created_at = created_at
        self._updated_at = updated_at

    def add_step(self, step: Step):
        """エンタープライズビジネスルール: チャットにステップを追加"""
        self._steps.append(step)

    def get_chat_history(self) -> str:
        """エンタープライズビジネスルール: チャット履歴の生成"""
        return "\n".join([f"{index + 1}: {step.get_question().value()} -> {step.get_answer().value()}" 
                         for index, step in enumerate(self._steps)])
```

**Clean Architecture観点:**
- 最内層のエンタープライズビジネスルール
- 外部依存なし（import文を見ると、全てドメイン内の値オブジェクト）
- ビジネスルールがメソッドとして実装されている

### 値オブジェクト (Value Object)

**Question 値オブジェクト** (`app/domain/chat/value_object/question.py`)
```python
MAX_QUESTION_LENGTH = 255

class Question:
    def __init__(self, value: str):
        if len(value) > MAX_QUESTION_LENGTH:
            raise ValueError(f"Question must be less than {MAX_QUESTION_LENGTH} characters long")
        self._value = value
```

**Clean Architecture観点:**
- エンタープライズビジネスルール（文字数制限）を値オブジェクトに封じ込め
- 不変性により予期しない状態変更を防止
- ビジネスルールの一元管理

### リポジトリ抽象 (Repository Interface)

**ChatRepository** (`app/domain/chat/repository/chat.py`)
```python
class ChatRepository(ABC):
    @abstractmethod
    def create(self, chat: Chat) -> Chat:
        pass

    @abstractmethod
    def find_by_id(self, id: Id) -> Chat:
        pass
```

**Clean Architecture観点:**
- 依存性逆転の原則（DIP）を実現
- ドメイン層が外部の永続化技術に依存しない
- インターフェースによる抽象化

## ユースケース層（アプリケーションビジネスルール）

Clean Architectureの第2層で、アプリケーション固有のビジネスロジックを含みます。

### ユースケース実装

**ChatSessionInteractor** (`app/usecase/stream/chat_session.py`)
```python
class ChatSessionInteractor(ChatSessionInputPort):
    def __init__(self, llm_client: LLMClient, chat_repository: ChatRepository):
        self.llm_client = llm_client
        self.chat_repository = chat_repository

    def execute(self, input: ChatSessionInput) -> ChatSessionOutput:
        """アプリケーションビジネスルール: チャットセッションの実行"""
        # 新規初回ループの場合
        if input.is_first and input.title is None:
            # ドメインオブジェクトの協調
            title = self.llm_client.generate_response(input.current_question, GENERATE_TITLE_PROMPT, None)
            chat_id = create_id(str(uuid.uuid4()))
            chat = create_chat(chat_id, create_title(title), [], created_at, updated_at)
            self.chat_repository.create(chat)
```

**Clean Architecture観点:**
- ドメインエンティティを協調させてユースケースを実現
- 外部依存（LLMClient, ChatRepository）はポート経由で抽象化
- アプリケーション固有の業務フローを制御

## インターフェースアダプター層

Clean Architectureの第3層で、データ形式の変換を担当します。

### 入力アダプター（Webハンドラー）

**ChatStreamHandler** (`app/infrastructure/fastapi/handler/stream/chat_stream.py`)
```python
class ChatStreamHandler:
    def __init__(self, chat_session_usecase: ChatSessionInputPort):
        self.chat_session_usecase = chat_session_usecase

    async def handle(self, websocket: WebSocket):
        # WebSocket形式からユースケース形式への変換（Input Adapter）
        data = await websocket.receive_json()
        input = ChatSessionInput(
            chat_id=data["chat_id"],
            current_question=data["current_question"],
            # ...
        )
        
        # ユースケース実行
        output = self.chat_session_usecase.execute(input)
        
        # ユースケース形式からWebSocket形式への変換（Output Adapter）
        await websocket.send_text(output.answer)
```

**Clean Architecture観点:**
- WebSocket形式とユースケース形式の変換
- プレゼンテーション層の詳細をユースケースから隠蔽
- データ形式の境界を明確に定義

### 出力アダプター（リポジトリ実装）

**ChatRepositoryMemoryImpl** (`app/infrastructure/memory/repository/chat.py`)
```python
class ChatRepositoryMemoryImpl(ChatRepository):
    def __init__(self):
        self._chats: list[Chat] = []

    def create(self, chat: Chat) -> Chat:
        """永続化技術の詳細を隠蔽"""
        self._chats.append(chat)
        return chat
```

**Clean Architecture観点:**
- ドメインインターフェースの実装
- 永続化技術（この場合はメモリ）の詳細を隠蔽
- 交換可能な実装（例：メモリ → データベース）

## フレームワーク・ドライバー層

Clean Architectureの最外層で、具体的なフレームワークやツールの詳細を含みます。

### アプリケーション構成

**main.py**
```python
# フレームワーク・ドライバー層での依存性注入
llm_client = create_openai_client()                    # 外部API
chat_repository = create_chat_repository()             # 永続化
chat_session_usecase = create_chat_session_usecase(    # ユースケースに注入
    llm_client, chat_repository
)
stream_handler = create_chat_stream_handler(           # Webハンドラー
    chat_session_usecase
)
fastapi_application = create_fastapi_application(      # Webフレームワーク
    stream_handler, ui_handler
)
```

**Clean Architecture観点:**
- 外側から内側への依存性注入
- フレームワーク（FastAPI）の詳細設定
- アプリケーションの組み立て（Composition Root）

## ポート・アダプターパターン

Clean Architectureの核となるパターンで、このアプリケーションでは明示的にポートが定義されています。

### 入力ポート（Primary Port）

**ChatSessionInputPort** (`app/usecase/ports/input/stream/chat_session.py`)
```python
class ChatSessionInputPort(ABC):
    @abstractmethod
    def execute(self, input: ChatSessionInput) -> ChatSessionOutput:
        pass
```

### 出力ポート（Secondary Port）

**LLMClient** (`app/usecase/ports/output/llm/client.py`)
```python
class LLMClient(ABC):
    @abstractmethod
    def generate_response(self, question: str, prompt: str, chat_history: Optional[str]) -> str:
        pass
```

**Clean Architecture観点:**
- ポートはユースケース層で定義されるインターフェース
- 入力ポート：外部からユースケースを呼び出すためのインターフェース
- 出力ポート：ユースケースが外部を呼び出すためのインターフェース
- アダプターがポートを実装し、具体的な技術詳細を提供

### ポート・アダプターの関係図

```
┌─────────────────┐    implements    ┌─────────────────┐
│  WebSocket      │ ──────────────→  │ ChatSessionInput│
│  Handler        │                   │ Port            │
│  (Adapter)      │                   │ (Port)          │
└─────────────────┘                   └─────────────────┘
                                              │
                                              │ uses
                                              ▼
┌─────────────────┐                   ┌─────────────────┐
│   OpenAI        │                   │ ChatSession     │
│   Client        │                   │ Interactor      │
│   (Adapter)     │                   │ (Use Case)      │
└─────────────────┘                   └─────────────────┘
        │                                     │
        │ implements                          │ uses
        ▼                                     ▼
┌─────────────────┐                   ┌─────────────────┐
│   LLMClient     │ ←─────────────────│ ChatRepository  │
│   (Port)        │      uses         │ (Port)          │
└─────────────────┘                   └─────────────────┘
                                              ▲
                                              │ implements
                                              │
                                   ┌─────────────────┐
                                   │   Memory        │
                                   │   Repository    │
                                   │   (Adapter)     │
                                   └─────────────────┘
```

## 依存性逆転の原則（DIP）

Clean Architectureの基本原則で、このアプリケーションでは徹底的に実践されています。

### 依存性の方向

```
外側の層 → 内側の層（依存の方向）
内側の層 ← 外側の層（制御の方向）
```

**実装例:**
```python
# ❌ 悪い例（依存性逆転なし）
class ChatSessionInteractor:
    def __init__(self):
        self.openai_client = OpenAIClient()  # 具象クラスに依存
        self.mysql_repository = MySQLRepository()  # 具象クラスに依存

# ✅ 良い例（依存性逆転あり）
class ChatSessionInteractor:
    def __init__(self, llm_client: LLMClient, chat_repository: ChatRepository):
        self.llm_client = llm_client  # 抽象インターフェースに依存
        self.chat_repository = chat_repository  # 抽象インターフェースに依存
```

**Clean Architecture観点:**
- 内側の層は外側の層を知らない
- 外側の層が内側の層のインターフェースを実装
- 制御の反転（IoC）による疎結合

## 実際の動作フロー

Clean ArchitectureとDDDの融合による実際の処理フローを追ってみましょう：

### 1. 外側から内側への依存性注入（Composition Root）
```python
# main.py - フレームワーク・ドライバー層
llm_client = create_openai_client()                    # 外部依存の実装
chat_repository = create_chat_repository()             # 永続化の実装
chat_session_usecase = create_chat_session_usecase(    # ユースケースに注入
    llm_client, chat_repository
)
```

### 2. リクエスト処理フロー
```python
# 1. Frameworks & Drivers → Interface Adapters
async def handle(self, websocket: WebSocket):
    data = await websocket.receive_json()  # WebSocket形式
    
    # 2. Interface Adapters → Use Cases
    input = ChatSessionInput(               # ユースケース形式に変換
        chat_id=data["chat_id"],
        current_question=data["current_question"]
    )
    
    # 3. Use Cases → Enterprise Business Rules
    output = self.chat_session_usecase.execute(input)
    
    # ユースケース内部での処理
    def execute(self, input):
        # ドメインオブジェクト生成（Enterprise Business Rules）
        question = create_question(input.current_question)
        answer = create_answer(self.llm_client.generate_response(...))
        step = create_step(id, chat_id, question, answer, created_at)
        
        # ドメインロジック実行（Enterprise Business Rules）
        chat.add_step(step)  # エンタープライズビジネスルール
        
        # 外部システム呼び出し（Use Cases → Output Port → Adapter）
        self.chat_repository.update(chat)  # ポート経由での永続化
    
    # 4. Use Cases → Interface Adapters → Frameworks & Drivers
    await websocket.send_text(output.answer)  # WebSocket形式で返却
```

### レイヤー間の責務

| 層 | 責務 | この例での実装 |
|---|---|---|
| **Enterprise Business Rules** | ビジネスの核となるルール | `Chat.add_step()`, `Question`のバリデーション |
| **Use Cases** | アプリケーション固有のビジネスフロー | チャットセッションの管理、LLM呼び出しのオーケストレーション |
| **Interface Adapters** | データ形式の変換 | WebSocket ↔ ユースケース形式の変換 |
| **Frameworks & Drivers** | 技術的詳細 | FastAPI, OpenAI API, メモリストレージ |

## DDDとClean Architectureの融合メリット

このアプリケーションから見える両アーキテクチャの融合メリット：

### 1. **表現力の向上**
- **DDD**: ドメインの概念（Chat, Step, Question）がコードに直接反映
- **Clean Architecture**: ビジネスロジックが技術的詳細から完全に分離

### 2. **保守性の向上**
- **DDD**: ビジネスルールが一箇所に集約（値オブジェクトのバリデーション等）
- **Clean Architecture**: 変更の影響範囲が限定（外側の層の変更が内側に影響しない）

### 3. **テスタビリティの向上**
- **DDD**: ドメインロジックが純粋な関数として テスト可能
- **Clean Architecture**: ポート・アダプターパターンによりモック/スタブが容易

### 4. **拡張性の向上**
- **DDD**: 新しいドメイン概念の追加が既存コードに影響しない
- **Clean Architecture**: 新しい外部システムとの統合がアダプター追加のみで可能

### 5. **技術的負債の軽減**
- **DDD**: ビジネスロジックとデータ構造が一体化し、データ指向の設計を回避
- **Clean Architecture**: フレームワークの変更（FastAPI → Flask等）がビジネスロジックに影響しない

## まとめ

このチャットアプリケーションは、**DDDの戦術的パターン**と**Clean Architectureの構造原則**を効果的に組み合わせた実践例です：

### DDD要素
- **エンティティ**: `Chat`, `Step` - ビジネスアイデンティティとライフサイクル
- **値オブジェクト**: `Question`, `Answer`, `Id` - 不変性とバリデーション
- **リポジトリ**: データアクセスの抽象化
- **ドメインサービス**: ビジネスロジックの協調

### Clean Architecture要素
- **4層構造**: Enterprise Business Rules, Use Cases, Interface Adapters, Frameworks & Drivers
- **依存性逆転**: 内側の層が外側の層に依存しない
- **ポート・アダプターパターン**: 明示的なインターフェース定義
- **境界の明確化**: 各層の責務が明確に分離

この組み合わせにより、**ビジネス価値の高い**、**保守性に優れた**、**変化に強い**アーキテクチャを実現しています。実際のコードを通じて、現代的なソフトウェア設計の実践を学習できる優れた参考例となっています。
