import { defineConfig, splitVendorChunkPlugin } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react(), splitVendorChunkPlugin()],
  server: { port: 1234 },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom', 'framer-motion', '@reduxjs/toolkit', 'react-redux'],
        },
      },
    },
  },
});
