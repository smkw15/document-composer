"""document-composer向けチェックボックスモジュール。"""
import tkinter as tk
import customtkinter as ctk

from typing import Any, Optional, Tuple, Union

from document_composer.gui.basic.dc_font import DCFont
from document_composer.gui.basic.dc_widget import DCWidget


class DCCheckBox(ctk.CTkCheckBox, DCWidget):  # type: ignore[misc]
    """独自チェックボックスラッパークラス。"""

    def __init__(
        self,
        master: Any,
        text: str = "",
        font: Optional[Union[Tuple[object], DCFont]] = None,
        **kwargs: object
    ):
        """コンストラクタ。"""
        self.checked = tk.BooleanVar()
        super().__init__(
            master,
            text=text,
            bg_color="transparent",
            font=DCFont() if font is None else font,
            variable=self.checked,
            **kwargs)
