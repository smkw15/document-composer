"""document-composer向けラベルモジュール。"""
import tkinter as tk
import customtkinter as ctk

from typing import Any, Tuple, Union, Optional

from document_composer.gui.basic.dc_font import DCFont
from document_composer.gui.basic.dc_widget import DCWidget


class DCLabel(ctk.CTkLabel, DCWidget):  # type: ignore[misc]
    """独自ラベルラッパークラス。"""

    def __init__(
        self,
        master: Any,
        text: str,
        width: int = 0,
        height: int = 28,
        font: Optional[Union[Tuple[object], ctk.CTkFont]] = None,
        anchor: str = tk.W,
        **kwargs: object
    ):
        """コンストラクタ。"""
        super().__init__(
            master,
            width,
            height,
            text=text,
            anchor=anchor,
            bg_color="transparent",
            font=DCFont() if font is None else font,
            **kwargs)
