# GAIT Documentation Website 📚

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Quick Start

```bash
# Install dependencies
npm install

# Start local development server
npm start

# Build for production
npm run build

# Serve production build locally
npm run serve
```

## Development Commands

| Command | Description |
|---------|-------------|
| `npm start` | Start dev server with hot reload (polls every 1s) |
| `npm run start:fast` | Start dev server without minification (faster) |
| `npm run build` | Build static site for production |
| `npm run serve` | Serve production build locally |
| `npm run clear` | Clear cache (helpful for debugging) |
| `npm run typecheck` | Run TypeScript type checking |

## Project Structure

```
website/
├── docs/                          # Markdown documentation files
│   ├── intro.md                   # Homepage/welcome
│   ├── getting-started/           # Installation & quickstart
│   ├── user-guide/                # User-facing guides
│   ├── architecture/              # Technical deep-dives
│   ├── recipes/                   # Real-world examples
│   ├── cli-reference/             # Command reference
│   └── troubleshooting/           # Help & debugging
├── blog/                          # Blog posts (optional)
├── src/
│   ├── components/                # Reusable React components
│   │   └── HomepageFeatures/      # Feature highlight component
│   ├── pages/                     # Custom pages (homepage, etc.)
│   │   └── index.tsx              # Main landing page
│   └── css/
│       └── custom.css             # Global styles & theme vars
├── static/                        # Static assets (images, favicons)
├── docusaurus.config.ts           # Site configuration
├── sidebars.ts                    # Navigation structure
├── package.json                   # Dependencies & scripts
└── tsconfig.json                  # TypeScript configuration
```

## Component Architecture

### Reusable Components

All shared components live in `src/components/` and follow these patterns:

- **Single responsibility**: Each component does one thing well
- **TypeScript**: All components use strict TypeScript
- **CSS Modules**: Scoped styles via `*.module.css` files
- **Documentation**: JSDoc comments explain purpose and usage

Example component structure:
```
src/components/HomepageFeatures/
├── index.tsx              # Component logic
└── styles.module.css      # Scoped styles
```

### Creating New Components

```tsx
/**
 * MyComponent - Brief description
 * 
 * Detailed explanation of what this component does
 * and when to use it.
 */

import type {ReactNode} from 'react';
import styles from './styles.module.css';

type MyComponentProps = {
  title: string;
  description: ReactNode;
};

export default function MyComponent({title, description}: MyComponentProps): ReactNode {
  return (
    <div className={styles.container}>
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
}
```

## Documentation Best Practices

### Writing Style

- **Use emojis** to make docs scannable and engaging 🎉
- **ELI5 (Explain Like I'm 5)** - Simple analogies and clear language
- **Real examples** - Show actual command outputs and code
- **Diagrams** - Use Mermaid for visualizations
- **Code blocks** - Always include working, tested examples

### Markdown Features

#### Admonitions (Callouts)

```markdown
:::tip Pro Tip
This is a helpful tip!
:::

:::warning Careful!
This is important to know.
:::

:::info FYI
Additional information.
:::

:::danger Critical
This could break things!
:::
```

#### Mermaid Diagrams

```markdown
\`\`\`mermaid
graph LR
    A[User] --> B[GAIT]
    B --> C[LLM]
    C --> D[Response]
\`\`\`
```

#### Code Tabs

```markdown
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="bash" label="Bash" default>
    \`\`\`bash
    gait init
    \`\`\`
  </TabItem>
  <TabItem value="python" label="Python">
    \`\`\`python
    import gait
    \`\`\`
  </TabItem>
</Tabs>
```

#### Images

```markdown
![Alt text](/img/screenshot.png)
```

#### Internal Links

```markdown
[Link to Getting Started](./getting-started/installation.md)
[Link to Section](#section-heading)
```

## Deployment

### GitHub Pages (Automatic)

The site automatically deploys to GitHub Pages when changes are pushed to `main`:

1. Changes pushed to `website/` or `.github/workflows/deploy-docs.yml`
2. GitHub Actions builds the site (`npm run build`)
3. Artifacts uploaded and deployed to `gh-pages` branch
4. Site live at: https://automateyournetwork.github.io/gait/

### Manual Deployment

```bash
# Using GitHub CLI
GIT_USER=<username> npm run deploy

# Or build and deploy manually
npm run build
# Upload contents of build/ directory to your hosting service
```

### Other Hosting Options

The `build/` directory is a static site that can be hosted on:
- **Vercel**: `vercel --prod`
- **Netlify**: Drag & drop `build/` folder
- **AWS S3**: `aws s3 sync build/ s3://your-bucket/`
- **Cloudflare Pages**: Connect GitHub repo
- **Any static host**: Upload `build/` contents

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
npx kill-port 3000

# Or use a different port
npm start -- --port 3001
```

### Build Errors

```bash
# Clear cache and rebuild
npm run clear
npm run build

# Reinstall dependencies (nuclear option)
rm -rf node_modules package-lock.json
npm install
```

### Broken Links

```bash
# Build checks for broken links automatically
npm run build
# Look for [WARNING] or [ERROR] about broken links in output
```

### Type Errors

```bash
# Run TypeScript type checking
npm run typecheck
```

## Contributing

1. Create a new branch: `git checkout -b docs/my-improvement`
2. Edit markdown files in `docs/` or components in `src/`
3. Test locally: `npm start`
4. Build to ensure no errors: `npm run build`
5. Commit and push: `git push origin docs/my-improvement`
6. Open a pull request

## Resources

- [Docusaurus Documentation](https://docusaurus.io/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Mermaid Diagram Syntax](https://mermaid.js.org/)
- [GAIT Repository](https://github.com/automateyournetwork/gait)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

---

**Questions?** Open an issue at https://github.com/automateyournetwork/gait/issues
