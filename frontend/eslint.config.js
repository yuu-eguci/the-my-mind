const js = require('@eslint/js')
const pluginVue = require('eslint-plugin-vue')
const globals = require('globals')

module.exports = [
  {
    ignores: ['dist/']
  },
  js.configs.recommended,
  ...pluginVue.configs['flat/vue2-essential'],
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node
      }
    }
  }
]
