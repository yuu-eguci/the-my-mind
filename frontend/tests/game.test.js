import { beforeEach, describe, expect, it, vi } from 'vitest'
import axios from 'axios'
import {
  callApi,
  formatNumberLabel,
  formatPlayMessage,
  HOW_MANY_CHOICES,
  isSuccess,
  NumberButton,
  playResultView,
  shouldDisableNumberButton
} from '../src/game'

vi.mock('axios')

describe('callApi', () => {
  beforeEach(() => {
    vi.resetAllMocks()
    vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  it('200 のとき response.data を返します。', async () => {
    const data = { statusCode: 200, body: { message: 'ok', numbers: [1, 2] } }
    axios.post.mockResolvedValue({ status: 200, data })

    expect(await callApi('http://example.test/numbers')).toEqual(data)
    expect(axios.post).toHaveBeenCalledWith(
      'http://example.test/numbers',
      {},
      expect.objectContaining({ validateStatus: expect.any(Function) })
    )
  })

  it('payload をそのまま POST します。', async () => {
    axios.post.mockResolvedValue({ status: 200, data: { statusCode: 200, body: {} } })

    await callApi('http://example.test/number', { number: 42 })

    expect(axios.post.mock.calls[0][1]).toEqual({ number: 42 })
  })

  it('backend の形ではないレスポンス (502 など) のときも statusCode と body.message を返します。', async () => {
    axios.post.mockResolvedValue({ status: 502, data: 'Internal Server Error' })

    expect(await callApi('http://example.test/numbers')).toEqual({
      statusCode: 502,
      body: { message: 'サーバでエラーが起きました。' }
    })
  })

  it('4xx でも例外にせず response.data を返します。', async () => {
    axios.post.mockResolvedValue({ status: 400, data: { statusCode: 400, body: { message: 'まだ配られていません。' } } })

    const result = await callApi('http://example.test/number', { number: 1 })

    expect(result.statusCode).toBe(400)
    expect(result.body.message).toBe('まだ配られていません。')
    const validateStatus = axios.post.mock.calls[0][2].validateStatus
    expect(validateStatus(400)).toBe(true)
    expect(validateStatus(409)).toBe(true)
  })

  it('通信エラーのとき null ではなくエラー用の結果を返します。', async () => {
    axios.post.mockRejectedValue(new Error('Network Error'))

    const result = await callApi('http://example.test/init')

    expect(result).toEqual({ statusCode: 0, body: { message: 'サーバにつながりませんでした。' } })
  })
})

describe('formatNumberLabel', () => {
  it('3 桁にゼロ埋めします。', () => {
    expect(formatNumberLabel(1)).toBe('001')
    expect(formatNumberLabel(42)).toBe('042')
    expect(formatNumberLabel(100)).toBe('100')
  })
})

describe('NumberButton', () => {
  it('最初は押せて、 disable() で押せなくなります。', () => {
    const button = new NumberButton(7)
    expect(button.number).toBe(7)
    expect(button.disabledButton).toBe(false)

    button.disable()

    expect(button.disabledButton).toBe(true)
  })
})

describe('formatPlayMessage', () => {
  it('numbers_out を【】で囲んで message の後ろに付けます。', () => {
    expect(formatPlayMessage({ message: '出せました。', numbers_out: [3, 15] }))
      .toBe('出せました。 【3】,【15】')
  })

  it('numbers_out がないときは message だけを返します。', () => {
    expect(formatPlayMessage({ message: 'まだ配られていません。' })).toBe('まだ配られていません。')
  })

  it('numbers_out が空のときは message だけを返します。', () => {
    expect(formatPlayMessage({ message: '出せました。', numbers_out: [] })).toBe('出せました。')
  })
})

describe('shouldDisableNumberButton', () => {
  it('200 と 409 のとき押せなくします。', () => {
    expect(shouldDisableNumberButton(200)).toBe(true)
    expect(shouldDisableNumberButton(409)).toBe(true)
  })

  it('それ以外のときは押せるままにします。', () => {
    expect(shouldDisableNumberButton(0)).toBe(false)
    expect(shouldDisableNumberButton(400)).toBe(false)
    expect(shouldDisableNumberButton(500)).toBe(false)
  })
})

describe('playResultView', () => {
  it('ふつうに出せたときは success で overlay を出しません。', () => {
    expect(playResultView({ statusCode: 200, body: { game_set: false, game_clear: false } }))
      .toEqual({ alertType: 'success', overlayText: '' })
  })

  it('409 のときは warning で overlay を出しません。', () => {
    expect(playResultView({ statusCode: 409, body: { game_set: false, game_clear: false } }))
      .toEqual({ alertType: 'warning', overlayText: '' })
  })

  it('400 で game_set などがないときは warning です。', () => {
    expect(playResultView({ statusCode: 400, body: { message: 'まだ配られていません。' } }))
      .toEqual({ alertType: 'warning', overlayText: '' })
  })

  it('game_set のときは error でゲームオーバーの overlay を出します。', () => {
    expect(playResultView({ statusCode: 200, body: { game_set: true, game_clear: false } }))
      .toEqual({ alertType: 'error', overlayText: 'ゲームオーバーです。お疲れ様でした。' })
  })

  it('game_clear のときは success でクリアの overlay を出します。', () => {
    expect(playResultView({ statusCode: 200, body: { game_set: false, game_clear: true } }))
      .toEqual({ alertType: 'success', overlayText: 'クリアです。お疲れ様でした。' })
  })
})

describe('isSuccess', () => {
  it('200 のとき true を返します。', () => {
    expect(isSuccess({ statusCode: 200, body: { message: '初期化しました。' } })).toBe(true)
  })

  it('通信エラーの 0 や 4xx, 5xx のときは false を返します。', () => {
    expect(isSuccess({ statusCode: 0, body: { message: 'サーバにつながりませんでした。' } })).toBe(false)
    expect(isSuccess({ statusCode: 400, body: { message: 'まだ初期化されていません。' } })).toBe(false)
    expect(isSuccess({ statusCode: 409, body: {} })).toBe(false)
    expect(isSuccess({ statusCode: 500, body: {} })).toBe(false)
  })
})

describe('HOW_MANY_CHOICES', () => {
  it('とる枚数として 1 から 12 までを選べます。', () => {
    expect(HOW_MANY_CHOICES).toEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
  })
})
