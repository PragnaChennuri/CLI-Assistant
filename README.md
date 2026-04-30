# CLI Assistant

CLI Assistant is a small TypeScript command-line app for tracking personal tasks from the terminal. It keeps data in a local JSON file, so it is easy to run, explain, and demo as a code sample.

## Features

- Add tasks with a priority
- List open or completed tasks
- Mark tasks as done
- Remove tasks you no longer need
- Show a quick stats summary

## Getting Started

```bash
npm install
npm run build
npm start -- help
```

## Commands

```bash
npm start -- add --priority high "Finish MLH application"
npm start -- list
npm start -- done 1
npm start -- remove 1
npm start -- stats
```
