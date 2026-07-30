const childProcess = require("node:child_process");
const fs = require("node:fs");

const LOCKFILE_PATH = "pnpm-lock.yaml";
const PUBLIC_REGISTRY = "https://registry.npmjs.org";
const TARBALL_URL = /(tarball:\s*)(https?:\/\/[^\s,}]+)/g;

function normalizeRegistryUrls(lockfile) {
  return lockfile.replace(TARBALL_URL, (match, prefix, tarball) => {
    const url = new URL(tarball);
    const registryMarker = "/registry/";
    const registryPath = url.pathname.includes(registryMarker)
      ? url.pathname.slice(
          url.pathname.indexOf(registryMarker) + registryMarker.length,
        )
      : url.pathname.replace(/^\//, "");

    return `${prefix}${PUBLIC_REGISTRY}/${registryPath}${url.search}${url.hash}`;
  });
}

function normalizeStagedLockfile({
  execFileSync = childProcess.execFileSync,
  readFileSync = fs.readFileSync,
  writeFileSync = fs.writeFileSync,
} = {}) {
  const stagedLockfile = execFileSync("git", ["show", `:${LOCKFILE_PATH}`], {
    encoding: "utf8",
  });
  const normalizedStagedLockfile = normalizeRegistryUrls(stagedLockfile);

  if (normalizedStagedLockfile === stagedLockfile) {
    return false;
  }

  const objectId = execFileSync("git", ["hash-object", "-w", "--stdin"], {
    encoding: "utf8",
    input: normalizedStagedLockfile,
  }).trim();
  execFileSync("git", [
    "update-index",
    "--cacheinfo",
    `100644,${objectId},${LOCKFILE_PATH}`,
  ]);

  const workingLockfile = readFileSync(LOCKFILE_PATH, "utf8");
  const normalizedWorkingLockfile = normalizeRegistryUrls(workingLockfile);
  if (normalizedWorkingLockfile !== workingLockfile) {
    writeFileSync(LOCKFILE_PATH, normalizedWorkingLockfile);
  }

  return true;
}

module.exports = {
  normalizeRegistryUrls,
  normalizeStagedLockfile,
  PUBLIC_REGISTRY,
};
