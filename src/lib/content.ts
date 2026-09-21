import { getCollection, type CollectionEntry } from 'astro:content';

/** A draft is visible while writing it and invisible once the site is built.
 *
 * ⚠️ Every list of posts must come through here, never `getCollection('blog')`
 * directly — the feed, the sitemap and the listings each filtered drafts
 * separately in the first cut, which is three chances to publish one early.
 * `tests/content.test.mjs` fails the build if a draft reaches `dist/`. */
const visible = (entry: { data: { draft: boolean } }) =>
  import.meta.env.DEV || !entry.data.draft;

export async function publishedPosts(): Promise<CollectionEntry<'blog'>[]> {
  const posts = await getCollection('blog', visible);
  return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export async function publishedProjects(): Promise<CollectionEntry<'projects'>[]> {
  const projects = await getCollection('projects', visible);
  return projects.sort(
    (a, b) => a.data.order - b.data.order || b.data.year - a.data.year,
  );
}

export async function featuredProjects(): Promise<CollectionEntry<'projects'>[]> {
  return (await publishedProjects()).filter((p) => p.data.featured);
}
