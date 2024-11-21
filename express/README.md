# Project Template :: TypeScript

## Commands

```sh
npm init
yarn add express cors winston
yarn add -D typescript jest @types/jest ts-node ts-jest @faker-js/faker nodemon dotenv
npx tsc --init
npx ts-jest config:init
```

## Config files

### package.json

```json
{
    ...
    "scripts": {
        "build": "tsc",
        "main": "tsc && node ./dist/src/main.js",
        "dev": "nodemon src/main.ts",
        "test": "jest",
        "test:watch": "jest --watchAll",
        "docker:compose": "docker-compose up -d"
    }
}
```

### tsconfig.json

```json
{
    ...
    "incremental": true,
    "experimentalDecorators": true,
    "outDir": "./dist",
    "include": [
      "src", "test"
    ]
}
```

### nodemon.json

```json
{
  "watch": ["src/**/*.ts", ".env"],
  "ignore": ["test/**/*.test.ts"],
  "exec": "ts-node -r dotenv/config ./src/main.ts"
}

```

### jest.config.js

```js
/** @type {import('ts-jest').JestConfigWithTsJest} **/
export default {
  preset: "ts-jest",
  testEnvironment: "node",
  testMatch: ['**/*.test.ts']
};
```
