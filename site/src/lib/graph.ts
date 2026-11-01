import graph from "../data/graph.json";

export type Grade = string;
export const { sources, findings, recommendations, changes } = graph as any;

export const byId: Record<string, any> = Object.fromEntries(
  [...sources, ...findings, ...recommendations, ...changes].map((n: any) => [n.id, n]),
);

/** Collapse "A–", "B/C" etc. to the four-step ramp used for colour. */
export function gradeClass(g: Grade): "a" | "b" | "c" | "d" {
  const c = (g || "D").trim()[0].toLowerCase();
  return (["a", "b", "c", "d"].includes(c) ? c : "d") as any;
}

export const gradeText: Record<string, string> = {
  a: "A: replicated or large peer-reviewed studies",
  b: "B: a single peer-reviewed study",
  c: "C: standards, official specs, professional guidance",
  d: "D: practitioner reports or our own unvalidated measurements",
};

export function url(path: string) {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  return `${base}/${path.replace(/^\//, "")}`;
}

export const usedBy = (fid: string) => recommendations.filter((r: any) => r.findings.includes(fid));
export const citedBy = (sid: string) => [
  ...findings.filter((f: any) => f.sources.includes(sid)),
  ...recommendations.filter((r: any) => r.sources.includes(sid)),
];
