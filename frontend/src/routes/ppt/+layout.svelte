<script lang="ts">
  import { afterNavigate, goto, preloadData } from "$app/navigation"

  function getIndex() {
    const path = location.pathname
    return Number(path.slice(path.lastIndexOf("/") + 1))
  }

  function getNextPage() {
    const path = location.pathname
    return path.slice(0, path.lastIndexOf("/") + 1) + (getIndex() + 1)
  }

  function getLastPage() {
    const path = location.pathname
    return path.slice(0, path.lastIndexOf("/") + 1) + (getIndex() - 1)
  }

  afterNavigate(() => {
    preloadData(getNextPage()).catch(() => {})
    preloadData(getLastPage()).catch(() => {})
  })

  function handleKeyDown(key: string) {
    if (key === "ArrowRight" || key === "ArrowDown") {
      return goto(getNextPage())
    }
    if (key === "ArrowLeft" || key === "ArrowUp") {
      return goto(getLastPage())
    }
  }
</script>

<slot />

<svelte:window on:keydown={({ key }) => handleKeyDown(key)} />
