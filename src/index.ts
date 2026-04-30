import { addTask } from "./commands/addTask.js";
import { completeTask } from "./commands/completeTask.js";
import { renderHelp } from "./commands/help.js";
import { listTasks } from "./commands/listTasks.js";
import { removeTask } from "./commands/removeTask.js";
import { renderStats } from "./commands/stats.js";
import { readStore, writeStore } from "./storage.js";
import type { Priority } from "./types.js";

type ParsedAddArgs = {
  priority: Priority;
  title: string;
};

function parsePriority(value: string | undefined): Priority {
  if (value === "low" || value === "medium" || value === "high") {
    return value;
  }

  throw new Error("Priority must be low, medium, or high.");
}

function parseAddArgs(args: string[]): ParsedAddArgs {
  const priorityFlagIndex = args.findIndex((value) => value === "--priority" || value === "-p");
  let priority: Priority = "medium";
  const titleParts = [...args];

  if (priorityFlagIndex !== -1) {
    priority = parsePriority(titleParts[priorityFlagIndex + 1]);
    titleParts.splice(priorityFlagIndex, 2);
  }

  const title = titleParts.filter((part) => !part.startsWith("-")).join(" ").trim();
  if (title.length === 0) {
    throw new Error("Add a task title.");
  }

  return { priority, title };
}

function parseId(value: string | undefined): number {
  const id = Number(value);
  if (!Number.isInteger(id) || id <= 0) {
    throw new Error("Provide a valid numeric id.");
  }

  return id;
}

async function main(): Promise<void> {
  const [command = "help", ...args] = process.argv.slice(2);

  try {
    const store = await readStore();

    switch (command) {
      case "add": {
        const { priority, title } = parseAddArgs(args);
        const task = addTask(store, title, priority);
        await writeStore(store);
        console.log(`Added task ${task.id}: ${task.title}`);
        break;
      }
      case "list": {
        console.log(listTasks(store, { showCompleted: args.includes("--all") }));
        break;
      }
      case "done": {
        const task = completeTask(store, parseId(args[0]));
        await writeStore(store);
        console.log(`Completed task ${task.id}: ${task.title}`);
        break;
      }
      case "remove": {
        const removed = removeTask(store, parseId(args[0]));
        if (!removed) {
          throw new Error(`Task ${args[0]} was not found.`);
        }

        await writeStore(store);
        console.log(`Removed task ${args[0]}.`);
        break;
      }
      case "stats": {
        console.log(renderStats(store));
        break;
      }
      case "help":
      default:
        console.log(renderHelp());
        break;
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : "An unexpected error occurred.";
    console.error(message);
    console.error("");
    console.error(renderHelp());
    process.exitCode = 1;
  }
}

void main();