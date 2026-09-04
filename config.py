# AI PC操作アシスタント設定ファイル

# Ollama設定
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llava"  # LLaVA ビジョンモデル

# スクリーンキャプチャ設定
SCREENSHOT_INTERVAL = 2  # スクリーンショット取得間隔（秒）
SCREENSHOT_QUALITY = 85  # JPG品質

# GUI設定
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
OVERLAY_WIDTH = 400
OVERLAY_HEIGHT = 300
OVERLAY_OPACITY = 0.9

# マウス操作設定
MOUSE_SPEED = 0.5  # マウス移動速度（秒）
CONFIRM_BEFORE_ACTION = True  # 操作前に確認を要求

# ログ設定
LOG_FILE = "ai_assistant.log"
LOG_LEVEL = "INFO"

# セーフティ設定
DANGEROUS_KEYWORDS = [
    "delete",
    "rm ",
    "unlink",
    "format",
    "reboot",
    "shutdown",
    "kill",
    "remove",
]

# AIプロンプト設定
VISION_PROMPT = """
このスクリーンショットを分析してください。
以下をJSON形式で返してください：

{
  "visible_elements": ["要素1", "要素2", ...],
  "description": "画面の説明",
  "detected_buttons": [{"name": "ボタン名", "x": 100, "y": 50}],
  "text_content": "画面に表示されているテキスト",
  "application": "実行中のアプリケーション"
}

必ずJSON形式で返してください。
"""

ACTION_PROMPT_TEMPLATE = """
現在の画面状態：
{screen_description}

ユーザーの命令：
{user_command}

以下をJSON形式で返してください：
{{
  "action": "click|type|scroll|drag|key",
  "target": "対象要素の名前",
  "x": 座標X,
  "y": 座標Y,
  "reason": "この操作を実行する理由",
  "confidence": 0.0-1.0
}}

必ずJSON形式で返してください。
"""
