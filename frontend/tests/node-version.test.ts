import { describe, expect, it } from 'vitest'
import dockerfile from '../Dockerfile?raw'
import packageJson from '../package.json?raw'

// Active LTS の Node.js です。
// CI と GitHub Pages の CD は setup-node の node-version-file で package.json の engines.node を読むので、 package.json と Dockerfile をそろえます。
const NODE_MAJOR = '26'

describe('Node.js のバージョン', () => {
  it('package.json の engines.node は Active LTS の Node.js です', () => {
    const { engines } = JSON.parse(packageJson) as { engines?: { node?: string } }
    expect(engines?.node).toBe(`^${NODE_MAJOR}`)
  })

  it('Docker のイメージは Active LTS の Node.js です', () => {
    expect(dockerfile).toMatch(new RegExp(`^FROM node:${NODE_MAJOR}-slim$`, 'm'))
  })
})
