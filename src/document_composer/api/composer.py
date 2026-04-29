"""コンポーザーモジュール。"""
import os
import pathlib
import shutil
import logging

from typing import Any, Dict, Mapping, Type

from document_composer.models.composable.protocol import Composable
from document_composer.models.composable.docx import Docx
from document_composer.models.composable.txt import Txt
from document_composer.config import Config
from document_composer.constants import (
    CONFIG_FILE_PATH,
    Extension,
    LoggerName
)


class Composer:
    """コンポーザー。"""

    def __init__(self, config: Config, logger: logging.Logger | None = None):
        """コンストラクタ。

        Args:
            config (Config): 構成情報。
            logger (logging.Logger): ロガー。
        """
        self.config: Config = config
        self.logger: logging.Logger | None = logger

    @classmethod
    def from_dict(cls, d: Dict[str, Any], logger: logging.Logger | None = None) -> 'Composer':
        """辞書からインスタンスを生成する。

        Args:
            d (dict): 辞書。
            logger (logging.Logger): ロガー。

        Returns:
            Converter: インスタンス。
        """
        return cls(Config.from_dict(d), logger=logger)

    @classmethod
    def from_yml(cls, config_file_path: str = CONFIG_FILE_PATH, logger: logging.Logger | None = None) -> 'Composer':
        """YAMLファイルからインスタンスを生成する。

        Args:
            config_file_path (str): 構成ファイルまでのパス。
            logger (logging.Logger): ロガー。

        Return:
            Converter: インスタンス。
        """
        return cls(Config.from_yml(config_file_path), logger=logger)

    def compose_verbosely(
        self,
        src_root_dir_path: pathlib.Path,
        dest_root_dir_path: pathlib.Path,
        can_remove: bool,
        src_type: Type[Composable],
        dest_type: Type[Composable]
    ) -> list[tuple[list[Composable], Composable | None]]:
        """コンポーズの冗長実行を行う。

        Args:
            src_root_dir_path (pathlib.Path): 入力元ルートディレクトリ。入力元の最も上層のディレクトリ。
            dest_root_dir_path (pathlib.Path): 出力先ルートディレクトリ。出力先の最も上層のディレクトリ。
            can_remove (bool): 削除フラグ。出力先ディレクトリの削除可否。
            src_type (Type[Composable]): 入力ファイルのファイル形式を示す型引数。
            dest_type (Type[Composable]): 出力ファイルのファイル形式を示す型引数。

        Returns:
            list[tuple[list[Composable], Composable | None]]: 入力ファイル群と出力ファイルの組み合わせのリスト。
        """
        ret = []
        # 出力先ディレクトリをセット
        self._reset_dest_dir(dest_root_dir_path, can_remove)
        # 入力元ディレクトリをすべて検索
        src_dir_pathes = self._find_pathes(src_root_dir_path, "**", self.config.ignorants)
        src_dir_pathes = [p for p in src_dir_pathes if p.is_dir()]
        for src_dir_path in src_dir_pathes:
            # 出力先ディレクトリのパスを導出
            dest_dir_path = pathlib.Path(str(src_dir_path.resolve()).replace(
                str(src_root_dir_path.resolve()),
                str(dest_root_dir_path.resolve())))
            # 出力ファイルのパスを導出
            if src_dir_path.resolve() == src_root_dir_path.resolve():
                dest_file_name = self.config.dest_root_file_nickname + "." + dest_type.get_extension()
                dest_file_path = dest_dir_path / dest_file_name
            else:
                dest_file_name = dest_dir_path.name + "." + dest_type.get_extension()
                dest_file_path = dest_dir_path / pathlib.Path(dest_file_name)
            # コンポーズ実行
            tpl = self.compose(src_dir_path, dest_file_path, False, src_type, dest_type)
            ret.append(tpl)
        return ret

    def compose(
        self,
        src_dir_path: pathlib.Path,
        dest_file_path: pathlib.Path,
        can_remove: bool,
        src_type: Type[Composable],
        dest_type: Type[Composable]
    ) -> tuple[list[Composable], Composable | None]:
        """コンポーズを実行する。

        Args:
            src_dir_path (pathlib.Path): 入力元ディレクリのパス。
            dest_file_path (pathlib.Path): 出力ファイルのパス。
            can_remove (bool): 削除フラグ。出力先ディレクトリの削除可否。
            src_type (Type[Composable]): 入力ファイルのファイル形式を示す型引数。
            dest_type (Type[Composable]): 出力ファイルのファイル形式を示す型引数。

        Returns:
            tuple[list[Composable], Composable | None]: 入力ファイル群と出力ファイルの組み合わせ。
        """
        # ファイル検索
        src_file_pathes = self._find_pathes(src_dir_path, "*." + src_type.get_extension(), self.config.ignorants)
        # ファイルが0件の時は中断
        if not src_file_pathes:
            self._log(f"Empty SRC_DIR skipped: {src_dir_path}", logging.WARN)
            return ([], None)
        # 出力先ディレクトリをリセット
        self._reset_dest_dir(dest_file_path.parent, can_remove)
        # 読み込み
        src_files = self._read_files(src_file_pathes, src_type)
        # 集積
        dest_file = dest_type.new_file(dest_file_path, self.config)
        self._accumulate_lines(src_files, dest_file)
        # 書き込み
        dest_file.write_file()
        self._log(f"Created: {dest_file_path}")
        return (src_files, dest_file)

    def _find_pathes(
        self,
        dir_path: pathlib.Path,
        condition: str,
        ignorants: list[pathlib.Path]
    ) -> list[pathlib.Path]:
        ignorants_str = [ig.resolve() for ig in ignorants]  # イグノアリストは絶対パスの文字列にする
        filted_pathes = [p for p in dir_path.rglob(condition) if p.resolve() not in ignorants_str]
        sorted_pathes = sorted(filted_pathes, key=lambda p: str(p.resolve()).split(os.sep))
        return sorted_pathes

    def _read_files(
        self,
        src_file_pathes: list[pathlib.Path],
        src_type: Type[Composable]
    ) -> list[Composable]:
        ret = []
        for src_file_path in src_file_pathes:
            src_file = src_type.new_file(src_file_path, self.config)
            src_file.read_file()
            ret.append(src_file)
            self._log(f"Loaded: {src_file_path}")
        return ret

    def _accumulate_lines(
        self,
        src_files: list[Composable],
        dest_files: Composable
    ) -> Composable:
        for i, src_file in enumerate(src_files):
            dest_files.append_lines(src_file.get_lines())
            if i != len(src_files) - 1:
                dest_files.append_lines(self.config.file_separator)
        return dest_files

    def _reset_dest_dir(self, dest_dir_path: pathlib.Path, can_remove: bool) -> None:
        if can_remove and dest_dir_path.exists():
            shutil.rmtree(str(dest_dir_path))
            self._log(f"Removed: {dest_dir_path}", logging.WARN)
        if not dest_dir_path.exists():
            dest_dir_path.mkdir(parents=True)
            self._log(f"Created: {dest_dir_path}")

    def _log(
        self,
        msg: str,
        level: int = logging.INFO,
        args: Any = None,
        exc_info: Any = None,
        extra: Mapping[str, object] | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
    ) -> None:
        if self.logger is None:
            print(msg)
        else:
            self.logger._log(
                level=level,
                msg=msg,
                args=args,
                exc_info=exc_info,
                extra=extra,
                stack_info=stack_info,
                stacklevel=stacklevel)


