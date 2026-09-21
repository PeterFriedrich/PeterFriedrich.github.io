// Site-wide constants. Everything user-facing that appears in more than one
// place lives here so a change lands once.
export const SITE_TITLE = 'Peter Friedrich';
export const SITE_TAGLINE = 'Machine learning and data science';
export const SITE_DESCRIPTION =
  'Data science and machine learning projects, and writing about the parts that are hard to get right.';
export const AUTHOR = 'Peter Friedrich';

export const NAV = [
  { href: '/', label: 'Home' },
  { href: '/projects', label: 'Projects' },
  { href: '/blog', label: 'Writing' },
  { href: '/about', label: 'About' },
] as const;

export const SOCIAL = [
  { href: 'https://github.com/PeterFriedrich', label: 'GitHub' },
  { href: 'https://www.linkedin.com/in/peter-friedrich-a8b56810b/', label: 'LinkedIn' },
  { href: 'https://www.kaggle.com/peterfriedrich1', label: 'Kaggle' },
] as const;
