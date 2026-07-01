/**
 * Prefixes an internal path with the site's base path (import.meta.env.BASE_URL).
 * Needed because Astro does not rewrite hardcoded href/src strings when
 * `base` is set in astro.config.mjs (e.g. for GitHub Pages project sites
 * served under /<repo-name>/) — only asset imports get that treatment.
 *
 * Does not assume BASE_URL has (or lacks) a trailing slash — that varies by
 * how `base` is written in astro.config.mjs — so it normalizes both sides
 * before joining to guarantee exactly one "/" between them.
 */
export function withBase(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return base + cleanPath;
}
