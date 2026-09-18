# foundev.github.io

Simply put this my blog, I have used it off and on for many years and I have had periods where I was posting a lot and then periods where there was a lot less. This is where
you can see that progression.

Apologies if some of it seems off or broken, I have gone through many blogging systems over the years.

## How it works

Built with [Hugo](https://gohugo.io) and deployed to GitHub Pages by
[`.github/workflows/hugo.yml`](.github/workflows/hugo.yml). Live at
<https://blog.foundev.pro>.

```
content/posts/   one Markdown file per post, named YYYY-MM-DD-title.md
layouts/         templates (baseof, home list, single post, tags, 404)
static/          files copied verbatim: images under static/assets, CNAME, css
hugo.toml        site config, including the permalink pattern that preserves
                 the URLs Jekyll used to publish
```

## Local preview

```
brew install hugo
hugo server
```

Then open <http://localhost:1313>. `hugo --minify` writes the site to `public/`.

## Writing a post

Add `content/posts/YYYY-MM-DD-my-title.md`. The date and URL slug come from the
filename, so `content/posts/2026-09-18-hello.md` becomes
`/2026/09/18/hello.html`, matching the old Jekyll URLs. A `date:` key in front
matter is ignored on purpose: the filename wins (see `[frontmatter]` in
`hugo.toml`), which is what keeps the slug free of the date.

```
---
title: 'Hello there'
tags: [cassandra]
---

Body text.
```

Notes:

- Posts almost always start with their own `<h1>` or `# Heading`, and that is the
  heading you see on the page. The `title:` in front matter is what shows up in
  the post list, feeds and `<title>`.
- Raw HTML in posts is allowed (`unsafe = true`); older posts are full of it.
- Straight quotes, dashes and ellipses are converted to typographic ones
  (`&ldquo;`, `&rsquo;`, `&ndash;`) the way kramdown did it on Jekyll.
- Gists are plain `<script src="https://gist.github.com/....js"></script>` tags,
  since Hugo has no `{% gist %}` tag.
- Legacy `.aspx` redirects from the old DataStax blog live in
  `static/blogs/rssvihla/archive/` as plain redirect pages.

## History

Started on Community Server/WordPress, migrated to Jekyll on GitHub Pages, and
converted to Hugo in September 2026. The last Jekyll state of the repo is commit
`eee5e23` if you ever need to compare.
