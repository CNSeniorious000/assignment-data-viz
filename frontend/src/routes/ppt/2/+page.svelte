<script lang="ts">
  import Bar from "$components/Bar.svelte"
  import { response_token } from "$output/distributions.json"
</script>

<Bar title="每轮对话响应 token 数" data={response_token} />
