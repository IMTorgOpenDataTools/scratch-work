# Scratch Work in Js

Different Js projects and implmentations.

## Usage

Choose one of the available `src_*/` + `index_*.html` patterns.  Modify the `vite.config.js` file with the matching `entryPoint` and `sourceFiles` variables.  Then, use the appropriate `npm` commands.

Within the `src_*/` directories, there may be multiple components that can be interchanged in `App.vue`.  For instance, in `src_PiniaORM/components/`  there are three different `Test*.vue` components.  These can be changed in `App.vue` at `import Test from '@/components/Test3.vue'`.



## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```
