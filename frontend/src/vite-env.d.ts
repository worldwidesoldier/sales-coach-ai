/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BACKEND_URL?: string;
  readonly VITE_FEATURE_FLAG_OVERRIDE?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
