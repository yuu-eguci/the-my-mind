import axios from 'axios'

// backend は 4xx でも同じ形の JSON を返すので、 HTTP status に関係なく response.data を返します。
export const callApi = async function (url, payload = {}) {
  try {
    const response = await axios.post(url, payload, { validateStatus: () => true })
    // Lambda の 502 など、 backend が返したのではないレスポンスは body をもちません。
    if (typeof response.data?.body !== 'object') {
      return { statusCode: response.status, body: { message: 'サーバでエラーが起きました。' } }
    }
    return response.data
  } catch (error) {
    console.error(error)
    // 通信できなかったときも、画面側が statusCode と body.message を読めるようにします。
    return { statusCode: 0, body: { message: 'サーバにつながりませんでした。' } }
  }
}

// 通信エラーの 0 や 4xx のときは false です。失敗したときはボタンを押せるままにして、やり直せるようにします。
export const isSuccess = function (result) {
  return result.statusCode === 200
}

// The Mind ではレベル N のとき各プレイヤーに N 枚配るので、レベル 1 から 12 までの枚数を選べるようにします。
export const HOW_MANY_CHOICES = Array.from({ length: 12 }, (_, i) => i + 1)

export const formatNumberLabel = function (number) {
  return (`000${number}`).slice(-3)
}

// 数値と disabled 属性を、辞書で管理するのがイヤだったので作ったクラスです。
export class NumberButton {
  constructor (number) {
    this.number = number
    this.disabledButton = false
  }

  disable () {
    this.disabledButton = true
  }
}

// numbers_out は 400 のときなど body に含まれないことがあります。
export const formatPlayMessage = function (body) {
  const numbersOut = body.numbers_out || []
  if (!numbersOut.length) {
    return body.message
  }
  return `${body.message} ${numbersOut.map(x => `【${x}】`)}`
}

// 200 は出せたとき、 409 はもう出されていたときなので、どちらも再び押す必要はありません。
export const shouldDisableNumberButton = function (statusCode) {
  return statusCode === 200 || statusCode === 409
}

// 数字を出した結果から、 alert の種類と、ボタンを覆う overlay の文言を決めます。 overlay を出さないときは空文字です。
export const playResultView = function (result) {
  if (result.body.game_set) {
    return { alertType: 'error', overlayText: 'ゲームオーバーです。お疲れ様でした。' }
  }
  if (result.body.game_clear) {
    return { alertType: 'success', overlayText: 'クリアです。お疲れ様でした。' }
  }
  return { alertType: result.statusCode === 200 ? 'success' : 'warning', overlayText: '' }
}
