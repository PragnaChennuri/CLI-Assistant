import { mkdir, readFile, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import type { StoreData } from "./types.js";

const DEFAULT_STORE: StoreData = {
  nextId: 1,
  tasks: [],
};

export function getDataDir(): string {
  return process.env.CLI_ASSISTANT_DATA_DIR ?? join(homedir(), ".cli-assistant");
}

export function getStorePath(): string {
  return join(getDataDir(), "tasks.json");
}

function isStoreData(value: unknown): value is StoreData {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const candidate = value as StoreData;
  return (
    typeof candidate.nextId === "number" &&
    Array.isArray(candidate.tasks) &&
    candidate.tasks.every((task) => typeof task?.id === "number")
  );
}

export async function readStore(): Promise<StoreData> {
  try {
    const raw = await readFile(getStorePath(), "utf8");
    const parsed: unknown = JSON.parse(raw);
    if (isStoreData(parsed)) {
      return parsed;
    }
    return DEFAULT_STORE;
  } catch (error) {
    if (error instanceof Error && "code" in error && (error as NodeJS.ErrnoException).code === "ENOENT") {
      return DEFAULT_STORE;
    }
    throw error;
  }
}

export async function writeStore(store: StoreData): Promise<void> {
  await mkdir(getDataDir(), { recursive: true });
  await writeFile(getStorePath(), `${JSON.stringify(store, null, 2)}\n`, "utf8");
}