import antfu from "@antfu/eslint-config"

export default antfu({
  formatters: true,
  unocss: true,
  svelte: true,
  lessOpinionated: true,
  stylistic: {
    quotes: "double",
    overrides: {
      "antfu/if-newline": "off",
      "curly": ["error", "all"],
      "style/brace-style": ["error", "1tbs", { allowSingleLine: true }],
      "node/prefer-global/process": "off",
    },
    semi: false,
  },
  overrides: {
    svelte: {
      "import/no-mutable-exports": "off",
    },
  },
})
