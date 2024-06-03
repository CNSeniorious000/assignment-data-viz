import { sveltekit } from "@sveltejs/kit/vite"
import { defineConfig } from "vite"
import uno from "unocss/vite"

export default defineConfig({
  plugins: [uno(), sveltekit()],
  build: { sourcemap: true }
})
