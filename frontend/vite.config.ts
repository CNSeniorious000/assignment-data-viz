import { sveltekit } from "@sveltejs/kit/vite"
import uno from "unocss/vite"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [uno(), sveltekit()],
  build: { sourcemap: true },
})
