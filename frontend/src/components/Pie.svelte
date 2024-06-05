<script lang="ts">
  import * as echarts from "echarts"
  import { onMount } from "svelte"

  export let title: string
  export let data: Record<string, number>

  let div: HTMLDivElement

  let width: number
  let height: number

  let chart: echarts.ECharts

  function resize(width: number, height: number) {
    if (chart) {
      chart.resize({ width: width || "auto", height: height || "auto" })
    }
  }

  $: resize(width, height)

  onMount(() => {
    chart = echarts.init(div, null, { width, height })

    chart.setOption({
      title: { text: title },
      tooltip: {
        trigger: "item",
      },
      series: [
        {
          type: "pie",
          radius: ["30%", "70%"],
          avoidLabelOverlap: false,
          padAngle: 4,
          itemStyle: {
            borderRadius: 10,
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 40,
            },
          },
          data: Object.entries(data).map(([key, value]) => ({ value, name: key })),
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
