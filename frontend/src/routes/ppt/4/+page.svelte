<script lang="ts">
  import Pie from "$components/Pie.svelte"
  import { ARABIC, CHINESE, ENGLISH, JAPANESE, RUSSIAN } from "$output/languages.json"
</script>

<Pie title="语言" data={{ ARABIC, CHINESE, ENGLISH, JAPANESE, RUSSIAN }} />
