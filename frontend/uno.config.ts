import extractorSvelte from "@unocss/extractor-svelte"
import { defineConfig, presetIcons, presetUno, presetWebFonts, transformerDirectives, transformerVariantGroup } from "unocss"

const config = defineConfig({
  extractors: [extractorSvelte()],
  transformers: [transformerVariantGroup(), transformerDirectives()],
  presets: [presetUno({ preflight: "on-demand" }), presetIcons(), presetWebFonts({ provider: "bunny", fonts: { mono: { name: "JetBrains Mono Variable", provider: "none" } } })],
})

export default config
