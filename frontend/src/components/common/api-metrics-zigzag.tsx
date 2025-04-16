"use client"

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Clock, Award, AlertTriangle, BarChart2, Users } from "lucide-react"
import { useTheme } from "@/theme/theme"

// Define the metrics interface to match the actual API response
interface Metrics {
  load_variance?: number;
  section_conflicts?: number;
  suitability?: number;
  teacher_conflicts?: number;
}

interface ApiMetricsProps {
  metrics?: Metrics;
  executionTime?: number;
  count?: number;
  status?: string;
}

export default function ApiMetricsZigzag({ metrics, executionTime, count, status }: ApiMetricsProps) {
  const [animated, setAnimated] = useState(false)
  const theme = useTheme()

  // Transform the API data for the chart
  const chartData = [
    {
      name: "Execution Time",
      value: executionTime ? `${executionTime.toFixed(2)}s` : "0.00s",
      icon: <Clock className="h-4 w-4" />
    },
    { 
      name: "Load Variance", 
      value: metrics?.load_variance !== undefined ? metrics.load_variance.toFixed(2) : "0.00", 
      icon: <BarChart2 className="h-4 w-4" /> 
    },
    { 
      name: "Section Conflicts", 
      value: metrics?.section_conflicts !== undefined ? metrics.section_conflicts : 0, 
      icon: <AlertTriangle className="h-4 w-4" /> 
    },
    { 
      name: "Suitability", 
      value: metrics?.suitability !== undefined ? metrics.suitability : 0, 
      icon: <Award className="h-4 w-4" /> 
    },
    { 
      name: "Teacher Conflicts", 
      value: metrics?.teacher_conflicts !== undefined ? metrics.teacher_conflicts : 0, 
      icon: <Users className="h-4 w-4" /> 
    },
  ]

  // Animation effect
  useEffect(() => {
    const timer = setTimeout(() => setAnimated(true), 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <Card className="w-full mx-auto overflow-hidden border" style={{ borderColor: theme.colors.lightBlue, backgroundColor: `${theme.colors.cream}10` }}>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center text-sm" style={{ color: theme.colors.mediumBlue }}>
            <Badge className="text-xs py-0" style={{ backgroundColor: theme.colors.lightBlue, color: theme.colors.darkGray }}>
              {status || "Success"}
            </Badge>
            {count !== undefined && (
              <span className="ml-2">{count} schedules</span>
            )}
          </div>
          <div className="text-sm font-medium" style={{ color: theme.colors.darkGray }}>
            Schedule Metrics
          </div>
        </div>

        <div className="flex justify-between mb-2 text-xs" style={{ color: theme.colors.mediumBlue }}>
          {chartData.map((item, index) => (
            <div key={index} className="text-center flex flex-col items-center">
              <div className="flex justify-center mb-1">{item.icon}</div>
              <div className="text-lg font-medium" style={{ color: theme.colors.darkGray }}>{item.value}</div>
              <div className="text-xs">{item.name}</div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
