# `Node.js`

<h2>Table of contents</h2>

- [What is `Node.js`](#what-is-nodejs)
- [`nvm`](#nvm)
  - [Install `nvm`](#install-nvm)
  - [Install `Node.js`](#install-nodejs)
  - [Check that `Node.js` works](#check-that-nodejs-works)
- [`npm`](#npm)
  - [`package.json`](#packagejson)
  - [`node_modules`](#node_modules)
  - [Common `npm` commands](#common-npm-commands)
    - [`npm install`](#npm-install)
  - [Common `npm` actions](#common-npm-actions)
    - [Install `Node.js` dependencies in the directory](#install-nodejs-dependencies-in-the-directory)

## What is `Node.js`

`Node.js` is a runtime environment that executes `JavaScript` outside of a browser. In this project, it is used to run the frontend development server and build tools.

Docs:

- [Node.js documentation](https://nodejs.org/en/docs)

## `nvm`

`nvm` (Node Version Manager) is a tool for installing and switching between multiple versions of [`Node.js`](#what-is-nodejs).

Docs:

- [`nvm` repository](https://github.com/nvm-sh/nvm)

### Install `nvm`

1. [Check the current shell in the `VS Code Terminal`](./vs-code.md#check-the-current-shell-in-the-vs-code-terminal).
2. Follow the [installation instructions](https://github.com/nvm-sh/nvm#installing-and-updating) for [`macOS`](./operating-system.md#macos) and [`Linux`](./operating-system.md#linux), even if you use [`Windows`](./operating-system.md#windows).
3. To check that `nvm` is installed,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   nvm --version
   ```

   The output should be similar to this:

   ```terminal
   0.40.3
   ```

### Install `Node.js`

1. [Install `nvm`](#install-nvm).

2. To install [`Node.js`](#what-is-nodejs),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   nvm install 25.7.0
   ```

3. The output should be similar to this:

   ```terminal
   Downloading and installing node v25.7.0...
   Now using node v25.7.0 (npm v11.10.1)
   ```

4. To set this version as the default,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   nvm alias default node
   ```

5. [Check that `Node.js` works](#check-that-nodejs-works).

### Check that `Node.js` works

1. To check the `Node.js` version,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   node --version
   ```

2. The output should be similar to this:

   ```terminal
   v25.7.0
   ```

## `npm`

`npm` is the default package manager for [`Node.js`](#what-is-nodejs).
It installs and manages project dependencies declared in [`package.json`](#packagejson).

It is installed automatically when you install [`Node.js`](#install-nodejs).

Docs:

- [`npm` documentation](https://docs.npmjs.com/)

### `package.json`

`package.json` is a configuration [file](./file-system.md#file) in a [`Node.js`](#what-is-nodejs) project that declares the project's [dependencies](./package-manager.md#dependency), scripts, and metadata.

[`npm`](#npm) reads it to know which packages to install and which commands to run.

### `node_modules`

`node_modules` stores all [`Node.js`](#nodejs) modules installed using [`npm`](#npm) or another package manager for `Node.js`.

This [directory](./file-system.md#directory) is [`.gitignore`](./git.md#gitignore)-d.

### Common `npm` commands

#### `npm install`

This command [installs packages in the specified directory](#install-nodejs-dependencies-in-the-directory).

Executes postinstall hooks.

### Common `npm` actions

- [Install `Node.js` dependencies in the directory](#install-nodejs-dependencies-in-the-directory)

#### Install `Node.js` dependencies in the directory

> [!NOTE]
> See [`npm install`](#npm-install), [`package.json`](#packagejson), [directory](./file-system.md#directory).

1. [Open in `VS Code` the project directory](./vs-code.md#open-the-directory).

2. If the `package.json` is in the [root directory of the repository](./git.md#root-directory-of-the-repository),

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   npm install
   ```

3. If the `package.json` is in a [subdirectory](./file-system.md#subdirectory) of the root directory of the repository,

   run in the `VS Code Terminal`:

   ```
   npm install --prefix <frontend-dir>
   ```

   Example:

   ```
   npm install --prefix frontend
   ```

4. Verify that the output is similar to this:

   ```terminal
   added 143 packages, and audited 144 packages in 3s
   ```

5. [Open the `VS Code Explorer`](./vs-code.md#vs-code-explorer).

6. Verify that there is the `node_modules` directory in the directory where you wanted to install the dependencies.
