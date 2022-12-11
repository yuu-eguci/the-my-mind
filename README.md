# the-my-mind

The Mind というテーブルゲームを、ぷろぐらむで再現してみようぜ! というプロジェクト。
Backend: Python + Flask + AWS Lambda; Frontend: Vue.js + GitHub Pages; CI/CD: GitHub Actions

The Mind: https://bodoge.hoobby.net/games/mind

## How to set up on the local env

1. Open two terminals.

```bash
# 2. Run backend
cd backend
pipenv sync --dev
pipenv run python local_test.py
```

```bash
# 3. Run frontend
cd frontend
yarn install
yarn serve
```

4. Open `http://localhost:8000/` and `http://localhost:8080/the-my-mind/`
