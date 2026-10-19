the-my-mind
===

The Mind というテーブルゲームを、ぷろぐらむで再現してみようぜ! というプロジェクト。

- Docker: 対応!
- Python: 3.14!
- Node.js: 24!
- Linter: Ruff (backend), ESLint (frontend)!
- Test: pytest (backend), Vitest (frontend)!
- Flask (ローカル開発用), Vue 2.7, Vuetify 2.7

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

GitHub Actions の CI (`.github/workflows/ci.yml`) では、これに加えて frontend の build と `docker compose build` も実行します。

## デプロイ

- `.github/workflows/cd-backend.yml` (AWS Lambda) と `.github/workflows/cd-frontend.yml` (GitHub Pages) は手動実行 (workflow_dispatch) のみです。
- main への push では自動デプロイしません。
- Lambda 関数のランタイムは AWS 側で Python 3.14 に設定します。
- ゲームの状態は Lambda の `/tmp` に保存します。 `/tmp` は実行環境ごとに別なので、 Lambda の予約同時実行数を 1 にします。実行環境が入れ替わると状態は消えるので、遊ぶ前に「初期化する」を押します。

### Caution

- このプロジェクトは Vuetify 2 を使っているが、このプロジェクトで遊んでいるさなかに Vuetify 3 がリリースされた。 Vuetify 3 のドキュメントを見ないように注意。
