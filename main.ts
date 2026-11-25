// THE WORLD — Wednesday 25 November 2026 front page.
// Deterministic: copies the pre-rendered assets/entry.png to /output/entry.png.
// No network, no randomness, no timestamps — every run writes identical bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "assets", "entry.png");
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
