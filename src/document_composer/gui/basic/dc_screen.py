"""document-composer向けスクリーンモジュール。"""
import customtkinter as ctk

from document_composer.gui.basic.dc_widget import DCWidget


class DCScreen(ctk.CTk, DCWidget):  # type: ignore[misc]
    """独自スクリーンのラッパークラス。"""

    def __init__(self, title: str = "", size: str = "", **kwargs: object):
        """コンストラクタ。"""
        super().__init__(**kwargs)
        self.title(title)
        self.geometry(size)
