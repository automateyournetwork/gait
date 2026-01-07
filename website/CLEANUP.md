# Website Cleanup Checklist

This document lists **legacy/unused files** that should be removed from the website directory.

## 🗑️ Files to Remove

### Default Docusaurus Tutorial Content

These are the default Docusaurus tutorial files that are **not referenced** in `sidebars.ts` and serve no purpose for GAIT documentation:

```bash
# Remove tutorial directories
rm -rf docs/tutorial-basics/
rm -rf docs/tutorial-extras/

# Specifically removes:
# - docs/tutorial-basics/create-a-document.md
# - docs/tutorial-basics/create-a-page.md
# - docs/tutorial-basics/deploy-your-site.md
# - docs/tutorial-basics/markdown-features.mdx
# - docs/tutorial-basics/congratulations.md
# - docs/tutorial-basics/create-a-blog-post.md
# - docs/tutorial-extras/translate-your-site.md
# - docs/tutorial-extras/manage-docs-versions.md
```

### Default Blog Posts

These are placeholder blog posts from Docusaurus template, **not actual GAIT content**:

```bash
# Remove default blog posts
rm blog/2019-05-28-first-blog-post.md
rm blog/2019-05-29-long-blog-post.md
rm blog/2021-08-01-mdx-blog-post.mdx
rm -rf blog/2021-08-26-welcome/
```

**Note:** Keep `blog/authors.yml` and `blog/tags.yml` for future blog posts.

## ✅ Why Remove These?

1. **Reduces confusion** - Developers won't accidentally read default Docusaurus docs
2. **Cleaner structure** - Only GAIT-specific content remains
3. **Faster builds** - Fewer files to process
4. **Better search** - Search results won't include irrelevant tutorial content

## 🔍 How to Verify

After removal, check for broken links:

```bash
cd website
npm run build
# Should complete without warnings about missing tutorial files
```

## 📝 Optional: Blog Strategy

If you plan to add a GAIT blog:

1. Keep the `blog/` directory structure
2. Create new posts in format: `YYYY-MM-DD-slug.md`
3. Update `blog/authors.yml` with GAIT contributors
4. Add `blog/tags.yml` with relevant tags (gait, llm, git, etc.)

If **no blog is planned**:

```bash
# Remove blog entirely
rm -rf blog/

# Update docusaurus.config.ts to disable blog
# In presets section, set blog: false
```

---

**Run the cleanup after backing up or committing current state!**
