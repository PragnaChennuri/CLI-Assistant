export function renderHelp(): string {
  return [
    "CLI Assistant",
    "",
    "Usage:",
    "  cli-assistant add --priority <low|medium|high> <title>",
    "  cli-assistant list [--all]",
    "  cli-assistant done <id>",
    "  cli-assistant remove <id>",
    "  cli-assistant stats",
    "",
    "Examples:",
    "  cli-assistant add --priority high Finish MLH application",
    "  cli-assistant list --all",
  ].join("\n");
}