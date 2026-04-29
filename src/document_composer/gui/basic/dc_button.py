"""document-composer向けボタンモジュール。"""
import customtkinter as ctk

from typing import Any, Tuple, Union, Optional, Callable

from document_composer.gui.basic.dc_font import DCFont
from document_composer.gui.basic.dc_widget import DCWidget


class DCButton(ctk.CTkButton, DCWidget):  # type: ignore[misc]
    """独自ボタンラッパークラス。"""

    def __init__(
        self,
        master: Any,
        text: str,
        command: Callable[[], Any],
        font: Optional[Union[Tuple[object], DCFont]] = None,
        **kwargs: object
    ):
        """コンストラクタ。"""
        super().__init__(
            master,
            text=text,
            command=command,
            bg_color="transparent",
            font=DCFont(weight="bold") if font is None else font,
            **kwargs)
