"""document-composer向けエントリーモジュール。"""
import customtkinter as ctk

from typing import Any, Optional, Tuple, Union

from document_composer.gui.basic.dc_font import DCFont
from document_composer.gui.basic.dc_widget import DCWidget


class DCEntry(ctk.CTkEntry, DCWidget):  # type: ignore[misc]
    """独自エントリーラッパークラス。"""

    def __init__(
        self,
        master: Any,
        font: Optional[Union[Tuple[object], DCFont]] = None,
        **kwargs: object
    ):
        """コンストラクタ。"""
        super().__init__(
            master,
            font=DCFont() if font is None else font,
            **kwargs)

    def set_value(self, value: str) -> None:
        """値のセット。

        Args:
            value (str): 値。
        """
        self.delete(0, ctk.END)
        self.insert(0, value)
