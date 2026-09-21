import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Frontmatter is a data contract, not a convention: a typo in a key name is a
// build failure here rather than a silently missing date on a live page.
const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    // Shown in listings, <meta name="description">, and the RSS item. Required,
    // because the fallback is Astro guessing from the first paragraph.
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    // Drafts build locally but are dropped from every production listing, the
    // sitemap and the feed. See `publishedPosts()` in src/lib/content.ts.
    draft: z.boolean().default(false),
  }),
});

const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    // Sort key for the projects index. A range ("2021–2022") is fine as a
    // display string; `year` is the number the sort uses.
    year: z.number(),
    period: z.string().optional(),
    status: z.enum(['active', 'complete', 'archived', 'paused']).default('complete'),
    tags: z.array(z.string()).default([]),
    repo: z.string().url().optional(),
    url: z.string().url().optional(),
    // Featured projects appear on the home page, in `order` then `year` order.
    featured: z.boolean().default(false),
    order: z.number().default(100),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog, projects };