def get_composable_type(ext: Extension) -> Type[Composable]:
    """ファイル種別からComposableの型情報を取得する。

    Args:
        ext (Extension): ファイル種別。

    Returns:
        Type[Composable]: Composableの型情報。
    """
    match(ext):
        case "txt":
            return Txt
        case "docx":
            return Docx
        case _:
            return Txt


def exec_composer(
    src_dir_path: str,
    dest_dir_path: str,
    config_file_path: str,
    src_file_ext: Extension,
    dest_file_ext: Extension,
    verbose: bool,
    logger_name: LoggerName
) -> None:
    """コンポーザーを実行する。

    Args:
        src_dir_path (str): 入力元ディレクトリまでのパス。
        dest_dir_path (str): 出力先ディレクトリまでのパス。
        config_file_path (str): 構成ファイルまでのパス。
        src_file_ext (Extension): 入力ファイルのファイル形式。
        dest_file_ext (Extension): 出力ファイルのファイル形式。
        verbose (bool): 冗長出力を行うか。
        logger_name (LoggerName): ロガー名。
    """
    # 入出力対象の型を取得
    src_type: Type[Composable] = get_composable_type(src_file_ext)
    dest_type: Type[Composable] = get_composable_type(dest_file_ext)
    # コンポーザー生成
    composer = Composer.from_yml(config_file_path, logging.getLogger(logger_name))
    if verbose:
        composer.compose_verbosely(
            pathlib.Path(src_dir_path),
            pathlib.Path(dest_dir_path),
            True,
            src_type,
            dest_type)
    else:
        dest_file_name = composer.config.dest_root_file_nickname + "." + dest_type.get_extension()
        composer.compose(
            pathlib.Path(src_dir_path),
            pathlib.Path(dest_dir_path) / pathlib.Path(dest_file_name),
            True,
            src_type,
            dest_type)
