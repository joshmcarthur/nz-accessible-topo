import { defineConfig } from "astro/config";

// SITE_BASE lets the same build serve from a sub-path (e.g. GitHub Pages /repo-name/).
export default defineConfig({
  base: process.env.SITE_BASE || "/",
  trailingSlash: "always",
});
