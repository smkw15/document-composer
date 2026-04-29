# document-composer

document-composerは、複数の文書ファイルを結合し、1つの文書ファイルとして出力するPythonモジュールです。

## 開発環境

- Windows 11
- Python 3.14.4
- uv

## 環境構築方法

```sh
# uv下準備
uv self update
uv pip install --upgrade pip

# Pythonインストール・バージョン固定
uv python install 3.14.4
uv python pin 3.14.4

# 仮想環境構築
uv venv .venv
uv sync

# 開発用の仮想環境とする場合
uv sync --extra dev

# リリース用の仮想環境とする場合
uv sync --extra release
```

## ディレクトリ構造

```txt
📁./
├─📁.venv  👈uv管理の仮想環境ディレクトリ
├─📁.github  👈GitHub設定ディレクトリ
├─📁.logs  👈ロギング出力ディレクトリ
├─📁build  👈配布物用ビルドファイルディレクトリ(実行時自動作成)
├─📁dist  👈配布物用ディレクトリ(実行時自動作成)
├─📁docs
│　├─📁dest  👈デフォルトの出力先ディレクトリ(実行時自動作成)
│　└─📁src  👈デフォルトの入力元ディレクトリ
├─📁src  👈document-composerのソースコード
│　└─📁document_composer  👈document_composerパッケージ
│　　 ├─📁resources  👈画像などのリースファイル
│　　 ├─📄config.yml  👈構成ファイル
│　　 ├─📄logging.yml  👈ロギング構成ファイル
│　　 └─🐍main.py  👈エントリーポイント
├─📄.flake8  👈flake8設定ファイル
├─📄.gitignore  👈Gitのignore設定ファイル
├─📄.python-version  👈Pythonバージョン固定ファイル
├─📄.user.yml  👈ユーザ入力ファイル(GUI用、実行時自動作成)
├─📄document_composer.spec  👈配布物作成用仕様ファイル
├─⚖️LICENSE.txt  👈ライセンス情報ファイル
├─📄pyproject.toml  👈プロジェクト管理ファイル
├─📄README.md  👈本テキスト
└─📄uv.lock  👈UV管理の依存パッケージロックファイル
```

## 動作仕様

document-composerは、`入力元ディレクトリ`に存在する文書ファイル(`入力ファイル`)を検索し、それらの内容(`ファイルコンテンツ`)を1つに結合した後、`出力先ディレクトリ`に文書ファイル(`出力ファイル`)として保存します。このファイルコンテンツの結合処理は、「コンポーズ」と呼ばれ、コンポーズは以下に示す手順で実行されます。

1. 入力ファイルの検索
2. 入力ファイルのフィルタリング
3. 入力ファイルのソート
4. ファイルコンテンツの結合
5. 出力ファイルの保存

**入力ファイルの検索**では、入力元ディレクトリに存在する特定の拡張子を持つファイルが検索されます。検索は再帰的に行われ、入力元ディレクトリ内の存在するすべてのフォルダ・ファイルが対象になります。検索条件になる拡張子は、`コマンドライン引数`や`GUI`でユーザが自由に設定することができます。

**入力ファイルのフィルタリング**では、`イグノアリスト`を利用した処理対象外のファイルの除外が行われます。`イグノアリスト`は、`構成ファイル`に定義されており、ユーザはこのイグノアリストを編集することで、特定のファイルがコンポーズに含まれないようにすることができます。

**入力ファイルのソート**では、コンポーズの対象になった入力ファイルを順番に並び替えます。ここでは、各入力ファイルがフォルダごとに名前の順で並び替えられます。

**ファイルコンテンツの結合**では、入力ファイルのファイルコンテンツを1つのファイルコンテンツにまとめます。その際、ファイルごとの境界を示す`ファイルセパレータ`がファイルごとに挿入されます。ファイルセパレータにどのような文字列を用いるかは、構成ファイルに定義されており、ユーザが自由に変更することができます。

