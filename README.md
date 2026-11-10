# open_quantum_physics

開放量子系（Lindblad 方程式・散逸による量子相・有効リウビリアン）の理論研究ノート。

## 構成

| パス | 内容 |
|---|---|
| `research_log.md` | 研究の経緯・現在の状況・成果の検証状況・次のAIへの申し送り・文献の確認状況。毎回まずここを読む |
| `research_queue.md` | 次に取り組む問いのリスト（上から順に処理） |
| `CLAUDE.md` | 研究上のルール（手動・自動の両方のセッションが従う） |
| `ROUTINE.md` | 毎日の自動研究セッションの手順書 |
| `notes/` | TeX ノートと生成した PDF（`.tex` と `.pdf` を両方コミットする） |
| `notes/preamble.tex` | 全ノート共通のプリアンブル |
| `scripts/` | 検算に使ったスクリプト |

## ノートのビルド

LuaLaTeX（LuaTeX-ja）を使う。

```sh
cd notes && latexmk -lualatex -interaction=nonstopmode 2026-11-09_overview.tex
```

TeX Live の入れ方は `ROUTINE.md` の「0. 環境の準備」を参照。
