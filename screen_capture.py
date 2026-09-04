"""
スクリーンキャプチャモジュール
定期的にスクリーンショットを取得し、画像処理を行う
"""

import pyautogui
import threading
import time
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ScreenCapture:
    """スクリーンキャプチャクラス"""

    def __init__(self, interval=2):
        """
        初期化
        
        Args:
            interval (int): キャプチャ間隔（秒）
        """
        self.interval = interval
        self.is_running = False
        self.current_screenshot = None
        self.last_capture_time = None
        self.capture_thread = None
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)

    def start(self):
        """キャプチャスレッド開始"""
        if self.is_running:
            logger.warning("スクリーンキャプチャは既に実行中です")
            return

        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        logger.info("スクリーンキャプチャを開始しました")

    def stop(self):
        """キャプチャスレッド停止"""
        self.is_running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=5)
        logger.info("スクリーンキャプチャを停止しました")

    def _capture_loop(self):
        """
        キャプチャループ
        定期的にスクリーンショットを取得
        """
        while self.is_running:
            try:
                self.capture_screenshot()
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"スクリーンキャプチャエラー: {e}")
                time.sleep(self.interval)

    def capture_screenshot(self):
        """
        スクリーンショットを取得
        
        Returns:
            PIL.Image: キャプチャした画像
        """
        try:
            # スクリーンショット取得
            screenshot = pyautogui.screenshot()
            self.current_screenshot = screenshot
            self.last_capture_time = datetime.now()
            
            logger.debug(
                f"スクリーンショット取得: {screenshot.size} "
                f"({self.last_capture_time})"
            )
            return screenshot
        except Exception as e:
            logger.error(f"スクリーンショット取得失敗: {e}")
            return None

    def get_current_screenshot(self):
        """
        現在のスクリーンショットを取得
        
        Returns:
            PIL.Image: 最後にキャプチャした画像
        """
        return self.current_screenshot

    def save_screenshot(self, name=None):
        """
        スクリーンショットをファイルに保存
        
        Args:
            name (str): ファイル名（省略時は自動生成）
            
        Returns:
            Path: 保存したファイルパス
        """
        if self.current_screenshot is None:
            logger.warning("保存するスクリーンショットがありません")
            return None

        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}.png"

        filepath = self.screenshot_dir / name
        self.current_screenshot.save(filepath)
        logger.info(f"スクリーンショット保存: {filepath}")
        return filepath

    def get_screenshot_info(self):
        """
        スクリーンショット情報を取得
        
        Returns:
            dict: スクリーンショット情報
        """
        if self.current_screenshot is None:
            return {"status": "取得未実施"}

        return {
            "size": self.current_screenshot.size,
            "mode": self.current_screenshot.mode,
            "last_capture": self.last_capture_time.isoformat() if self.last_capture_time else None,
        }


class ScreenAnalyzer:
    """スクリーン分析クラス"""

    @staticmethod
    def get_screen_resolution():
        """
        画面解像度を取得
        
        Returns:
            tuple: (幅, 高さ)
        """
        try:
            width, height = pyautogui.size()
            return width, height
        except Exception as e:
            logger.error(f"画面解像度取得失敗: {e}")
            return None, None

    @staticmethod
    def get_mouse_position():
        """
        マウスカーソル位置を取得
        
        Returns:
            tuple: (x, y)
        """
        try:
            x, y = pyautogui.position()
            return x, y
        except Exception as e:
            logger.error(f"マウス位置取得失敗: {e}")
            return None, None

    @staticmethod
    def screenshot_to_base64(screenshot):
        """
        スクリーンショットをBase64に変換
        
        Args:
            screenshot (PIL.Image): 画像オブジェクト
            
        Returns:
            str: Base64エンコードされた画像データ
        """
        import base64
        import io

        try:
            buffer = io.BytesIO()
            screenshot.save(buffer, format="PNG")
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return image_base64
        except Exception as e:
            logger.error(f"Base64変換失敗: {e}")
            return None


if __name__ == "__main__":
    # テスト実行
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # スクリーンキャプチャテスト
    capture = ScreenCapture(interval=1)
    capture.start()
    
    time.sleep(3)
    
    # スクリーンショット取得・保存
    screenshot = capture.get_current_screenshot()
    if screenshot:
        capture.save_screenshot("test_screenshot.png")
        print(f"スクリーンショット情報: {capture.get_screenshot_info()}")
    
    # スクリーン情報取得
    analyzer = ScreenAnalyzer()
    width, height = analyzer.get_screen_resolution()
    x, y = analyzer.get_mouse_position()
    print(f"画面解像度: {width}x{height}")
    print(f"マウス位置: ({x}, {y})")
    
    capture.stop()