**出力ファイルの保存**では、1つにまとめられたファイルコンテンツが特定の拡張子で出力先ディレクトリに保存されます。この出力ファイルのファイル名には、既定のファイル名が用いられます。この既定のファイル名もまた構成ファイルに定義されており、ユーザが自由に変更することができます。

## 使用方法

以下のコマンドでdocument-composerのメインモジュールを実行します。メインモジュールが終了すると、出力先ディレクトリに出力ファイルが保存されます。なお、このコマンドはWindowsでもLinux/Mac OSでも同様です。

```sh
uv run document_composer
  [--src <src_dir_path>]
  [--dest <dest_dir_path>]
  [--config <config_file_path>]
  [-x <src_file_extension>]
  [-y <dest_file_extension>]
  [--verbose]
  [--ui <user_interface>]
```

### コマンドライン引数

メインモジュールには、必要に応じてコマンドライン引数を渡すことができます。コマンドライン引数では、主に入出力に関わる内容を指定することができます。また、コンポーズに用いる構成ファイルや、「冗長出力を行うかどうか」「UIに何を利用するか」を指定することもできます。

| 引数 | 初期値 | 説明 |
| -- | -- | -- |
| `--src`または`-s` | `./docs/src` | 入力元ディレクトリまでのパス。 |
| `--dest`または`-d` | `./docs/dest` | 出力先ディレクトリまでのパス。 |
| `--config`または`-c` | `./config.yaml` | 構成ファイルまでのパス。 |
| `-x` | `txt` | 入力ファイルの形式を示す文字列。`txt`か`docx`。 |
| `-y` | `txt` | 出力ファイルの形式を示す文字列。`txt`か`docx`。 |
| `--verbose`または`-v` | `False` | 冗長出力を行うかどうか。真偽値で`True`の時は冗長出力を実行する、`False`の時は冗長出力を実行しない。 |
| `--ui`または`-u` | `cui`または`gui` | UIに何を利用するか。`cui`の時はCUIで実行、`GUI`の時はGUIを起動する。 |

#### 構成ファイルオプション

`--config`は、構成ファイルオプションです。構成ファイルまでのパスを指定します。

構成ファイルには、コンポーズの内部仕様を決定する各種設定値が定義されています。ユーザはこのファイルを編集することで、コンポーズの細かい動作を制御することができます。

| 設定値名 | 初期値 | 内容 |
| -- | -- | -- |
| `ignorants` | `[]` | イグノアリスト。入力対象外にするファイル・ディレクトリまでのパス。相対パスでも絶対パスでもよい。 |
| `dest_root_file_nickname` | `__all_in_one__` | 最上層の出力ファイル(出力ルートファイル)のファイル名。拡張子を記載しない。 |
| `file_separator` | `['', "＊", '']` | ファイルセパレータ。1つの配列要素が1行の文字列に相当する。 |
| `paragraph_style_name` | `Body Text` | 段落のスタイル。python-docxの仕様に基づく。 |
| `paragraph_pt_before` | `0.0` | 段落間スペースのサイズ。段落前。 |
| `paragraph_pt_after` | `0.0` | 段落間スペースのサイズ。段落後。 |
| `page_width_mm` | `210.0` | ページサイズの横幅。mm単位。 |
| `page_height_mm` | `297.0` | ページサイズの縦幅。mm単位。 |
| `left_margin_mm` | `19.0` | ページの余白の左。mm単位。 |
| `top_margin_mm` | `19.0` | ページの余白の右。mm単位。 |
| `right_margin_mm` | `19.0` | ページの余白の上。mm単位。 |
| `bottom_margin_mm` | `19.0` | ページの余白の下。mm単位。 |
| `header_distance_mm` | `19.0` | ヘッダーの幅。mm単位。 |
| `footer_distance_mm` | `19.0` | フッターの幅。mm単位。 |
| `encoding` | `utf-8` | 文字エンコーディング方式。 |
| `newline_code_src` | `LF` | 入力ファイル改行コード。`LF`、`CRLF`、`LF`のどれか。 |
| `newline_code_dest` | `LF` | 出力ファイル改行コード。`LF`、`CRLF`、`LF`のどれか。 |

