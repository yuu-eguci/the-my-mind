the-my-mind
===

The Mind というテーブルゲームを、ぷろぐらむで再現してみようぜ! というプロジェクト。

- Docker: 対応!
- Python: 3.14!
- Node.js: 24!
- Linter: Ruff (backend), ESLint (frontend)!
- Test: pytest (backend), Vitest (frontend)!
- Flask (ローカル開発用), Vue 3.5, Vuetify 4, Vite 8

The Mind: https://bodoge.hoobby.net/games/mind

## パッと実行してみたい

```bash
docker compose up --build --renew-anon-volumes
# http://localhost:8080/the-my-mind/ を開く
```

## 構成

- backend: Python + AWS Lambda (関数 URL)
    - `backend/lambda_function.py` がゲームの本体
    - `backend/local_test.py` は Flask で HTTP リクエストを `lambda_handler` に渡すローカル開発用のサーバ
- frontend: Vue.js + Vuetify + GitHub Pages
    - `frontend/src/App.vue` が画面

## Lint と Test

```bash
docker compose run --rm backend ruff check .
docker compose run --rm backend ruff format --check .
docker compose run --rm backend pytest
docker compose run --rm frontend npm run lint
docker compose run --rm frontend npm test
```

CI は `.github/workflows/ci.yml`。上のチェックに加えて、 frontend の build と `docker compose build` も実行。

## デプロイ

- `.github/workflows/cd-backend.yml` (AWS Lambda) と `.github/workflows/cd-frontend.yml` (GitHub Pages) は手動実行 (workflow_dispatch) のみ。
- main への push で自動デプロイはしない。
- Lambda のランタイムは AWS 側で Python 3.14 に設定する。
- ゲームの状態は Lambda の `/tmp` に保存。
- `/tmp` は実行環境ごとに別なので、予約同時実行数は 1 に設定する。
- 実行環境が入れ替わると状態が消えるので、遊ぶ前に「初期化する」を押す。
