const js = require("@eslint/js");
const globals = require("globals");

module.exports = [
  js.configs.recommended,
  {
    files: ["src/js/**/*.js"],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: "script",
      globals: globals.browser,
    },
    rules: {
      eqeqeq: ["error", "always"],
      "no-console": "off",
      "no-redeclare": ["error", { builtinGlobals: false }],
      "no-restricted-globals": [
        "error",
        "exports",
        "module",
        "process",
        "require",
        "__dirname",
        "__filename",
      ],
      "no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_", caughtErrorsIgnorePattern: "^_" },
      ],
      "no-var": "warn",
      "prefer-const": "warn",
    },
  },
  {
    files: ["eslint.config.js", "scripts/**/*.js", "tests/**/*.js"],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: "commonjs",
      globals: globals.node,
    },
  },
  {
    ignores: ["node_modules/**", "out/**", "src/*.html"],
  },
];
