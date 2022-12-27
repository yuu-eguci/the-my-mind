<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <h1 class="d-flex align-center">
        THE MY MIND
      </h1>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <v-alert
          elevation="4"
          shaped
          :type="alertType"
          v-show="message"
        >
          {{ message }}
        </v-alert>
        <v-card
          elevation="4"
          shaped
        >
          <v-card-title>
            初期化
          </v-card-title>
          <v-card-text>
            <v-btn
              color="blue-grey"
              class="ma-2 white--text"
              elevation="2"
              x-large
              :disabled="disabledInitializationButton"
              @click="onClickInit"
            >
              <v-icon
                left
                dark
              >
                mdi-domain
              </v-icon>
              初期化する
            </v-btn>
          </v-card-text>

          <v-card-title>
            数字をとる
          </v-card-title>
          <v-card-text>
            <v-btn
              color="blue-grey"
              class="ma-2 white--text"
              elevation="2"
              x-large
              @click="onClickNumbers"
            >
              <v-icon
                left
                dark
              >
                mdi-hand-back-left
              </v-icon>
              数字をとる
            </v-btn>
          </v-card-text>

          <v-card-title>
            数字を出す
          </v-card-title>
          <v-card-text>
            <v-btn
              color="blue-grey"
              class="ma-2 white--text"
              elevation="2"
              x-large
              @click="onClickNumber"
            >
              <v-icon
                left
                dark
              >
                mdi-upload
              </v-icon>
              数字を出す 001
            </v-btn>
            <v-btn
              color="blue-grey"
              class="ma-2 white--text"
              elevation="2"
              x-large
              @click="onClickNumber"
            >
              <v-icon
                left
                dark
              >
                mdi-upload
              </v-icon>
              数字を出す 033
            </v-btn>
            <v-btn
              color="blue-grey"
              class="ma-2 white--text"
              elevation="2"
              x-large
              @click="onClickNumber"
            >
              <v-icon
                left
                dark
              >
                mdi-upload
              </v-icon>
              数字を出す 051
            </v-btn>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>

    <v-footer padless>
      <v-col
        class="text-center"
        cols="12"
      >
        {{ new Date().getFullYear() }} — <strong>yuu-eguci</strong>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import axios from 'axios'

const callApi = async function (url) {
  try {
    const response = await axios.post(url, {
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export default {
  name: 'App',

  components: {
  },

  data: () => ({
    message: '',
    alertType: 'success',

    // 連打を防止します。
    disabledInitializationButton: false
  }),

  async mounted () {
    console.info('Started!')
  },

  methods: {
    onClickInit: async function () {
      const result = await callApi(`${process.env.VUE_APP_BACKEND_BASE_URL}/init`)
      console.info(result.statusCode, result.body)
      this.alertType = result.statusCode === 200 ? 'success' : 'warning'
      if (result.body.message) {
        this.message = result.body.message
      }
      this.disabledInitializationButton = true
    },

    onClickNumbers: async function () {
      const result = await callApi(`${process.env.VUE_APP_BACKEND_BASE_URL}/numbers`)
      console.info(result.statusCode, result.body)
      this.alertType = result.statusCode === 200 ? 'success' : 'warning'
      if (result.body.message) {
        this.message = result.body.message
      }
    },

    onClickNumber: async function () {
      const result = await callApi(`${process.env.VUE_APP_BACKEND_BASE_URL}/number`)
      console.info(result.statusCode, result.body)
      this.alertType = result.statusCode === 200 ? 'success' : 'warning'
      if (result.body.message) {
        this.message = result.body.message
      }
    },
  },
};
</script>
