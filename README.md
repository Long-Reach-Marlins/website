# Long Reach Marlins website

This repository contains the static website source for Long Reach Marlins, Inc. Static assets are under `src/`, and generated pages are written to the ignored `out/` directory.

Shared page markup lives in `templates/base.html`, while page-specific content lives in `templates/pages/`.
Run `py -3 scripts/build_pages.py` after editing a template to build the deployable site under `out/`.
The local server and GitHub Pages workflow run this build automatically.

## Development

Use Node.js 24 and the pnpm version declared in `package.json` for repository formatting and linting tools. Dependency releases are held for seven days before installation. `pnpm install` also configures the tracked pre-commit hook, which normalizes staged lockfile tarball URLs to `https://registry.npmjs.org/`.

```powershell
pnpm install
pnpm check
```

Run `pnpm format` to format authored files. Generated files under `out/` are intentionally excluded from Prettier; update their templates and run `pnpm build` instead.
