/**
 * HomepageFeatures Component
 * 
 * Displays the three core features of GAIT on the homepage:
 * - Undo AI Mistakes
 * - Persistent Memory
 * - Parallel Conversations
 * 
 * This is a reusable component that follows Docusaurus patterns
 * and maintains consistent styling with the rest of the site.
 */

import type {ReactNode} from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

/**
 * Feature item configuration
 * Uses emoji + text format for visual consistency with GAIT docs
 */
type FeatureItem = {
  title: string;
  emoji: string;
  description: ReactNode;
};

const FEATURE_LIST: FeatureItem[] = [
  {
    emoji: '⏪',
    title: 'Undo AI Mistakes',
    description: (
      <>
        AI said something wrong? Just type <code>/undo</code> and go back in time.
        No more contaminated conversations!
      </>
    ),
  },
  {
    emoji: '📌',
    title: 'Persistent Memory',
    description: (
      <>
        Pin important context with <code>/pin</code> so the AI never forgets.
        Your knowledge persists across entire conversations.
      </>
    ),
  },
  {
    emoji: '🌳',
    title: 'Parallel Conversations',
    description: (
      <>
        Create branches to explore different approaches.
        Compare models, test ideas, merge the best results.
      </>
    ),
  },
];

/**
 * Individual feature display component
 */
function Feature({emoji, title, description}: FeatureItem): ReactNode {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <div className={styles.featureEmoji}>{emoji}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

/**
 * Main features section component
 * Renders a responsive grid of GAIT's core features
 */
export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FEATURE_LIST.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
