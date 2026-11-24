# Agent Skills

Task-triggered playbooks written against the open [Agent Skills standard](https://agentskills.io/specification), which
Claude Code, GitHub Copilot, VS Code, OpenAI Codex CLI, OpenCode, Cursor, Gemini CLI and others implement.

For how this directory is discovered, which client reads which path, the placeholder convention, and how to customize
any of it in your own repository, see [`../README.md`](../README.md). This file is about the skills themselves.

## Available skills

| Skill                                                   | Use when                                                                    |
| ------------------------------------------------------- | --------------------------------------------------------------------------- |
| [`ha-entity-platform`](ha-entity-platform/SKILL.md)     | adding or changing an entity platform or an individual entity               |
| [`ha-service-action`](ha-service-action/SKILL.md)       | adding or changing a service action (`services.yaml` + handler)             |
| [`ha-config-flow`](ha-config-flow/SKILL.md)             | config flow, options, reauth, reconfigure, discovery, subentries            |
| [`ha-coordinator-debug`](ha-coordinator-debug/SKILL.md) | entities unavailable, stale data, setup failures, runtime debugging         |
| [`ha-translations`](ha-translations/SKILL.md)           | `translations/*.json`, `icons.json`, entity and exception translations      |
| [`ha-user-experience`](ha-user-experience/SKILL.md)     | deciding what users see — states, attributes, icons, options, help, actions |
| [`ha-testing`](ha-testing/SKILL.md)                     | writing or fixing tests with `pytest-homeassistant`                         |
| [`ha-quality-review`](ha-quality-review/SKILL.md)       | auditing the integration against the Integration Quality Scale              |
| [`ha-modern-apis`](ha-modern-apis/SKILL.md)             | verifying an API is current, or fixing deprecation warnings                 |
| [`ha-breaking-changes`](ha-breaking-changes/SKILL.md)   | anything that could break existing installs — IDs, entry data, migrations   |
| [`ha-grill`](ha-grill/SKILL.md)                         | interviewing the developer until a change's requirements are settled        |
| [`ha-planning`](ha-planning/SKILL.md)                   | planning a large change or recording an architectural decision              |
| [`ha-issue-triage`](ha-issue-triage/SKILL.md)           | working through the GitHub issue backlog via branch + PR                    |
| [`blueprint-decisions`](blueprint-decisions/SKILL.md)   | recording or superseding an architectural decision, and its index           |
| [`blueprint-lessons`](blueprint-lessons/SKILL.md)       | keeping a lesson from a bug or a repeated correction; project skills        |
| [`ha-release`](ha-release/SKILL.md)                     | cutting a release, commit messages, changelog, release notes                |
| [`ha-marketplace`](ha-marketplace/SKILL.md)             | publishing through the Marketplace/HACS catalog, `hacs.json`, brand images  |
| [`blueprint-tooling`](blueprint-tooling/SKILL.md)       | validation scripts, hook scripts, dependencies, template sync               |
| [`blueprint-update`](blueprint-update/SKILL.md)         | carrying over blueprint changes the template sync cannot deliver            |
| [`blueprint-scaffold`](blueprint-scaffold/SKILL.md)     | turning the fresh template into an integration for one real device          |
| [`blueprint-import`](blueprint-import/SKILL.md)         | migrating an existing custom integration into this repository               |

`blueprint-scaffold` and `blueprint-import` are one-time skills: each ends with a step that removes itself once its
job is done. Leaving them in place costs context in every later session.
