// Turn plain-text IDs in rendered docs into links: F-xx, R-xx, S-…, and
// "log 0019" / "logs 0004, 0009 and 0014". Only IDs that exist are linked.
// Operates on text between tags; skips text inside <a>, <pre> and headings.
import { byId, url } from "./graph";

export function linkify(html: string, logIds: string[], selfId?: string): string {
  const logs = new Map(logIds.map((id) => [id.slice(0, 4), id]));
  const link = (href: string, text: string) => `<a href="${href}">${text}</a>`;
  const id = (m: string) => {
    if (m === selfId || !byId[m]) return m;
    if (m.startsWith("F-")) return link(url(`findings/${m}/`), m);
    if (m.startsWith("R-")) return link(url(`recommendations/${m}/`), m);
    if (m.startsWith("S-")) return link(url(`trace/#${m}`), m);
    return m;
  };
  const logRef = (n: string) => (logs.has(n) && logs.get(n) !== selfId ? link(url(`log/${logs.get(n)}/`), n) : n);
  const text = (t: string) =>
    t
      .replace(/\b(?:F|R)-\d{2}\b|\bS-[A-Z0-9-]*[A-Z0-9]\b/g, id)
      .replace(/\b(logs?)(\s|-)(\d{4})((?:,?\s(?:and\s)?\d{4})*)/g, (_m, w, sep, first, rest) =>
        `${w}${sep}${logRef(first)}${rest.replace(/\d{4}/g, logRef)}`);

  let skip = 0;
  return html.split(/(<[^>]+>)/g).map((part) => {
    if (part.startsWith("<")) {
      if (/^<(a|pre|h[1-6])[\s>]/i.test(part)) skip++;
      else if (/^<\/(a|pre|h[1-6])>/i.test(part)) skip = Math.max(0, skip - 1);
      return part;
    }
    return skip ? part : text(part);
  }).join("");
}
