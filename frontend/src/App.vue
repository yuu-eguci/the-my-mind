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
export default {
  name: 'App',

  components: {
  },

  data: () => ({
    //
  }),
};
</script>
