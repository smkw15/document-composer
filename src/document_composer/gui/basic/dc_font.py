"""document-composer向けフォントモジュール。"""
import customtkinter as ctk

from document_composer.gui.constants import (
    FONT_FAMILY,
    FONT_SIZE_STD
)
from document_composer.gui.basic.dc_widget import DCWidget


class DCFont(ctk.CTkFont, DCWidget):  # type: ignore[misc]
    """独自フォントラッパークラス。"""

    def __init__(
        self,
        family: str = FONT_FAMILY,
        size: int = FONT_SIZE_STD,
        **kwargs: object
    ):
        """コンストラクタ。"""
        super().__init__(family=family, size=size, **kwargs)
