<script lang="ts">
  import Bar from "$components/Bar.svelte"
  import { conversation_length } from "$output/distributions.json"
</script>

<Bar title="每轮对话响应 token 数" data={conversation_length} />
