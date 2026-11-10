# 自動研究セッションの手順書

毎日の Routine で起動したセッションが従う手順。研究上のルールは `CLAUDE.md`、研究の状況は `research_log.md`、課題は `research_queue.md` にある。人間は見ていないので、質問せずに最後まで自律的に進める。

**最重要原則：成果は課題を1つ終えるたびに、その場でコミットして push する。** トークンや時間がいつ尽きても、それまでの成果が残るようにする。最後にまとめて push しない。

---

## 0. 環境の準備（10分以内を目安）

1. **リポジトリ**：作業ディレクトリが `open_quantum_physics` のチェックアウトであることを確認し、`git fetch origin main && git checkout main && git pull --no-rebase origin main` で main の最新に合わせる。リポジトリの持ち主は main への直接コミット・push を許可している。新しいブランチやプルリクエストは作らない。
2. **日付**：ファイル名の日付は日本時間を使う（`TZ=Asia/Tokyo date +%F`）。
3. **TeX**：`lualatex` が無ければ次で入れる。`texlive-science` は無い環境があるので別にして、失敗しても続ける。
   ```sh
   apt-get update -qq
   DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
     texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-lang-japanese \
     texlive-luatex texlive-fonts-recommended latexmk poppler-utils
   DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends texlive-science || true
   ```
4. **Python**：`pip install` は止まることがあるので、まず apt を使う。
   ```sh
   DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-numpy python3-scipy python3-sympy python3-matplotlib
   ```
   その後は `/usr/bin/python3` で実行する（`python3` は numpy の無い別の Python を指すことがある）。QuTiP などが必要なときだけ `timeout 300 /usr/bin/python3 -m pip install --break-system-packages <pkg>` を試す。
5. **論文**：arXiv の本文は `curl -sSL https://arxiv.org/pdf/<id> -o <dir>/<id>.pdf` で取得し、`pdftotext` で読む。ダウンロードしたファイルはスクラッチパッドの専用ディレクトリに置き、リポジトリには入れない。

## 1. 把握と検証（毎回、最初に行う）

1. `CLAUDE.md`、`research_log.md`（特に「現在の状況」「成果の検証状況」「次のAIへの申し送り」）、`research_queue.md` を読む。
2. 「成果の検証状況」で ⏳（未レビュー）と ⚠️（要修正）の主張について、元のノートと検算スクリプトを読み、**論理が正しいかを独立に判断する**。
   - 導出を1行ずつ追い、使われている仮定を明示する。
   - 検算スクリプトを再実行し、必要なら別の方法（SymPy での記号計算、別の数値例、極限の場合）でも確かめる。
   - 引用文献の主張が本文と合っているかを確認する。
3. 結果を「成果の検証状況」の表に記録する（✅／⚠️／❌、根拠を一言）。誤りを見つけたら、元のノートは書き換えず、訂正ノート `notes/YYYY-MM-DD_correction_<題名>.tex` を書き、訂正を直す課題をキューの先頭に追加する。
4. **ここで一度コミットして push する。**

検証に時間をかけすぎない。未レビューの項目が多いときは、新しいものと重要なものを優先し、残りは ⏳ のまま次回に回す。

## 2. 研究（課題を1つずつ、尽きるまで繰り返す）

`research_queue.md` の未完了の課題を上から順に取る（検証で追加された訂正課題が最優先）。課題ごとに次を行う。

1. キューの該当行を `[~]` にする。
2. **先行研究の確認**：その問いが既に解かれていないか、arXiv の本文と Web 検索で確かめる。解かれていれば、それを記録して次の課題へ進む（それも成果である）。
3. **研究**：導出・証明・数値計算を行う。検算に使ったスクリプトは `scripts/` に置く。課題が大きすぎるときは、小課題に分割してキューに書き、そのうち1つを仕上げる。
4. **ノートにまとめる**：`notes/YYYY-MM-DD_<短い英語の題名>.tex` に書き（`notes/preamble.tex` を `\input`）、`cd notes && latexmk -lualatex -interaction=nonstopmode <file>.tex` で PDF にする。ビルドエラーが無いことを確認し、可能なら `pdftoppm` で1ページ画像にして表示を確かめる。ノートには必ず次を区別して書く：文献で確認済み／自分で導出・検算済み／推測・未検証（`\unverified`）。
5. **記録を更新する**：
   - `research_queue.md`：完了した課題を `[x]`（ノート名を添える）。途中なら `[~]` のまま、どこまで進んだかを書く。新しく生まれた課題を適切な位置に追加する。
   - `research_log.md`：今日の「セッション記録」に1項目追記し、「成果の検証状況」に新しい主張を ⏳ で追加し、「現在の状況」と「次のAIへの申し送り」を書き換える。
6. **コミットして push する**（`.tex`、`.pdf`、スクリプト、キュー、ログをまとめて）。これで1課題が完了。次の課題へ進む。

課題はいくつ進めてもよい。行き詰まったら、何を試して何が分からなかったかを記録し、push してから次の課題へ進む。

## 3. 終了時

余力があるうちに、`research_log.md` の「次のAIへの申し送り」を見直す。次にやるべきこと、その理由、注意点（使える手法・はまりどころ・環境の問題）を具体的に書き、push する。最終メッセージには、今日完了した課題、主な成果、push が成功したかを書く。

## push について

- non-fast-forward で拒否されたら `git pull --no-rebase origin main` してから再度 push する。force push・rebase・amend はしない。
- **認証・権限のエラー（403 など）で push できない場合**：回避策（別の認証情報など）は試さない。成果を失わないため、`git format-patch origin/main --stdout -- . ':!*.pdf'` でパッチを作り、スクラッチパッド内のファイルとして Artifact に添付して公開する（`files` に `{"session.patch": {"from": <パス>, "contentType": "text/plain"}}`）。研究はローカルで続け、課題を終えるたびにパッチを作り直して同じ Artifact に再公開する。最終メッセージの先頭に、push 失敗とその Artifact の URL を書く。

## 変更してはいけないもの

環境設定・Routine の設定・リポジトリの設定は変更しない。既存のノートや記録は削除・書き換えしない（訂正は新しいノートとログで行う）。人間が書いた課題を削除しない。
