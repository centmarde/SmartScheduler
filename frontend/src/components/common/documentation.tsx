"use client"

import type React from "react"
import { useState } from "react"
import { BookOpen, Calendar, ChevronDown, ChevronRight, Code, Layout, Users } from "lucide-react"
import { useTheme } from "@/theme/theme"

interface EndpointProps {
  method: "GET" | "POST" | "PUT" | "DELETE"
  path: string
  description: string
  expanded?: boolean
}

const ApiEndpoint: React.FC<EndpointProps> = ({ method, path, description, expanded = false }) => {
  const [isExpanded, setIsExpanded] = useState(expanded)
  const theme = useTheme()

  const methodColors = {
    GET: {
      bg: "bg-emerald-100 dark:bg-emerald-900/30",
      text: "text-emerald-700 dark:text-emerald-400",
      border: "border-emerald-200 dark:border-emerald-800/50",
    },
    POST: {
      bg: "bg-blue-100 dark:bg-blue-900/30",
      text: "text-blue-700 dark:text-blue-400",
      border: "border-blue-200 dark:border-blue-800/50",
    },
    PUT: {
      bg: "bg-amber-100 dark:bg-amber-900/30",
      text: "text-amber-700 dark:text-amber-400",
      border: "border-amber-200 dark:border-amber-800/50",
    },
    DELETE: {
      bg: "bg-rose-100 dark:bg-rose-900/30",
      text: "text-rose-700 dark:text-rose-400",
      border: "border-rose-200 dark:border-rose-800/50",
    },
  }

  return (
    <div className="border-b last:border-b-0" style={{ borderColor: theme.colors.lightBlue }}>
      <button
        className="flex w-full items-center gap-3 p-3 transition-colors text-left"
        onClick={() => setIsExpanded(!isExpanded)}
        style={{
          color: theme.colors.darkGray,
         
        }}
      >
        {isExpanded ? (
          <ChevronDown className="h-4 w-4 shrink-0" style={{ color: theme.colors.mediumBlue }} />
        ) : (
          <ChevronRight className="h-4 w-4 shrink-0" style={{ color: theme.colors.mediumBlue }} />
        )}

        <span
          className={`font-mono text-xs font-bold px-2 py-0.5 rounded border ${methodColors[method].bg} ${methodColors[method].text} ${methodColors[method].border}`}
        >
          {method}
        </span>

        <code className="font-mono text-sm flex-1" style={{ color: theme.colors.darkGray }}>{path}</code>
      </button>

      {isExpanded && (
        <div className="pl-10 pr-4 pb-4 pt-1">
          <p className="text-sm" style={{ color: theme.colors.mediumBlue }}>{description}</p>
        </div>
      )}
    </div>
  )
}

