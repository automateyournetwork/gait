/**
 * Sidebar Configuration for GAIT Documentation
 * 
 * Defines the navigation structure for the documentation site.
 * 
 * Three main sidebars:
 * 1. docsSidebar: User-facing documentation (getting started, guides, CLI reference)
 * 2. architectureSidebar: Technical architecture and implementation details
 * 3. recipesSidebar: Real-world usage patterns and workflows
 * 
 * @see https://docusaurus.io/docs/sidebar
 */

import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  // ============================================================
  // Main Documentation Sidebar
  // ============================================================
  docsSidebar: [
    'intro',
    {
      type: 'category',
      label: '🚀 Getting Started',
      items: [
        'getting-started/installation',
        'getting-started/quickstart',
        'getting-started/first-conversation',
        'getting-started/key-concepts',
      ],
    },
    {
      type: 'category',
      label: '📖 User Guide',
      items: [
        'user-guide/interactive-chat',
        'user-guide/memory-system',
        'user-guide/branching-merging',
        'user-guide/remote-sync',
        'user-guide/provider-setup',
        'user-guide/advanced-workflows',
      ],
    },
    {
      type: 'category',
      label: '📟 CLI Reference',
      items: [
        'cli-reference/commands',
        'cli-reference/chat-commands',
        'cli-reference/environment-variables',
      ],
    },
    {
      type: 'category',
      label: '🐛 Troubleshooting',
      items: [
        'troubleshooting/common-issues',
        'troubleshooting/environment-setup',
      ],
    },
  ],

  // ============================================================
  // Architecture & Internals Sidebar
  // ============================================================
  architectureSidebar: [
    'architecture/overview',
    'architecture/content-addressed-storage',
    'architecture/commit-dag',
    'architecture/memory-reflog',
    'architecture/remote-protocol',
    'architecture/data-schemas',
    'architecture/llm-providers',
  ],

  // ============================================================
  // Recipes & Use Cases Sidebar
  // ============================================================
  recipesSidebar: [
    {
      type: 'category',
      label: '🧪 Recipes',
      items: [
        'recipes/recovering-from-hallucinations',
        'recipes/model-comparison',
        'recipes/knowledge-merging',
        'recipes/collaborative-reasoning',
        'recipes/squashing-conversations',
      ],
    },
  ],
};

export default sidebars;
