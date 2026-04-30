import type { StoreData } from "../types.js";

export function removeTask(store: StoreData, id: number): boolean {
  const index = store.tasks.findIndex((candidate) => candidate.id === id);
  if (index === -1) {
    return false;
  }

  store.tasks.splice(index, 1);
  return true;
}