import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";

// The research log is the source of truth in ../docs; the site only presents it.
const log = defineCollection({
  loader: glob({ pattern: "0*.md", base: "../docs/research-log" }),
});

export const collections = { log };