const ApiDocumentation: React.FC = () => {
  const [activeTab, setActiveTab] = useState("schedules")
  const theme = useTheme()

  const tabs = [
    { id: "schedules", label: "Schedules", icon: Calendar },
    { id: "teachers", label: "Teachers", icon: Users },
    { id: "subjects", label: "Subjects", icon: BookOpen },
    { id: "sections", label: "Sections", icon: Layout },
  ]

  return (
    <div className="w-full mx-auto container-fluid">
      <div className="rounded-lg overflow-hidden" style={{ 
        backgroundColor: theme.colors.cream,
        border: `1px solid ${theme.colors.lightBlue}`,
        boxShadow: `0 4px 8px rgba(76, 88, 91, 0.1)`
      }}>
        {/* Header */}
        <div className="p-4" style={{ borderBottom: `1px solid ${theme.colors.lightBlue}` }}>
          <div className="flex items-center gap-2">
            <Code className="h-5 w-5" style={{ color: theme.colors.mediumBlue }} />
            <h2 className="text-xl font-semibold" style={{ color: theme.colors.darkGray }}>API Documentation</h2>
          </div>
          <p className="text-sm mt-1" style={theme.components.text.small}>
            Explore the available API endpoints for the Smart Scheduler application
          </p>
        </div>

        {/* Tabs */}
        <div className="flex" style={{ borderBottom: `1px solid ${theme.colors.lightBlue}` }}>
          {tabs.map((tab) => {
            const Icon = tab.icon
            const isActive = activeTab === tab.id
            return (
              <button
                key={tab.id}
                className="flex items-center gap-1.5 px-4 py-3 text-sm font-medium border-b-2 transition-colors"
                style={{
                  color: isActive ? theme.colors.darkGray : theme.colors.mediumBlue,
                  borderBottomColor: isActive ? theme.colors.darkGray : 'transparent',
                }}
                onClick={() => setActiveTab(tab.id)}
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </button>
            )
          })}
        </div>

        {/* Content */}
        <div className="overflow-auto max-h-[500px]">
          <div className="p-1">
            {/* Schedules Tab */}
            {activeTab === "schedules" && (
              <div className="py-2">
                <ApiEndpoint
                  method="GET"
                  path="/schedules/"
                  description="Get all schedules with related data including teacher, section, and subject information."
                  expanded
                />
                <ApiEndpoint
                  method="GET"
                  path="/schedules/teacher/:teacher_id"
                  description="Get schedule for a specific teacher with related section and subject information."
                />
                <ApiEndpoint
                  method="GET"
                  path="/schedules/section/:section_id"
                  description="Get schedule for a specific section with related teacher and subject information."
                />
                <ApiEndpoint
                  method="POST"
                  path="/schedules/"
                  description="Create a new schedule entry with day, time slot, and optional teacher, section, and subject IDs."
                />
                <ApiEndpoint
                  method="POST"
                  path="/schedules/generate/moga"
                  description="Generate schedules using the Multi-Objective Genetic Algorithm (MOGA)."
                />
                <ApiEndpoint
                  method="POST"
                  path="/schedules/generate/hill-climbing"
                  description="Generate schedules using the Hill Climbing optimization algorithm."
                />
                <ApiEndpoint
                  method="POST"
                  path="/schedules/generate/simple-genetic"
                  description="Generate schedules using the Simple Genetic Algorithm."
                />
                <ApiEndpoint
                  method="POST"
                  path="/schedules/generate/ant-colony"
                  description="Generate schedules using the Ant Colony Optimization algorithm."
                />
              </div>
            )}

            {/* Teachers Tab */}
            {activeTab === "teachers" && (
              <div className="py-2">
                <ApiEndpoint
                  method="GET"
                  path="/teachers/"
                  description="Get all teachers with their subject information if available."
                  expanded
                />
                <ApiEndpoint
                  method="GET"
                  path="/teachers/:teacher_id"
                  description="Get a specific teacher by ID with their subject information."
                />
                <ApiEndpoint
                  method="GET"
                  path="/teachers/subject/:subject_id"
                  description="Get all teachers teaching a specific subject."
                />
              </div>
            )}

            {/* Subjects Tab */}
            {activeTab === "subjects" && (
              <div className="py-2">
                <ApiEndpoint
                  method="GET"
                  path="/subjects/"
                  description="Get all subjects with basic information and their associated teachers."
                  expanded
                />
                <ApiEndpoint
                  method="GET"
                  path="/subjects/:subject_id"
                  description="Get a specific subject by ID with detailed information including teachers and sections."
                />
                <ApiEndpoint
                  method="GET"
                  path="/subjects/section/:section_id"
                  description="Get all subjects for a specific section."
                />
              </div>
            )}

            {/* Sections Tab */}
            {activeTab === "sections" && (
              <div className="py-2">
                <ApiEndpoint
                  method="GET"
                  path="/sections/"
                  description="Get all sections with their basic information."
                  expanded
                />
                <ApiEndpoint method="GET" path="/sections/:section_id" description="Get a specific section by ID." />
                <ApiEndpoint method="POST" path="/sections/" description="Create a new section with a name." />
                <ApiEndpoint
                  method="PUT"
                  path="/sections/:section_id"
                  description="Update an existing section's information."
                />
                <ApiEndpoint method="DELETE" path="/sections/:section_id" description="Delete a section by ID." />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ApiDocumentation
