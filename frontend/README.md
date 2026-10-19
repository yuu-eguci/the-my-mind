# frontend

Vue 2.7 + Vuetify 2.7 + Vue CLI 5 です。 Node.js 24 と npm を使います。

```bash
npm ci
VUE_APP_BACKEND_BASE_URL=http://localhost:8000 npm run serve  # http://localhost:8080/the-my-mind/
VUE_APP_BACKEND_BASE_URL=http://localhost:8000 npm run build
npm run lint  # ESLint 9 (eslint.config.js)
npm test      # Vitest (tests/)
```

- 画面は `src/App.vue` です。
- API 呼び出しや表示用の整形など、画面以外のロジックは `src/game.js` にあり、 `tests/game.test.js` でテストしています。
- Docker で動かすときは、リポジトリ直下の README を参照してください。
