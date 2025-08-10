import { defineConfig } from 'astro/config';
import netlify from '@astrojs/netlify';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  output: 'static',
  adapter: netlify(),
  site: 'https://ki-iro.co.jp',
  integrations: [
    react(),
    sitemap(),
  ],
  markdown: {
    shikiConfig: {
      theme: 'dracula',
    },
  },
});
