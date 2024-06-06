import { readdirSync } from "node:fs"
import { resolve } from "node:path"
import type { PageServerLoad } from "./$types"

const directories = readdirSync(resolve(`${process.cwd()}/src/routes/ppt`), { withFileTypes: true }).filter(dirent => dirent.isDirectory()).map(dirent => dirent.name)

export const load = (async () => {
  return { directories }
}) satisfies PageServerLoad

export const prerender = true
