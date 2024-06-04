<script lang="ts">
  import Pie from "$components/Pie.svelte"
  import { count } from "$output/flags.json"
</script>

<Pie title="合规性" data={{ unflagged: count[0], flagged: count[1] }} />
