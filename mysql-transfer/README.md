# スキーマ間転送アプリケーション

このアプリケーションは、MySQL Shell ユーティリティを利用してMySQLのスキーマ間転送を行います。
MySQL Shell ユーティリティを使うと、MySQLのバックアップ/リストアの処理速度が高速にできます。[Benchmarks](https://dev.mysql.com/blog-archive/mysql-shell-dump-load-part-2-benchmarks/)を参照ください。

ただ、MySQL Shellユーティリティは、ダンプコマンドとロードコマンドを作成する必要があります。
アプリケーションのテストでは、いくつかのテーブルを別の環境に移行するケースが多く、都度コマンドを作成するのは面倒です。このアプリケーションはそのような作業をする必要はなく、設定ファイル(yaml形式)に必要な情報を設定すると、ダンプとロードの両方のコマンドを実行して、転送元のテーブルを転送先にcopyします。

## 動作環境

|category   |Product/Version       |
|:----------|:---------------------|
|OS         | Windows 11           |
|language   | Python 3.11.3        |
|Middleware | MySQL Shell 8.0.32   |

## install

### MySQLShell 8.0

MySQLShell 8.0を[ここ](../mysqlshell-usage/readme.md)を参照にしてインストールしてください。

### Python Library 

```Shell Session (console)
pip install loguru pyyaml
```

## advance preparation (事前準備)

[settings.yaml.example](config/settings.yaml.example)を[configフォルダー](config)にcopyして「settings.yaml」にリネームし、適時編集してください。


|category     |explain                           |
|:------------|:---------------------------------|
|log:         | ログに関する設定です　　　　　　　　|
| filepath:   | ファイルの出力先を指定します　　　　|
| rotation:   | ファイルのローテーションを指定します|
| retention:  | ファイルの保存期間を指定します　　　|
|dump:        | dumpTables()に関する設定です　　 　|
| user:       | 転送元のMySQLのユーザーID  　　　　|
| passwd:     | 転送元のMySQLのPassword   　　　　|
| host:       | 転送元のMySQLのHost名　　  　　　　|
| port:       | 転送元のMySQLのPort番号    　　　　|
| schema:     | 転送元のMySQLのスキーマ名  　　　　|
| tables:     | 転送元のテーブル名(リストで指定) 　|
| options:    | dumpTables()に指定するオプション(リストで指定) 　|
|load:        | loadDump()に関する設定です　 　　　　　|
| user:       | 転送先のMySQLのユーザーID  　　　　|
| passwd:     | 転送先のMySQLのPassword   　　　　|
| host:       | 転送先のMySQLのHost名　　  　　　　|
| port:       | 転送先のMySQLのPort番号    　　　　|
| schema:     | 転送先のMySQLのスキーマ名  　　　　|
| options:    | loadDump()に指定するオプション(リストで指定) 　|

設定についてはそれぞれ下記を参照ください。

[logの設定(Delgan/loguru)](https://github.com/Delgan/loguru){:target="_blank"}

[tableDumpsユーティリティのオプション](https://dev.mysql.com/doc/mysql-shell/8.0/ja/mysql-shell-utilities-dump-instance-schema.html){:target="_blank"}

[loadDumpユーティリティ](https://dev.mysql.com/doc/mysql-shell/8.0/ja/mysql-shell-utilities-load-dump.html){:target="_blank"}

## usage (実行)

以下のコマンドを実行します。

```Shell Session (console)
python main.py
```
