import type { Priority, Task } from "./types.js";

const PRIORITY_LABELS: Record<Priority, string> = {
  low: "low",
  medium: "medium",
  high: "high",
};

export function formatTask(task: Task): string {
  const statusMarker = task.status === "done" ? "x" : " ";
  return `${task.id}. [${statusMarker}] (${PRIORITY_LABELS[task.priority]}) ${task.title}`;
}

export function formatTaskCount(count: number): string {
  return count === 1 ? "1 task" : `${count} tasks`;
}