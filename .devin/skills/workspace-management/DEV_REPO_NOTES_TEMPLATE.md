# DevRepo NOTES Template

Template for DevRepo NOTES.md. Copy and adapt for your workspace.

Replace all `[placeholder]` values with your workspace-specific content.

## Workspace Constants

- [WORKSPACE_FOLDER]: [current workspace root path]
- [WORKSPACE_FILE]: [WORKSPACE_FOLDER]\main.code-workspace (WORKSPACE mode only, omit if SINGLE-PROJECT or MONOREPO)
- [DEV_REPO_FOLDER]: [WORKSPACE_FOLDER]
- [PRODUCT_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\[product-repo-name]
- [COMPANY_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\Company
- [KNOWLEDGE_FOLDER]: [DEV_REPO_FOLDER]\knowledge
- [KNOWLEDGE_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\knowledge
- [RULES_FOLDER]: [DEV_REPO_FOLDER]\rules
- [RULES_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\rules
- [PRODUCT_DOCS_FOLDER]: [PRODUCT_REPO_FOLDER]\docs
# Release constants (uncomment if using /project-release workflow)
# - [RELEASE_SOPS_FILE]: SOPS.md
# - [RELEASE_SESSIONS_FOLDER]: [DEFAULT_SESSIONS_FOLDER]
# - [RELEASE_NOTES_DIR]: [PRODUCT_DOCS_FOLDER]\ReleaseNotes

Instructions: Replace [product-repo-name] with your product repository folder name. Adjust [COMPANY_REPO_FOLDER] if your company folder is in a different location. All paths should be relative to [WORKSPACE_FOLDER]. [WORKSPACE_FOLDER] is the filesystem path of the workspace root. [WORKSPACE_FILE] is the main.code-workspace file that defines which repos belong to the workspace - repos referenced in it may be physically outside [WORKSPACE_FOLDER] (e.g., ../ProductRepo). Omit [WORKSPACE_FILE] in SINGLE-PROJECT and MONOREPO modes. Release constants compose from existing workspace constants and are used by `/project-release` workflow. `[RELEASE_SOPS_FILE]` is the SOPS filename (`SOPS.md` or `_SOPS.md`). `[RELEASE_SESSIONS_FOLDER]` typically equals `[DEFAULT_SESSIONS_FOLDER]` from `@skills:session-management`. `[RELEASE_NOTES_DIR]` composes from `[PRODUCT_DOCS_FOLDER]` and a `ReleaseNotes` subfolder.

## Sync Sources

Direction definitions:
- Downstream = sync from source to all targets (distribute content to dependent repos)
- Upstream = sync from here back to source (push local changes back to origin)

### Prompt System
- Source: [WORKSPACE_FOLDER]\..\[devsystem-source-name]\DevSystemV*
- Target: [DEV_REPO_FOLDER]\[AGENT_FOLDER]
- Direction: downstream
- Filter: skill categories from [SKILL_CATEGORIES]

### Knowledge
- Source: [KNOWLEDGE_SOURCE_FOLDER]
- Target: [KNOWLEDGE_FOLDER]
- Direction: downstream
- Filter: bundle names from sync policy

### Rules
- Source: [RULES_SOURCE_FOLDER]
- Target: [RULES_FOLDER]
- Direction: downstream
- Filter: file patterns from sync policy

Instructions: Adjust source paths if your DevSystem source or Company folder is in a different location. Set direction to "upstream" for target-to-source sync.

## Project Info

- Project name: [project-name]
- Project goal: [one-sentence-description]
- Workspace mode: WORKSPACE
- Version strategy: SINGLE-VERSION

Instructions: Replace placeholder values with your project information.

## Build/Test Rules

- Build command: [build-command]
- Test command: [test-command]
- Lint command: [lint-command]

Instructions: Define commands for building, testing, and linting your product repo.

## Runtime Environment

**Applies to ProductRepo only.** DevRepo and CompanyRepo are exempt (no buildable source code).

- Runtime: [node|bun|deno|python|rust|zig]
- Version file: [.nvmrc|.python-version|rust-toolchain.toml|build.zig.zon]
- Environment dir: [node_modules|.venv|target|zig-cache]
- Activate command: [n/a for rust/zig|.venv\Scripts\activate for python|fnm use for node]

Instructions: Every ProductRepo must use a local environment. See LOCAL_ENVIRONMENTS.md in workspace-management skill for setup details. Pin runtime version in a committed version file. Gitignore the environment directory.

## Skill Categories

[SKILL_CATEGORIES]
- Development: [list-of-development-skills]
- Infrastructure: [list-of-infrastructure-skills]
- Research: [list-of-research-skills]

Instructions: Register all skills installed in your agent folder. Categories determine which skills are synced to which downstream repos.

## Release Configuration

Optional. Uncomment and configure if using `/project-release` workflow. All paths use workspace constants from `## Workspace Constants` section above. See `_SPEC_RELEASE_PROJECT_WORKFLOW.md [RLSPROJ-SP01]` for full config schema and decision guide.

```
# ## Release Configuration
#
# [RELEASE_CONFIG]
# sops_file: [RELEASE_SOPS_FILE]
# sessions_folder: [RELEASE_SESSIONS_FOLDER]
# release_notes_dir: [RELEASE_NOTES_DIR]
# release_notes_naming: RELEASE_NOTES_v{VERSION}_{DATE}.md
# tag_annotation_template: Release {TAG}: {SUMMARY}
#
# # Single-repo: one [RELEASE_REPO] block
# # Multi-repo: product block first, then dev block(s)
#
# [RELEASE_REPO: product]
# path: [WORKSPACE_FOLDER]
# role: product
# tag_format: [date or semver]
# version_source: [devsystem_folder or pyproject_toml or package_json or none]
# # version_file: [PRODUCT_REPO_FOLDER]\pyproject.toml  # Required when version_source is pyproject_toml or package_json
# post_release_bump: [devsystem_rename or patch_bump or minor_bump or none]
# # binary_build: true     # Uncomment if product has a binary
# # binary_path_pattern: dist/[appname]-{version}-win-x64.exe  # Required when binary_build is true
# # version_gate: true     # Uncomment if version consistency check needed
# # test_command: [command]  # Uncomment if tests not already defined in ## Build/Test Rules
# github_release: true
# # github_release_assets:  # Uncomment if binary assets to attach
# #   - dist/[appname]-{version}-win-x64.exe
#
# # [RELEASE_REPO: dev]    # Uncomment for multi-repo
# # path: [DEV_REPO_FOLDER]
# # role: dev
# # tag_format: [date or semver]
# # version_source: [devsystem_folder or pyproject_toml or package_json or none]
# # post_release_bump: [devsystem_rename or patch_bump or minor_bump or none]
# # test_command: [command]
# # github_release: true
# # github_release_notes: reference  # Dev repo references product release
```

Instructions: Uncomment and replace placeholder values. `test_command` lookup order: (1) `[RELEASE_REPO]` config, (2) `## Build/Test Rules` section above, (3) skip. If `test_command` already defined in Build/Test Rules, omit it from `[RELEASE_REPO]` config.
