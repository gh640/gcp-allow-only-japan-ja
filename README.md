# `gcp_allow_only_japan.py`

Google Cloud Platform で日本以外からのアクセスをブロックするルールを作成するためのスクリプトです。
あくまでもサンプルです。

## 使い方

1. リポジトリをチェックアウト
2. 日本の IP アドレスの一覧を用意
3. プロジェクト名を変更
4. スクリプトを実行

### 1. リポジトリをチェックアウト

本リポジトリを `git clone` でチェックアウトします。

```bash
git clone https://github.com/gh640/gcp-allow-only-japan-ja.git
```

リポジトリのルートディレクトリに移動しておきます。

```bash
cd gcp-allow-only-japan-ja
```

### 2. 日本の IP アドレスの一覧を用意

日本の IP アドレスの一覧を取得します。
ここでは https://ipv4.fetus.jp/ で公開されているものを利用させていただきます。

```bash
curl -O https://ipv4.fetus.jp/jp.txt
```

次のようなファイルがダウンロードできれば OK です。

```bash
head jp.txt
#
# [jp] 日本 (Japan)
#  https://ipv4.fetus.jp/jp.txt
#  出力日時: 2021-02-11 21:37:55 JST (2021-02-11 12:37:55 UTC)
#

1.0.16.0/20
1.0.64.0/18
1.1.64.0/18
1.5.0.0/16
```

### 3. プロジェクト名を変更

コード内のプロジェクト名の値を実際のものに変更します。

該当箇所:

```python
GCP_PROJECT = '__GCP_PROJECT_NAME__'
```

### 4. スクリプトを実行

スクリプトを実行します。

最初に `--dry-run` オプションを付けて実行して、うまく動きそうか確認します。

```bash
python3 gcp_allow_only_japan.py --dry-run
```

問題なさそうなら `--dry-run` なしで実行します。

```bash
python3 gcp_allow_only_japan.py
```

13 件ほどのルールを直列で作成するため、しばらく時間がかかります。

## 関連リポジトリ

- [GitHub - gh640/gcp-block-country-ja](https://github.com/gh640/gcp-block-country-ja)

## 参考

- [ipv4.fetus.jp : 国/地域別IPアドレス(IPv4アドレス)割り当て一覧](https://ipv4.fetus.jp/)
