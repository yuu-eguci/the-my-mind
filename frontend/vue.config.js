const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: '/the-my-mind/',
  css: {
    loaderOptions: {
      sass: {
        // Vuetify 2 の Sass が出す非推奨警告は、こちらでは直せないので表示しません。
        sassOptions: {
          silenceDeprecations: ['import', 'global-builtin', 'slash-div', 'if-function']
        }
      }
    }
  }
})
