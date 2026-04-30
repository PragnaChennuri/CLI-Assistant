import { formatTask } from "../format.js";
import type { StoreData } from "../types.js";

export function listTasks(store: StoreData, options?: { showCompleted?: boolean }): string {
  const showCompleted = options?.showCompleted ?? false;
  const visibleTasks = store.tasks.filter((task) => (showCompleted ? true : task.status !== "done"));

  if (visibleTasks.length === 0) {
    return showCompleted ? "No tasks saved yet." : "No open tasks.";
  }

  const openTasks = visibleTasks.filter((task) => task.status === "open");
  const doneTasks = visibleTasks.filter((task) => task.status === "done");

  const output: string[] = [];

  if (openTasks.length > 0) {
    output.push("Open tasks:");
    output.push(...openTasks.map(formatTask));
  }

  if (showCompleted && doneTasks.length > 0) {
    if (output.length > 0) {
      output.push("");
    }
    output.push("Completed tasks:");
    output.push(...doneTasks.map(formatTask));
  }

  return output.join("\n");
}