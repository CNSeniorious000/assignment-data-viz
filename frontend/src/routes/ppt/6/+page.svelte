<script lang="ts">
  import Pie from "$components/Pie.svelte"
  import { flags as data } from "$output/flags.json"
</script>

<Pie title="违规分类" {data} />
