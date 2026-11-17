// compose や GitHub Actions が渡す backend の URL です。 vite.config.ts の envPrefix で読めるようにしています。
interface ImportMetaEnv {
  readonly VUE_APP_BACKEND_BASE_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
