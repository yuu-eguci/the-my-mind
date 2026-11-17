import axios from 'axios'

// backend (lambda_function.py) が返す body です。 API ごとに含まれるものが違います。
export interface ApiBody {
  message?: string
  numbers?: number[]
  numbers_out?: number[]
  game_set?: boolean
  game_clear?: boolean
}

// statusCode が 0 のときは通信できなかったときです。
export interface ApiResult {
  statusCode: number
  body: ApiBody
}

export type AlertType = 'success' | 'warning' | 'error'

// Lambda の 502 など、 backend が返したのではないレスポンスは body をもちません。
const isApiResult = function (data: unknown): data is ApiResult {
  return typeof data === 'object' && data !== null && 'body' in data
    && typeof data.body === 'object' && data.body !== null
}

// backend は 4xx でも同じ形の JSON を返すので、 HTTP status に関係なく response.data を返します。
export const callApi = async function (url: string, payload: Record<string, unknown> = {}): Promise<ApiResult> {
  try {
    const response = await axios.post<unknown>(url, payload, { validateStatus: () => true })
    if (!isApiResult(response.data)) {
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
export const isSuccess = function (result: ApiResult): boolean {
  return result.statusCode === 200
}

// The Mind ではレベル N のとき各プレイヤーに N 枚配るので、レベル 1 から 12 までの枚数を選べるようにします。
export const HOW_MANY_CHOICES = Array.from({ length: 12 }, (_, i) => i + 1)

export const formatNumberLabel = function (number: number): string {
  return (`000${number}`).slice(-3)
}

// 数値と disabled 属性を、辞書で管理するのがイヤだったので作ったクラスです。
export class NumberButton {
  number: number
  disabledButton: boolean

  constructor (number: number) {
    this.number = number
    this.disabledButton = false
  }

  disable (): void {
    this.disabledButton = true
  }
}

// numbers_out は 400 のときなど body に含まれないことがあります。
// 画面からは message があるときだけ呼びます。
export const formatPlayMessage = function (body: ApiBody): string {
  const numbersOut = body.numbers_out || []
  if (!numbersOut.length) {
    return body.message ?? ''
  }
  return `${body.message} ${numbersOut.map(x => `【${x}】`)}`
}

// 200 は出せたとき、 409 はもう出されていたときなので、どちらも再び押す必要はありません。
export const shouldDisableNumberButton = function (statusCode: number): boolean {
  return statusCode === 200 || statusCode === 409
}

// 数字を出した結果から、 alert の種類と、ボタンを覆う overlay の文言を決めます。 overlay を出さないときは空文字です。
export const playResultView = function (result: ApiResult): { alertType: AlertType, overlayText: string } {
  if (result.body.game_set) {
    return { alertType: 'error', overlayText: 'ゲームオーバーです。お疲れ様でした。' }
  }
  if (result.body.game_clear) {
    return { alertType: 'success', overlayText: 'クリアです。お疲れ様でした。' }
  }
  return { alertType: result.statusCode === 200 ? 'success' : 'warning', overlayText: '' }
}
