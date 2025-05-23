"use client"

import * as React from "react"
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartLegend,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

const chartColors = [
  "hsl(var(--chart-1))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
  "hsl(var(--chart-5))",
]

export function PacketsBarChart({ chartData }: { chartData: Array<String> }) {
  const uniqueDomains = Array.from(new Set(chartData.map((data) => data.domain)))
  const maxDomains = uniqueDomains.slice(0, 5)

  const transformedData = maxDomains.sort((a, b) => b.time - a.time).reduce((acc, domain) => {
    chartData.filter((data) => data.domain === domain).forEach(({ time, visits }) => {
      const existingTimeData = acc.find((item) => item.time === time)
      if (existingTimeData) {
        existingTimeData[domain] = visits
      } else {
        acc.push({ time, [domain]: visits })
      }
    })
    return acc
  }, [] as { time: string; [key: string]: number }[])

  const chartConfig = {
    domains: maxDomains.reduce((acc, domain, index) => {
      acc[domain] = {
        label: domain,
        color: chartColors[index % chartColors.length], 
      }
      return acc
    }, {} as Record<string, { label: string; color: string }>)
  }

  return (
    <Card className="w-full h-full">
      <CardHeader className="flex flex-col items-stretch space-y-0 border-b p-0 sm:flex-row">
        <div className="flex flex-1 flex-col justify-center gap-1 px-6 py-5 sm:py-6">
          <CardTitle>Time-based Visits</CardTitle>
          <CardDescription>Visits per domain over time</CardDescription>
        </div>
      </CardHeader>
      <CardContent className="px-2 sm:p-6">
        <ChartContainer config={chartConfig} className="aspect-auto h-[250px] w-full">
          <BarChart
            data={transformedData}
            margin={{
              left: 12,
              right: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="time"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
              tickFormatter={(value) => value}
            />
            <ChartTooltip content={<ChartTooltipContent hideLabel />} />
            <ChartLegend>
              {maxDomains.map((domain) => (
                <div key={domain} style={{ display: "flex", alignItems: "center", margin: "0 10px" }}>
                  <div
                    style={{
                      width: 20,
                      height: 20,
                      backgroundColor: chartConfig.domains[domain].color,
                      marginRight: "8px",
                    }}
                  />
                  <span>{chartConfig.domains[domain].label}</span>
                </div>
              ))}
            </ChartLegend>
            {maxDomains.map((domain) => (
              <Bar
                key={domain}
                dataKey={domain}
                stackId="time" 
                fill={chartConfig.domains[domain].color}
              />
            ))}
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
