<script lang="ts">
  import * as echarts from "echarts"
  import { onMount } from "svelte"
  import { messages_token, total } from "$output/distributions.json"

  let div: HTMLDivElement

  let width: number
  let height: number

  let chart: echarts.ECharts

  function resize(width: number, height: number) {
    if (chart) {
      chart.resize({ width: width || "auto", height: height || "auto" })
    }
  }

  let length = Object.keys(messages_token)
    .map(Number)
    .sort((a, b) => a - b)
    .at(-1)!

  length = Math.min(length, 20000)

  const xs = Array.from({ length }).map((_, i) => i)
  const ys = Array.from({ length }).map((_, i) => messages_token[String(i) as keyof typeof messages_token] ?? 0)

  $: resize(width, height)

  onMount(() => {
    chart = echarts.init(div, null, { width, height })

    chart.setOption({
      title: { text: `Token Count in ${total} chats` },
      toolbox: {
        show: true,
        feature: {
          dataZoom: { yAxisIndex: false },
        },
      },
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "shadow",
        },
      },
      grid: {
        left: "5",
        right: "5",
        bottom: "60",
        containLabel: true,
      },
      dataZoom: [{ type: "slider" }],
      xAxis: [
        {
          type: "category",
          data: xs,
          axisTick: { alignWithLabel: true },
        },
      ],
      yAxis: [
        {
          type: "value",
        },
      ],
      series: [
        {
          type: "bar",
          data: ys,
        },
      ],
    } as echarts.EChartsOption)
  })
</script>

<svelte:window
  on:resize={() => {
    width = div.clientWidth
    height = div.clientHeight
  }}
/>

<div class="m-20 h-3/4 w-3/4">
  <div class="h-full w-full" bind:this={div} bind:clientWidth={width} bind:clientHeight={height} />
</div>
