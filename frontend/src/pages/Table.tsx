import { useEffect, useState } from "react"
import { CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import DefaultLayout from "@/layouts/default"
import { useTheme } from "@/theme/theme"
import { useResultsStore } from "@/stores/results"
import { Loader2, RefreshCw } from "lucide-react"
import { Alert } from "@/components/common/alert"
import { Button } from "@/components/ui/button"
import { useScheduleStore } from "@/stores/models"
import ApiMetricsZigzag from "@/components/common/api-metrics-zigzag"

export default function TeacherSchedule() {
  const theme = useTheme();
  const { formattedSchedule, loading, error, fetchAllData, scheduleItems } = useResultsStore();
  const [showDebug, setShowDebug] = useState(false);
  const [showApiResponse, setShowApiResponse] = useState(false);
  const generationResult = useScheduleStore(state => state.generationResult);

  // Fetch all data on component mount
  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  // Time slots and days (used for rendering the table)
  const timeSlots = [
    "8:00 AM - 9:00 AM",
    "9:00 AM - 10:00 AM",
    "10:00 AM - 11:00 AM",
    "11:00 AM - 12:00 PM",
    "12:00 PM - 1:00 PM",
    "1:00 PM - 2:00 PM",
    "2:00 PM - 3:00 PM",
    "3:00 PM - 4:00 PM",
  ]

  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

  const handleRefresh = () => {
    fetchAllData();
  };

  // This function will help us see what time slots are available in the raw data
  const getRawTimeSlots = () => {
    if (!scheduleItems || scheduleItems.length === 0) return [];
    return [...new Set(scheduleItems.map(item => item.time_slot))].sort();
  };

  return (
    <DefaultLayout>
      <div className="flex flex-col flex-grow overflow-hidden">
        <CardHeader className="flex-shrink-0 flex justify-between items-center">
          <div>
           
            <div className="flex space-x-2">
              <Button 
                onClick={() => setShowDebug(!showDebug)} 
                variant="ghost" 
                size="sm"
                className="text-xs text-muted-foreground"
              >
                {showDebug ? "Hide Debug" : "Show Debug"}
              </Button>
              <Button 
                onClick={() => setShowApiResponse(!showApiResponse)} 
                variant="ghost" 
                size="sm"
                className="text-xs text-muted-foreground"
              >
                {showApiResponse ? "Hide API Response" : "Show API Response"}
              </Button>
            </div>
          </div>
          <Button 
            onClick={handleRefresh} 
            variant="outline" 
            className="flex items-center gap-2"
            disabled={loading}
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </CardHeader>
        <CardContent className="flex-grow overflow-hidden">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
              <span className="ml-2">Loading schedule...</span>
            </div>
          ) : error ? (
            <Alert 
              variant="error" 
              title="Error Loading Schedule" 
              message={error} 
              dismissible={true}
            />
          ) : (
            <>
              {showDebug && (
                <div className="mb-4 p-4 rounded text-xs overflow-auto max-h-80" style={{ backgroundColor: `${theme.colors.cream}20` }}>
                  <h3 className="font-bold mb-2">Debug Information:</h3>
                  <div className="mb-2">
                    <strong>Raw Time Slots from API:</strong> {getRawTimeSlots().join(', ')}
                  </div>
                  <div className="mb-2">
                    <strong>Display Time Slots:</strong> {timeSlots.join(', ')}
                  </div>
                  <pre>{JSON.stringify({formattedSchedule}, null, 2)}</pre>
                </div>
              )}
              
              {showApiResponse && generationResult && (
                <div className="mb-4 p-4 rounded text-xs overflow-auto max-h-80">
                  <h3 className="font-bold mb-2" style={{ color: theme.colors.darkGray }}>API Generation Response:</h3>
                  <pre style={{ backgroundColor: theme.colors.cream, color: theme.colors.darkGray }} className="p-3 rounded border">{JSON.stringify(generationResult, null, 2)}</pre>
                </div>
              )}
              
              {/* API Metrics above the table */}
              <div className="mb-6">
                <ApiMetricsZigzag 
                  metrics={generationResult?.data?.metrics || generationResult?.metrics}
                  executionTime={generationResult?.data?.execution_time_seconds}
                  count={generationResult?.data?.count}
                  status={generationResult?.status}
                />
              </div>
              
              <div className="rounded-md border h-full flex flex-col overflow-auto" style={{ borderColor: theme.colors.lightBlue }}>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-[150px] sticky left-0 z-20" style={{ backgroundColor: theme.colors.cream, color: theme.colors.darkGray }}>Time</TableHead>
                      {days.map((day) => (
                        <TableHead key={day} className="text-center min-w-[200px]" style={{ backgroundColor: theme.colors.cream, color: theme.colors.darkGray }}>
                          {day}
                        </TableHead>
                      ))}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {timeSlots.map((time) => (
                      <TableRow key={time}>
                        <TableCell className="font-medium sticky left-0 z-10" style={{ backgroundColor: `${theme.colors.cream}70`, color: theme.colors.darkGray }}>{time}</TableCell>
                        {days.map((day) => {
                          const cellData = formattedSchedule[time]?.[day];
                          return (
                            <TableCell 
                              key={`${day}-${time}`} 
                              className="text-center"
                              style={{ 
                                backgroundColor: time === "12:00 PM - 1:00 PM" ? theme.colors.lightBlue : undefined,
                                color: time === "12:00 PM - 1:00 PM" ? theme.colors.darkGray : theme.colors.darkGray
                              }}
                            >
                              <div className="whitespace-pre-wrap">
                                {cellData && cellData.length > 0 ? (
                                  <div className="space-y-2">
                                    {cellData.map((item, index) => (
                                      <div 
                                        key={index} 
                                        className={`${index > 0 ? 'pt-2 border-t border-dashed' : ''}`}
                                        style={{ borderColor: index > 0 ? theme.colors.mediumBlue : undefined }}
                                      >
                                        {item}
                                      </div>
                                    ))}
                                  </div>
                                ) : "—"}
                              </div>
                            </TableCell>
                          );
                        })}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
              
            </>
          )}
        </CardContent>
        <CardFooter className="flex-shrink-0">
          <p className="text-sm" style={{ color: theme.colors.mediumBlue }}>
            Note: This faculty schedule is subject to change. Office hours are available by appointment. Please contact
            the respective teacher directly to confirm availability outside of scheduled office hours.
          </p>
        </CardFooter>
      </div>
    </DefaultLayout>
  )
}
