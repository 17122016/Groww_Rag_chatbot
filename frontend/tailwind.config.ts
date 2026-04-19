import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0f1114",
        foreground: "#ffffff",
        growwGreen: {
          DEFAULT: "#00d09c",
          dark: "#00b386",
        },
        cardBg: "#1c1f24",
        border: "#2e3238",
      },
    },
  },
  plugins: [],
} satisfies Config;
