# open_quantum_physics

開放量子系（Lindblad 方程式・散逸による量子相・有効リウビリアン）の理論研究ノート。

## 構成

| パス | 内容 |
|---|---|
| `research_log.md` | 研究の経緯・現在の状況・文献の確認状況。毎回まずここを読む |
| `research_queue.md` | 次に取り組む問いのリスト（上から順に処理） |
| `notes/` | TeX ノートと生成した PDF（`.tex` と `.pdf` を両方コミットする） |
| `notes/preamble.tex` | 全ノート共通のプリアンブル |

## ノートのビルド

LuaLaTeX（LuaTeX-ja）を使う。

```sh
cd notes && latexmk -lualatex -interaction=nonstopmode 2026-11-09_overview.tex
```

TeX Live が入っていない環境では次で入る（Ubuntu）:

```sh
apt-get install -y --no-install-recommends texlive-latex-base texlive-latex-recommended \
  texlive-latex-extra texlive-lang-japanese texlive-luatex texlive-fonts-recommended \
  texlive-science latexmk
```
