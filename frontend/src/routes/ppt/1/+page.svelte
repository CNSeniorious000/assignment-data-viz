<script lang="ts">
  import Bar from "$components/Bar.svelte"
  import { messages_token } from "$output/distributions.json"
</script>

<Bar title="每轮对话总 token 数" data={messages_token} />