**注意: 現在のdocument-composerは`txt`ファイルと`docx`ファイルの読み込みにのみ対応していますが、これらの読み込み処理には改行コードを用いていないため、`newline_code_src`は使われていない設定値になります。将来的に対応ファイルが増えた際のニーズを見込んで実装が残されています。**

改行コードは、一般に多く見られる仕様に準じて定義されています。

| 改行コード | 改行文字 | 対応OS |
| -- | -- | -- |
| `LF` | `\n` | Unix/Linux、Mac OS X以降 |
| `CRLF` | `\r\n` | Windows |
| `CR` | `\r` | Mac OS 9以前 |

#### 冗長出力オプション

`--verbose`は、冗長出力オプションです。冗長出力を行うかどうかを指定します。

冗長出力とは、入力ディレクトリに存在する全階層で、その階層を単位としたコンポーズを実行する出力形式を指します。つまり、出力先ディレクトリに入力元ディレクトリと同様な階層構造が作成され、そのディレクトリごとに、個別の出力ファイルが保存されます。その際、出力ファイルのファイル名には、元になった入力元フォルダのフォルダ名が用いられます。なお、冗長出力を行う場合でも、既定の出力ファイル(全階層のすべての入力ファイルを含む出力ファイル)が保存されます。

##### 通常の出力

```txt
📁docs/src
├─📁A
│　├─📄A1
│　└─📄A2
└─📁B
　　├─📄B1
　　└─📄B2

👇処理結果

📁docs/dest
└─📄__all_in_one__  👈A1 + A2 + B1 + B2
```

##### 冗長出力

```txt
📁docs/src
├─📁A
│　├─📄A1
│　└─📄A2
└─📁B
 　├─📄B1
 　└─📄B2

👇処理結果

📁docs/src
├─📁A
│　└─📄A  👈A1 + A2
├─📁B
│　└─📄B  👈B1 + B2
└─📄__all_in_one__  👈A1 + A2 + B1 + B2
```

#### UIオプション

`--ui`は、UIオプションです。UIオプションには、`cui`または`gui`のどちらか文字列を指定します。

`cui`を指定した場合、document-composerがCUI(Character User Interface)で実行されます。すなわち、そのままコンポーズが実行されます。

`gui`を指定した場合、document-composerのGUIアプリケーションが起動します。ユーザはそのGUI(Graphical User Interface)を通してコンポーズを実行することができます。なお、`gui`を指定してGUIアプリケーションを起動した場合、その他のコマンドライン引数は無視されます(GUIによってコマンドライン引数に相当する項目を指定することになるため)。

`--ui`オプションの初期値は、document-composerをどのように起動したかで異なります。Pythonのスクリプトとしてコマンドラインから実行した場合は、`cui`が初期値となります。配布された実行ファイルから実行した場合は、`gui`が初期値となります。これらは、開発に適したユーザインターフェースがCUIであり、配布物に適したユーザインターフェースがGUIであることを考慮した仕様です。

GUIでは、コマンドライン引数と同様な項目を指定することができ、「実行」ボタンを押下することで、コンポーズを実行することができます(画面にはログも表示されます)。この時、GUIで入力した内容は、`ユーザ入力ファイル`に保存され、次にユーザがGUIを利用した際の初期値となります。

![image](./src/document_composer/resources/gui.png)

GUIアプリケーションの操作方法は、[GUIマニュアル](./src/document_composer/resources/manual.html)を参照してください。

### ロギング

document-composerは、ロギング構成ファイルの定義に基づいてロギングを行います。この時のログローテーションの初期設定は、以下の通りです。

| 設定値名 | 初期値 | 説明 |
| -- | -- | -- |
| `when` | `W6` | 毎週日曜日深夜 |
| `interval` | `1` | 1週間ごと |
| `backupCount` | `12` | 最大3か月分(12週間分) |
| `utc` | `False` | 現地時間で |

## ビルド方法

以下のコマンドでビルドを行うことができます。

```sh
uv build
```

コマンドが終了すると、配布物用ディレクトリにwheelが作成されます。なお、ファイル名に付されたバージョン番号(`0.1.0`など)は、document-composerのバージョンによって異なります。

