<script lang="ts">
  import Bar from "$components/Bar.svelte";
  import { conversation_length } from "$output/distributions.json";
</script>

<Bar title="对话消息条数" data={conversation_length} />
