import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const isWidget = mode === 'widget';
  
  return {
    plugins: [react(), tailwindcss()],
    base: './',
    build: isWidget ? {
      // Widget build config
      lib: {
        entry: resolve(__dirname, 'src/widget.jsx'),
        name: 'MVACalculatorWidget',
        fileName: (format) => `mva-widget.${format}.js`,
        formats: ['umd', 'es'],
      },
      rollupOptions: {
        output: {
          assetFileNames: 'mva-widget[extname]',
        },
      },
      outDir: 'dist-widget',
    } : {
      // Standalone app build
      outDir: 'dist',
    },
  };
});
