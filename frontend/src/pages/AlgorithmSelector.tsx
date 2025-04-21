import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowRight, Mountain, Bug, GitBranch, Code, Loader2 } from "lucide-react"
import DefaultLayout from "@/layouts/default"
import { useScheduleStore, Algorithm } from "@/stores/models"
import { useNavigate } from "react-router-dom"
import { useTheme } from "@/theme/theme"
import ApiTester from "@/components/common/tester"
import ApiDocumentation from "@/components/common/documentation"


export default function AlgorithmSelector() {
  const [selectedAlgorithmId, setSelectedAlgorithmId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const setAlgorithm = useScheduleStore(state => state.setAlgorithm)
  const generateSchedules = useScheduleStore(state => state.generateSchedules)
  const navigate = useNavigate()
  const theme = useTheme()

  // Map from component algorithm IDs to store Algorithm type
  const algorithmMapping: Record<string, Algorithm> = {
    "hill_climbing": "Hill Climbing",
    "ant_colony": "Ant Colony",
    "moga_algo": "MOGA",
    "simple_genetic": "Simple Genetic"
  }

  const algorithms = [
    {
      id: "hill_climbing",
      name: "Hill Climbing",
      description: "A mathematical optimization technique that belongs to the family of local search algorithms.",
      icon: Mountain,
    },
    {
      id: "ant_colony",
      name: "Ant Colony",
      description:
        "A probabilistic technique for solving computational problems which can be reduced to finding good paths through graphs.",
      icon: Bug,
    },
    {
      id: "moga_algo",
      name: "MOGA Algorithm",
      description:
        "Multi-Objective Genetic Algorithm that finds a set of solutions which are non-dominated with respect to each other.",
      icon: GitBranch,
    },
    {
      id: "simple_genetic",
      name: "Simple Genetic",
      description:
        "An algorithm inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms.",
      icon: Code,
    },
  ]

  const handleSelect = (algorithmId: string) => {
    setSelectedAlgorithmId(algorithmId)
    // Set the algorithm in the store
    setAlgorithm(algorithmMapping[algorithmId])
  }

  const handleContinue = async () => {
    if (selectedAlgorithmId) {
      console.log(`Selected algorithm: ${algorithmMapping[selectedAlgorithmId]}`)
      
      // Start loading
      setIsLoading(true)
      
      try {
        // Generate schedules using the selected algorithm
        await generateSchedules()
        
        // Navigate to the next page after generating schedules
        navigate("/schedule-generation")
      } catch (error) {
        console.error("Failed to generate schedules:", error)
        // Handle error if needed
      } finally {
        setIsLoading(false)
      }
    }
  }

  return (
    <DefaultLayout>
      <div className="container-fluid mx-auto py-8 px-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold" style={{ color: theme.colors.darkGray }}>Select an Algorithm</h1>
          
          <div className="flex items-center gap-4">
            <ApiTester />
            <Button 
              onClick={handleContinue} 
              disabled={!selectedAlgorithmId || isLoading} 
              className="flex items-center gap-2"
              style={{
                ...theme.components.button.primary.base,
                ...(!selectedAlgorithmId || isLoading ? { opacity: 0.6, cursor: 'not-allowed' } : {})
              }}
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" /> 
                  Processing...
                </>
              ) : (
                <>
                  Continue <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {algorithms.map((algorithm) => (
            <Card
              key={algorithm.id}
              className={`cursor-pointer transition-all duration-200 hover:shadow-md`}
              style={{
                ...theme.components.card,
                ...(selectedAlgorithmId === algorithm.id 
                  ? { 
                      borderColor: theme.colors.darkGray, 
                      borderWidth: '2px',
                      boxShadow: `0 4px 12px rgba(76, 88, 91, 0.2)` 
                    } 
                  : {})
              }}
              onClick={() => handleSelect(algorithm.id)}
            >
              <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                  <algorithm.icon style={{ color: theme.colors.mediumBlue }} className="h-8 w-8" />
                  {selectedAlgorithmId === algorithm.id && (
                    <div 
                      className="h-4 w-4 rounded-full" 
                      style={{ backgroundColor: theme.colors.darkGray }}
                    ></div>
                  )}
                </div>
                <CardTitle className="text-lg" style={{ color: theme.colors.darkGray }}>
                  {algorithm.name}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription style={{ color: theme.colors.mediumBlue }}>
                  {algorithm.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="my-8">
          <ApiDocumentation />
        </div>
      </div>
    </DefaultLayout>
  )
}
