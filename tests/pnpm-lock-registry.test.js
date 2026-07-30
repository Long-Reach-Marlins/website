const assert = require("node:assert/strict");
const { test } = require("node:test");

const {
  normalizeRegistryUrls,
  normalizeStagedLockfile,
  PUBLIC_REGISTRY,
} = require("../scripts/lib/pnpm-lock-registry.js");

test("normalizes public and proxy tarball URLs to the public npm registry", () => {
  const lockfile = [
    "resolution: {tarball: https://registry.yarnpkg.com/pkg/-/pkg-1.0.0.tgz}",
    "resolution: {tarball: https://feed.example/npm/registry/@scope/pkg/-/pkg-1.0.0.tgz?x=1#hash}",
    "homepage: https://example.com/registry/not-a-tarball",
  ].join("\n");

  assert.equal(
    normalizeRegistryUrls(lockfile),
    [
      `resolution: {tarball: ${PUBLIC_REGISTRY}/pkg/-/pkg-1.0.0.tgz}`,
      `resolution: {tarball: ${PUBLIC_REGISTRY}/@scope/pkg/-/pkg-1.0.0.tgz?x=1#hash}`,
      "homepage: https://example.com/registry/not-a-tarball",
    ].join("\n"),
  );
});

test("updates the staged blob and working lockfile without staging unrelated lockfile edits", () => {
  const stagedLockfile =
    "resolution: {tarball: https://feed.example/npm/registry/pkg/-/pkg-1.0.0.tgz}\n";
  const workingLockfile = `${stagedLockfile}unstaged: true\n`;
  const calls = [];
  let writtenLockfile;
  const execFileSync = (command, args, options = {}) => {
    calls.push({ command, args, options });
    if (args[0] === "show") return stagedLockfile;
    if (args[0] === "hash-object") return "object-id\n";
    return "";
  };

  assert.equal(
    normalizeStagedLockfile({
      execFileSync,
      readFileSync: () => workingLockfile,
      writeFileSync: (file, content) => {
        assert.equal(file, "pnpm-lock.yaml");
        writtenLockfile = content;
      },
    }),
    true,
  );
  assert.equal(
    calls[1].options.input,
    `resolution: {tarball: ${PUBLIC_REGISTRY}/pkg/-/pkg-1.0.0.tgz}\n`,
  );
  assert.deepEqual(calls[2].args, [
    "update-index",
    "--cacheinfo",
    "100644,object-id,pnpm-lock.yaml",
  ]);
  assert.equal(
    writtenLockfile,
    `resolution: {tarball: ${PUBLIC_REGISTRY}/pkg/-/pkg-1.0.0.tgz}\nunstaged: true\n`,
  );
});

test("does not rewrite an already normalized staged lockfile", () => {
  const lockfile = `resolution: {tarball: ${PUBLIC_REGISTRY}/pkg/-/pkg-1.0.0.tgz}\n`;
  let readWorkingFile = false;

  assert.equal(
    normalizeStagedLockfile({
      execFileSync: () => lockfile,
      readFileSync: () => {
        readWorkingFile = true;
      },
    }),
    false,
  );
  assert.equal(readWorkingFile, false);
});
