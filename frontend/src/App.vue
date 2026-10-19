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
      <v-container>
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
            <v-select
              v-model="howMany"
              :items="howManyChoices"
              label="とる枚数"
              :disabled="disabledGetNumbersButton"
            />
            <v-btn
              color="blue-grey"
              class="ma-2 white--text"
              elevation="2"
              x-large
              :disabled="disabledGetNumbersButton"
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
          <v-card-text v-if="!numbersInHand.length">
            数字をまだとっていない
          </v-card-text>
          <v-card-text>
            <v-btn
              v-for="numberButtonInstance in numbersInHand"
              :key="numberButtonInstance.number"
              color="blue-grey"
              class="ma-2 white--text"
              elevation="2"
              x-large
              :disabled="numberButtonInstance.disabledButton"
              @click="onClickNumber(numberButtonInstance)"
            >
              <v-icon
                left
                dark
              >
                mdi-upload
              </v-icon>
              数字を出す {{ formatNumberLabel(numberButtonInstance.number) }}
            </v-btn>
          </v-card-text>

        <!-- NOTE: Vuetify 3 では扱い方が変わっている。間違って 3 のドキュメントを見ないよう注意。 (このプロジェクトは 2) -->
        <v-overlay
          :absolute="true"
          :value="!!overlayText"
        >
          <v-btn>
            {{ overlayText }}
          </v-btn>
        </v-overlay>
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
import {
  callApi,
  formatNumberLabel,
  formatPlayMessage,
  HOW_MANY_CHOICES,
  isSuccess,
  NumberButton,
  playResultView,
  shouldDisableNumberButton
} from './game'

export default {
  name: 'App',

  components: {
  },

  data: () => ({
    message: '',
    alertType: 'success',

    // 連打を防止します。
    disabledInitializationButton: false,
    disabledGetNumbersButton: false,

    // ボタンをもつエリアを覆う overlay の文言。空文字のときは overlay を出しません。
    overlayText: '',

    // 1 回でとる数字の枚数。 The Mind のレベルと同じ数です。
    howMany: 3,
    howManyChoices: HOW_MANY_CHOICES,

    // 手持ちの数字たち。
    numbersInHand: []
  }),

  computed: {
  },

  async mounted () {
    console.info('Started!')
  },

  methods: {
    onClickInit: async function () {
      // 応答を待つあいだの連打を防ぐため、先に disable にして、失敗したら戻します。
      this.disabledInitializationButton = true
      const result = await callApi(`${process.env.VUE_APP_BACKEND_BASE_URL}/init`)
      console.info(result.statusCode, result.body)
      this.alertType = isSuccess(result) ? 'success' : 'warning'
      if (result.body.message) {
        this.message = result.body.message
      }
      this.disabledInitializationButton = isSuccess(result)
    },

    onClickNumbers: async function () {
      // 応答を待つあいだの連打を防ぐため、先に disable にして、失敗したら戻します。
      this.disabledGetNumbersButton = true
      const result = await callApi(
        `${process.env.VUE_APP_BACKEND_BASE_URL}/numbers`,
        {how_many: this.howMany}
      )
      console.info(result.statusCode, result.body)
      this.alertType = isSuccess(result) ? 'success' : 'warning'
      if (result.body.message) {
        this.message = result.body.message
      }
      this.disabledGetNumbersButton = isSuccess(result)
      if (isSuccess(result)) {
        this.disabledInitializationButton = true
      }
      for (const number of result.body.numbers || []) {
        this.numbersInHand.push(new NumberButton(number))
      }
    },

    onClickNumber: async function (numberButtonInstance) {
      const result = await callApi(
        `${process.env.VUE_APP_BACKEND_BASE_URL}/number`,
        {number: numberButtonInstance.number}
      )
      console.table(result.statusCode)
      console.table(result.body)
      const view = playResultView(result)
      this.alertType = view.alertType
      this.overlayText = view.overlayText
      if (result.body.message) {
        this.message = formatPlayMessage(result.body)
      }
      if (shouldDisableNumberButton(result.statusCode)) {
        numberButtonInstance.disable()
      }
    },

    formatNumberLabel,
  },
};
</script>
