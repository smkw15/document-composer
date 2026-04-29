"""document-composer向けフレームモジュール。"""
import customtkinter as ctk

from typing import Any

from document_composer.gui.basic.dc_widget import DCWidget


class DCFrame(ctk.CTkFrame, DCWidget):  # type: ignore[misc]
    """独自フレームラッパークラス。"""

    def __init__(self, master: Any, **kwargs: object):
        """コンストラクタ。"""
        super().__init__(
            master,
            fg_color="transparent",
            bg_color="transparent",
            **kwargs)
