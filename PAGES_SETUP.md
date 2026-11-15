# Enable the portfolio website

The repository contains a static portfolio at `index.html`. GitHub Actions validates it, stages only that file, and deploys it. The workflow does not publish source files, tests, or internal documentation.

## One-time repository setting

A repository owner must enable GitHub Pages once:

1. Open **DT-09/DT-09 → Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Save the setting.
4. Open **Actions → Deploy engineering fieldbook** and run the workflow manually, or push a later change to `index.html`.
5. Confirm the deployment job succeeds. GitHub displays the published site URL in the Pages settings and deployment summary.

The workflow cannot complete this owner-level setting when the repository's Actions token lacks permission to create a Pages site. That is why a green build is not the same as a published website.

## Deployment boundary

- Source: `index.html`
- Build: no framework build; the page is self-contained.
- Artifact: `_site/index.html` and `.nojekyll` only.
- Validation: unit tests, local links, metadata, accessibility structure, reduced-motion support, inline JavaScript syntax and referenced SVGs.
- Hosting: GitHub Pages.

Do not mark the website as live until the deployment action reports success and the published URL has been opened and checked.
