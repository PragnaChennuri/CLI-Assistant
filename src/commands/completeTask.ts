import type { StoreData, Task } from "../types.js";

export function completeTask(store: StoreData, id: number): Task {
  const task = store.tasks.find((candidate) => candidate.id === id);
  if (!task) {
    throw new Error(`Task ${id} was not found.`);
  }

  task.status = "done";
  task.completedAt = new Date().toISOString();
  return task;
}