```txt
./
├─📁dist
│　├─📦document_composer-0.1.0-py3-none-any.whl
│　└─📦document_composer-0.1.0.tar.gz
├─📄document_composer.spec
└─📄main.py
```

作成された`*.whl`ファイル、または、`*.tar.gz`ファイルを別のPythonインストール済みの環境でインストールすることで、その環境でもDocumentComoserを利用できるようになります。

```sh
# pip install
pip install document_composer-0.1.0-py3-none-any.whl
# or
pip install document_composer-0.1.0.tar.gz

# 実行
document_composer 
  [--src <src_dir_path>]
  [--dest <dest_dir_path>]
  [--config <config_file_path>]
  [-x <src_file_extension>]
  [-y <dest_file_extension>]
  [--verbose]
  [--ui <user_interface>]
```

## 配布方法

document-composerでは、[PyInstaller](https://github.com/pyinstaller/pyinstaller)を利用した実行ファイルの作成に対応しています。実行ファイルを作成するには、以下のコマンドを実行します。

```sh
uv run pyinstaller --clean document_composer.spec
```

コマンドが終了すると、配布物用ディレクトリに実行ファイルとそれに関連したファイルが作成されます。

```txt
./
├─📁build
├─📁dist
│　├─📁document_composer_exe
│　│　├─📁_internal
│　│　│　├─📁...
│　│　│　└─📁document_composer
│　│　│　　├─📁resources
│　│　│　　│　├─🖼️gui.png
│　│　│　　│　├─🖼️icon64.ico
│　│　│　　│　├─🖼️icon64.png
│　│　│　　│　├─📄manual.html
│　│　│　　│　└─📄manual.css
│　│　│　　├─📄config.yml
│　│　│　　└─📄logging.yml
│　│　├─📄README.md
│　│　├─⚖️LICENSE.txt
│　│　└─🤖document_composer.exe
│　└─📦document_composer_exe.zip
├─📄document_composer.spec
└─📄main.py
```

配布すべきものは、`dist/document_composer_exe`ディレクトリ内のすべてのファイル・フォルダです。しかし、実際には、`document_composer_exe.zip`がそれらすべてを含んでいるので、このZIPファイル1つを配布すれば済むようになっています。

実行ファイル`document_composer.exe`を起動すると、document-composerのGUIが表示されます。

今のところ、実行ファイルの作成/配布は、Windowsにおいてのみ対応しています。

使い方を記載したドキュメントは、`README.md`と`manual.html`です。`README.md`は開発者向けの内容なので、一般ユーザには`manual.html`を読むように教示することを推奨しています。

## ライセンス情報ファイル出力方法

ライセンス情報ファイルを作成するには、以下のコマンドで仮想環境を整備してから`pip-licenses`を利用します。

```sh
uv sync --all-extras
uv run pip-licenses --format=plain-vertical --with-license-file --output-file LICENSE.txt --ignore-packages document-composer --no-license-path
```

| 引数 | 値 | 説明 |
| -- | -- | -- |
| `--format=*` | `plain-vertical` | フォーマットを指定します。`plain-vertical`は1パッケージごとにブロックで出力します。`json`にすると、JSON文字列で出力できます。 |
| `--with-license-file` | `True` | ライセンス本文を追加で出力します。 |
| `--output-file` | `LICENSE.txt` | 出力先のファイルを指定します。 |
| `--ignore-packages` | `document-composer` | 出力に含めないパッケージを指定します。`pip-licenses`は仕様で自身のライセンス情報を含めてしまうので、ここでは`document-composer`を除きます。 |
| `--no-license-path` | `True` | ライセンス情報が記載されたファイルまでのパスを出力しないようにします。ローカル環境のディレクトリが公開されてしまうため、ここでは出力しない設定にしています。 |

**注意: `pip-licenses`は情報の取得に失敗すると、`UNKNOWN`という文字列を出力します。出力後のLICENSE.txtに`UNKNOWN`が含まれている場合は、手動で穴埋めしてください。**
