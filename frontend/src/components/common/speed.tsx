import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { useTheme } from "@/theme/theme"
import { FastForward, Clock } from "lucide-react"

interface SpeedDialogProps {
  executionTime: number
  isOpen: boolean
  onClose: () => void
}

export default function SpeedDialog({ executionTime, isOpen, onClose }: SpeedDialogProps) {
  const theme = useTheme()
  
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop with blur effect */}
      <div 
        className="absolute inset-0 backdrop-blur-sm bg-black/30"
        onClick={onClose}
      />
      
      {/* Dialog Card */}
      <Card 
        className="relative z-10 w-96 max-w-md shadow-xl animate-in fade-in-50 zoom-in-95"
        style={{ backgroundColor: theme.colors.cream }}
      >
        <CardHeader className="pb-2">
          <div className="flex justify-center mb-4">
            <div 
              className="p-3 rounded-full"
              style={{ backgroundColor: `${theme.colors.mediumBlue}20` }}
            >
              <Clock className="h-8 w-8" style={{ color: theme.colors.mediumBlue }} />
            </div>
          </div>
          <CardTitle className="text-xl font-bold text-center" style={{ color: theme.colors.darkGray }}>
            Processing Complete
          </CardTitle>
        </CardHeader>
        
        <CardContent className="text-center py-4">
          <div className="flex items-center justify-center gap-3 mb-2">
            <FastForward className="h-5 w-5" style={{ color: theme.colors.mediumBlue }} />
            <h3 className="text-2xl font-bold" style={{ color: theme.colors.darkGray }}>
              {executionTime.toFixed(2)}s
            </h3>
          </div>
          <p className="text-sm" style={{ color: theme.colors.mediumBlue }}>
            Execution time for algorithm processing
          </p>
        </CardContent>
        
        <CardFooter className="flex justify-center pt-2 pb-4">
          <Button 
            onClick={onClose}
            className="px-8"
            style={{
              ...theme.components.button.primary.base,
            }}
          >
            OK
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
