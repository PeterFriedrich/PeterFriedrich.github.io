import rss from '@astrojs/rss';
import { publishedPosts } from '../lib/content.ts';
import { SITE_TITLE, SITE_DESCRIPTION } from '../consts.ts';

// The feed is generated from the same `publishedPosts()` every listing uses,
// so a draft cannot reach subscribers through a filter that was forgotten here.
export async function GET(context) {
  const posts = await publishedPosts();
  return rss({
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/blog/${post.id}/`,
    })),
  });
}
