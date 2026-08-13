---
myst:
  html_meta:
    description: "Landscape Debarchive REST API reference."
---

(reference-api-debarchive)=
# Debarchive API

```{raw} html
<style>
  /* Neutralize Furo's TOC-error injection — Scalar may portal content outside
     #scalar-app (modals, tooltips, expanded operations), so this is page-scoped.
     Furo applies two things to .contents: an error :before pseudo, plus a red
     background and color on the element itself. Override both, leave the rest
     of Scalar's styling intact. */
  .contents:before,
  .contents:after { content: none !important; display: none !important; }
  .contents {
    background: transparent !important;
    color: inherit !important;
  }

  /* Bridge Furo's CSS variables into Scalar's namespace. Scalar inherits
     Furo's fonts and colors, including dark-mode toggling via body[data-theme]. */
  #scalar-app {
    --scalar-font: var(--font-stack);
    --scalar-font-code: var(--font-stack--monospace);
    --scalar-color-1: var(--color-foreground-primary);
    --scalar-color-2: var(--color-foreground-muted);
    --scalar-color-3: var(--color-foreground-secondary);
    --scalar-color-accent: var(--color-brand-content);
    --scalar-background-1: var(--color-background-primary);
    --scalar-background-2: var(--color-background-secondary);
    --scalar-background-3: var(--color-background-hover);
    --scalar-background-accent: var(--color-api-background);
    --scalar-border-color: var(--color-background-border);
  }
</style>
<div id="scalar-app"></div>
<script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
<script>
  Scalar.createApiReference('#scalar-app', {
    url: '../../../_static/openapi.yaml',
    theme: 'default',
    servers: [
      { url: 'https://landscape.canonical.com/api/debarchive', description: 'Production' },
    ],
    withDefaultFonts: false,
    showSidebar: false,
    hideClientButton: true,
    hideSearch: true,
    hideModels: true,
    hideTestRequestButton: true,
    agent: {
      disabled: true,
    },
  });
</script>
```
