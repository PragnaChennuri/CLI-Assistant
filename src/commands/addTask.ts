import type { Priority, StoreData, Task } from "../types.js";

export function addTask(store: StoreData, title: string, priority: Priority): Task {
  const task: Task = {
    id: store.nextId,
    title,
    priority,
    status: "open",
    createdAt: new Date().toISOString(),
  };

  store.tasks.push(task);
  store.nextId += 1;
  return task;
}