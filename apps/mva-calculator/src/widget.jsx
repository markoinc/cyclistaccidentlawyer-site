/**
 * MVA Calculator Widget Export
 * 
 * Usage:
 * 1. Include the built widget.js and widget.css files
 * 2. Call MVACalculatorWidget.init('#container-id', options)
 * 
 * Options:
 * - embedded: true (uses minimal styling)
 * - defaultState: 'CA' (default state selection)
 * - defaultBudget: 10000
 * - defaultOfferType: 'lead' | 'transfer' | 'case'
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import MVACalculator from './components/MVACalculator';
import './index.css';

const MVACalculatorWidget = {
  init(selector, options = {}) {
    const container = typeof selector === 'string' 
      ? document.querySelector(selector) 
      : selector;

    if (!container) {
      console.error('[MVA Widget] Container not found:', selector);
      return null;
    }

    const root = ReactDOM.createRoot(container);
    root.render(
      <React.StrictMode>
        <MVACalculator embedded={options.embedded ?? true} {...options} />
      </React.StrictMode>
    );

    return {
      destroy() {
        root.unmount();
      }
    };
  }
};

// Export for ESM and UMD
export { MVACalculator, MVACalculatorWidget };
export default MVACalculatorWidget;

// Auto-attach to window for script tag usage
if (typeof window !== 'undefined') {
  window.MVACalculatorWidget = MVACalculatorWidget;
}
