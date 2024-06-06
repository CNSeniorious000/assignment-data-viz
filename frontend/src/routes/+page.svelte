<script lang="ts">
  import type { PageData } from "./$types"

  export let data: PageData
</script>

<div class="grid grid-cols-5 gap-1.5 [&>*]:(grid aspect-1 place-items-center rounded-lg bg-gray-1 py-6 transition) [&>a:hover]:(bg-gray-2)">
  <a class="col-span-2 aspect-2/1 bg-gray-8 text-white font-sans hover:!bg-gray-7" href="https://github.com/CNSeniorious000/assignment-data-viz">Slides 👉</a>
  {#each data.directories as name}
    <a href="/ppt/{name}">{name}</a>
  {/each}
</div>
