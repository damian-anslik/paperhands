<template>
    <div class="chart-container">
        <apexchart type="candlestick" :options="chartOptions" :series="series" height="100%" width="100%" ref="chart" />
    </div>
</template>

<script>
import controller from '@/controller'
export default {
    // TODO When chart is first loaded, show a message to select a symbol if no activeSymbol is set, or show the chart if activeSymbol is set
    name: "Apex charts",
    computed: {
        activeSymbol() {
            return this.$store.state.activeSymbol
        }
    },
    watch: {
        activeSymbol: function (symbol) {
            if (this.activeSymbol === '') return
            this.updateSeries([])
            this.updateChartOptions({
                title: {
                    text: `${symbol} Chart`
                },
                noData: {
                    text: 'Loading...'
                }
            })
            controller.getHistoricalData(symbol)
                .then(response => {
                    console.log(response.data)
                    const bars = response.data.bars.map(bar => {
                        return {
                            x: new Date(bar.t),
                            y: [bar.o, bar.h, bar.l, bar.c]
                        }
                    })
                    console.log(bars);
                    this.updateSeries([
                        {
                            data: bars
                        }
                    ])
                    this.updateChartOptions({
                        title: {
                            text: `${symbol} Chart`
                        },
                    })
                })
                .catch(error => {
                    console.log(error);
                })
        }
    },
    methods: {
        updateChartOptions(newOptions) {
            this.$refs.chart.updateOptions(newOptions)
        },
        updateSeries(newSeries) {
            this.$refs.chart.updateSeries(newSeries, true)
        },
    },
    data: () => ({
        chartOptions: {
            chart: {
                type: 'candlestick',
                // TODO Toolbar does not show all icons on mobile
                toolbar: {
                    show: true,
                    offsetX: -4,
                    tools: {
                        download: false,
                        selection: true,
                        zoom: true,
                        zoomin: true,
                        zoomout: true,
                        pan: true,
                        reset: true
                    },
                }
            },
            noData: {
                text: 'Select a symbol to view chart',
            },
            grid: {
                borderColor: '#333',
            },
            title: {
                align: 'left'
            },
            xaxis: {
                type: 'datetime',
            },
            yaxis: {
                show: true,
                tooltip: {
                    enabled: true,
                    style: {
                        fontSize: '12px',
                        fontFamily: undefined
                    },
                },
                labels: {
                    formatter: function (val) {
                        return Math.floor(val)
                    }
                }
            },
            tooltip: {
                theme: 'dark'
            }
        },
        series: [],
    }),
};
</script>

<style>
.chart-container {
    padding-block: 1rem;
    width: 100%;
    height: 60vh;
    z-index: -1;
    resize: vertical;
    overflow: hidden;
    background-color: black;
}
</style>