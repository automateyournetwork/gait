/**
 * Docusaurus Configuration for GAIT Documentation
 * 
 * This file configures the GAIT documentation website, including:
 * - Site metadata (title, tagline, URLs)
 * - Navigation structure (navbar, sidebars)
 * - Theme settings (dark mode, syntax highlighting)
 * - Deployment configuration (GitHub Pages)
 * - Feature flags (Mermaid diagrams, v4 preview)
 * 
 * @see https://docusaurus.io/docs/configuration
 */

import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  // ============================================================
  // Site Metadata
  // ============================================================
  title: 'GAIT',
  tagline: 'Git for AI Turns - Version Control Your AI Conversations',
  favicon: 'img/favicon.ico',

  // Enable Docusaurus v4 features
  future: {
    v4: true,
  },

  // ============================================================
  // Deployment Configuration
  // ============================================================
  url: 'https://automateyournetwork.github.io',
  // Use /gait/ for production (GitHub Pages subpath), / for local dev
  baseUrl: process.env.NODE_ENV === 'production' ? '/gait/' : '/',

  organizationName: 'automateyournetwork',
  projectName: 'gait',

  // ============================================================
  // Build Configuration
  // ============================================================
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // ============================================================
  // Markdown Features
  // ============================================================
  markdown: {
    mermaid: true,
  },

  themes: ['@docusaurus/theme-mermaid'],

  // ============================================================
  // Presets Configuration
  // ============================================================
  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: 'docs',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/automateyournetwork/gait/tree/main/website/',
          remarkPlugins: [],
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/automateyournetwork/gait/tree/main/website/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  // ============================================================
  // Theme Configuration
  // ============================================================
  themeConfig: {
    image: 'img/gait-social-card.png',
    
    // Dark mode configuration
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    
    // Navigation bar
    navbar: {
      title: 'GAIT',
      logo: {
        alt: 'GAIT Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: '📚 Docs',
        },
        {
          type: 'docSidebar',
          sidebarId: 'architectureSidebar',
          position: 'left',
          label: '🏗️ Architecture',
        },
        {
          type: 'docSidebar',
          sidebarId: 'recipesSidebar',
          position: 'left',
          label: '🧪 Recipes',
        },
        {
          href: 'https://github.com/automateyournetwork/gait',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    
    // Footer configuration
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {
              label: '🚀 Getting Started',
              to: '/intro',
            },
            {
              label: '🧠 Key Concepts',
              to: '/getting-started/key-concepts',
            },
            {
              label: '🏗️ Architecture',
              to: '/architecture/overview',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/automateyournetwork/gait',
            },
            {
              label: 'Issues',
              href: 'https://github.com/automateyournetwork/gait/issues',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: '🧪 Recipes',
              to: '/docs/recipes/recovering-from-hallucinations',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} GAIT Project. Licensed under GPL-3.0-only. Built with Docusaurus.`,
    },
    
    // Syntax highlighting
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'python', 'json'],
    },
    
    // Mermaid diagram themes
    mermaid: {
      theme: {light: 'neutral', dark: 'dark'},
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
