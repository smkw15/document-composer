"""document-composer向けテキストボックスモジュール。"""
import customtkinter as ctk

from typing import Any, Optional, Tuple, Union

from document_composer.gui.basic.dc_font import DCFont
from document_composer.gui.basic.dc_widget import DCWidget


class DCTextbox(ctk.CTkTextbox, DCWidget):  # type: ignore[misc]
    """独自テキストボックスクラス。"""

    def __init__(
        self,
        master: Any,
        font: Optional[Union[Tuple[object], DCFont]] = None,
        readonly: bool = False,
        **kwargs: object
    ):
        """コンストラクタ。"""
        super().__init__(
            master,
            font=DCFont() if font is None else font,
            **kwargs)
        self.readonly = readonly
        if self.readonly:
            self.configure(state="disabled")

    def set_value(self, value: str) -> None:
        """値のセット。

        Args:
            value (str): 値。
        """
        if self.readonly:
            self.configure(state="normal")
            self.delete("1.0", ctk.END)
            self.insert(ctk.END, value)
            self.configure(state="disabled")
        else:
            self.delete("1.0", ctk.END)
            self.insert(ctk.END, value)

    def insert_value(self, value: str) -> None:
        """値の挿入。

        Args:
            value (str): 値。
        """
        _value = value + "\n"
        if self.readonly:
            self.configure(state="normal")
            self.insert(ctk.END, _value)
            self.configure(state="disabled")
        else:
            self.insert(ctk.END, _value)
