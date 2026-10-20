import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    // Vuetify 4 の初期値は OS の設定に合わせる system なので、これまでどおり light に固定します。
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          // Vuetify 2 のときと同じ色にします。
          primary: '#1976D2',
          error: '#FF5252'
        }
      }
    }
  }
})
