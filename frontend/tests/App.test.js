import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import App from '../src/App.vue'
import { callApi } from '../src/game'

// 通信はせず、 callApi の結果をテストごとに決めます。
vi.mock('../src/game', async (importOriginal) => ({
  ...await importOriginal(),
  callApi: vi.fn()
}))

// v-overlay が参照する visualViewport は happy-dom にないので、 Vuetify が扱える null を入れます。
globalThis.visualViewport ??= null

const mountApp = function () {
  return mount(App, {
    attachTo: document.body,
    global: { plugins: [createVuetify()] }
  })
}

const findButton = function (wrapper, text) {
  return wrapper.findAll('button').find(button => button.text().includes(text))
}

// 応答を待つあいだの状態を確かめるため、あとから resolve できる Promise を返します。
const deferred = function () {
  let resolve
  const promise = new Promise(r => { resolve = r })
  return { promise, resolve }
}

describe('App', () => {
  let wrapper

  beforeEach(() => {
    vi.resetAllMocks()
    vi.stubEnv('VUE_APP_BACKEND_BASE_URL', 'http://backend.test')
    vi.spyOn(console, 'info').mockImplementation(() => {})
    vi.spyOn(console, 'table').mockImplementation(() => {})
  })

  afterEach(() => {
    wrapper.unmount()
    vi.unstubAllEnvs()
  })

  it('「数字をとる」を素早く 2 回押しても API は 1 回だけ呼ばれます。', async () => {
    const response = deferred()
    callApi.mockReturnValue(response.promise)
    wrapper = mountApp()

    const button = findButton(wrapper, '数字をとる')
    await button.trigger('click')
    await button.trigger('click')
    response.resolve({ statusCode: 200, body: { message: '配りました。', numbers: [7] } })
    await flushPromises()

    expect(callApi).toHaveBeenCalledTimes(1)
    expect(button.attributes('disabled')).toBeDefined()
    expect(findButton(wrapper, '数字を出す 007').exists()).toBe(true)
  })

  it('「初期化する」を素早く 2 回押しても API は 1 回だけ呼ばれます。', async () => {
    const response = deferred()
    callApi.mockReturnValue(response.promise)
    wrapper = mountApp()

    const button = findButton(wrapper, '初期化する')
    await button.trigger('click')
    await button.trigger('click')
    response.resolve({ statusCode: 200, body: { message: '初期化しました。' } })
    await flushPromises()

    expect(callApi).toHaveBeenCalledTimes(1)
    expect(callApi.mock.calls[0][0]).toBe('http://backend.test/init')
    expect(wrapper.text()).toContain('初期化しました。')
  })

  it('初期化に失敗したらボタンを押せるように戻し、やり直せます。', async () => {
    callApi.mockResolvedValue({ statusCode: 0, body: { message: 'サーバにつながりませんでした。' } })
    wrapper = mountApp()

    const button = findButton(wrapper, '初期化する')
    await button.trigger('click')
    await flushPromises()

    expect(button.attributes('disabled')).toBeUndefined()
    expect(wrapper.text()).toContain('サーバにつながりませんでした。')
    await button.trigger('click')
    await flushPromises()
    expect(callApi).toHaveBeenCalledTimes(2)
  })

  it('数字をとるのに失敗したらボタンを押せるように戻し、やり直せます。', async () => {
    callApi.mockResolvedValue({ statusCode: 400, body: { message: 'まだ初期化されていません。' } })
    wrapper = mountApp()

    const button = findButton(wrapper, '数字をとる')
    await button.trigger('click')
    await flushPromises()

    expect(button.attributes('disabled')).toBeUndefined()
    expect(wrapper.text()).toContain('まだ初期化されていません。')
    await button.trigger('click')
    await flushPromises()
    expect(callApi).toHaveBeenCalledTimes(2)
  })

  it('とる枚数は初期値 3 で送ります。', async () => {
    callApi.mockResolvedValue({ statusCode: 200, body: { numbers: [] } })
    wrapper = mountApp()

    await findButton(wrapper, '数字をとる').trigger('click')
    await flushPromises()

    expect(callApi.mock.calls[0][0]).toBe('http://backend.test/numbers')
    expect(callApi.mock.calls[0][1]).toEqual({ how_many: 3 })
  })

  it('選んだとる枚数を送ります。', async () => {
    callApi.mockResolvedValue({ statusCode: 200, body: { numbers: [] } })
    wrapper = mountApp()

    const select = wrapper.findComponent({ name: 'VSelect' })
    expect(select.props('items')).toEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    await select.vm.$emit('update:modelValue', 5)
    await findButton(wrapper, '数字をとる').trigger('click')
    await flushPromises()

    expect(callApi.mock.calls[0][1]).toEqual({ how_many: 5 })
  })

  const dealAndPlay = async function (playResult) {
    callApi
      .mockResolvedValueOnce({ statusCode: 200, body: { numbers: [12, 34] } })
      .mockResolvedValueOnce(playResult)
    wrapper = mountApp()
    await findButton(wrapper, '数字をとる').trigger('click')
    await flushPromises()
    const button = findButton(wrapper, '数字を出す 012')
    await button.trigger('click')
    await flushPromises()
    return button
  }

  it('出した数字を送り、 200 のときはそのボタンを disable にします。', async () => {
    const button = await dealAndPlay({ statusCode: 200, body: { message: '出しました。' } })

    expect(callApi.mock.calls[1][0]).toBe('http://backend.test/number')
    expect(callApi.mock.calls[1][1]).toEqual({ number: 12 })
    expect(button.attributes('disabled')).toBeDefined()
    expect(findButton(wrapper, '数字を出す 034').attributes('disabled')).toBeUndefined()
  })

  it('409 のときもそのボタンを disable にします。', async () => {
    const button = await dealAndPlay({ statusCode: 409, body: { message: 'もう出されています。' } })

    expect(button.attributes('disabled')).toBeDefined()
  })

  it('400 のときはそのボタンを押せるままにします。', async () => {
    const button = await dealAndPlay({ statusCode: 400, body: { message: 'まだ配られていません。' } })

    expect(button.attributes('disabled')).toBeUndefined()
  })

  it('game_set のときはゲームオーバーの overlay を出します。', async () => {
    await dealAndPlay({ statusCode: 200, body: { message: '失敗。', game_set: true, numbers_out: [5] } })

    expect(document.body.textContent).toContain('ゲームオーバーです。お疲れ様でした。')
    expect(wrapper.text()).toContain('失敗。 【5】')
    // overlay は card の中に出て、 scrim でボタンを覆います。
    expect(wrapper.find('.v-card .v-overlay--contained .v-overlay__scrim').exists()).toBe(true)
  })

  it('game_clear のときはクリアの overlay を出します。', async () => {
    await dealAndPlay({ statusCode: 200, body: { message: '成功。', game_clear: true } })

    expect(document.body.textContent).toContain('クリアです。お疲れ様でした。')
  })

  it('overlay は game_set や game_clear になるまで出しません。', async () => {
    await dealAndPlay({ statusCode: 200, body: { message: '出しました。' } })

    expect(document.body.textContent).not.toContain('お疲れ様でした。')
  })
})
