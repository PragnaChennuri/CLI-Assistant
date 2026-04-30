import { formatTaskCount } from "../format.js";
import type { StoreData } from "../types.js";

export function renderStats(store: StoreData): string {
  const openCount = store.tasks.filter((task) => task.status === "open").length;
  const doneCount = store.tasks.filter((task) => task.status === "done").length;

  return [
    `Open: ${formatTaskCount(openCount)}`,
    `Done: ${formatTaskCount(doneCount)}`,
    `Total: ${formatTaskCount(store.tasks.length)}`,
  ].join("\n");
}