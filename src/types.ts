export type Priority = "low" | "medium" | "high";

export type TaskStatus = "open" | "done";

export interface Task {
  id: number;
  title: string;
  priority: Priority;
  status: TaskStatus;
  createdAt: string;
  completedAt?: string;
}

export interface StoreData {
  nextId: number;
  tasks: Task[];
}