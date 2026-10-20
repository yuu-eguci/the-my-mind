# frontend

Vue 3.5 + Vuetify 4 + Vite 8。
Node.js 24 と npm で動かす。

```bash
npm ci
VUE_APP_BACKEND_BASE_URL=http://localhost:8000 npm run serve  # http://localhost:8080/the-my-mind/
VUE_APP_BACKEND_BASE_URL=http://localhost:8000 npm run build
npm run lint  # ESLint 10 (eslint.config.js)
npm test      # Vitest (tests/)
```

- 画面は `src/App.vue`。
- API 呼び出しや表示の整形は `src/game.js`。
- テストは `tests/` (`game.js` と `App.vue`)。
- Docker で動かす手順は、リポジトリ直下の README を参照。
