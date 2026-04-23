# CLI-Assistant

A lightweight command-line productivity tool to manage local tasks.

## Features

- Create tasks
- Update tasks
- Complete tasks
- Delete tasks
- List tasks (pending/completed/all)
- Local JSON persistence
- Basic productivity stats
- Optional task metadata: `priority`, `due-date`

## Usage

Run commands with Python:

```bash
python /home/runner/work/CLI-Assistant/CLI-Assistant/main.py --storage /path/to/tasks.json add "Write docs" --priority high --due-date 2026-05-01
python /home/runner/work/CLI-Assistant/CLI-Assistant/main.py --storage /path/to/tasks.json list --all
python /home/runner/work/CLI-Assistant/CLI-Assistant/main.py --storage /path/to/tasks.json update 1 --title "Write better docs"
python /home/runner/work/CLI-Assistant/CLI-Assistant/main.py --storage /path/to/tasks.json complete 1
python /home/runner/work/CLI-Assistant/CLI-Assistant/main.py --storage /path/to/tasks.json delete 1
python /home/runner/work/CLI-Assistant/CLI-Assistant/main.py --storage /path/to/tasks.json stats
```

If `--storage` is omitted, tasks are stored in `tasks.json` in the current working directory.

## Testing

```bash
cd /home/runner/work/CLI-Assistant/CLI-Assistant
python -m unittest discover -s tests -v
```
