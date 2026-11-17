# frontend

Vue 3.5 + Vuetify 4 + Vite 8 + TypeScript 6。
Node.js 26 (Active LTS) と npm で動かす。 バージョンは `package.json` の `engines.node` で、 CI と GitHub Pages の CD はここから読む。 Docker の `node:26-slim` もそろえている (`tests/node-version.test.ts` で確認)。
TypeScript は 6.0 のまま。 TypeScript 7.0 は API をもたず、 vue-tsc と typescript-eslint が対応していないため。

```bash
npm ci
VUE_APP_BACKEND_BASE_URL=http://localhost:8000 npm run serve  # http://localhost:8080/the-my-mind/
VUE_APP_BACKEND_BASE_URL=http://localhost:8000 npm run build
npm run lint       # ESLint 10 + typescript-eslint (eslint.config.ts)
npm run typecheck  # vue-tsc (tsconfig.json, strict)
npm test           # Vitest (tests/)
```

- 画面は `src/App.vue` (`<script lang="ts">`)。
- API 呼び出しや表示の整形は `src/game.ts`。 backend の応答の型もここ。
- `VUE_APP_BACKEND_BASE_URL` の型は `src/env.d.ts`。
- テストは `tests/` (`game.ts` と `App.vue`)。
- Docker で動かす手順は、リポジトリ直下の README を参照。
