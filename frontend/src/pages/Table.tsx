import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { InsideNavbar } from "@/components/common/inside_nav"
import { useTheme } from "@/theme/theme"

export default function TeacherSchedule() {
  const theme = useTheme();

  // Sample schedule data
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

  // Sample class data (you can replace with actual schedule)
  const schedule: Record<string, Record<string, string>> = {
    "8:00 AM - 9:00 AM": {
      Monday: "Math 101 (Room 204) - Dr. Smith",
      Tuesday: "Office Hours - Dr. Smith",
      Wednesday: "Math 101 (Room 204) - Dr. Smith",
      Thursday: "Department Meeting - All Faculty",
      Friday: "Math 101 (Room 204) - Dr. Smith",
    },
    "9:00 AM - 10:00 AM": {
      Monday: "Algebra (Room 210) - Prof. Johnson",
      Tuesday: "Algebra (Room 210) - Prof. Johnson",
      Wednesday: "Prep Time - Prof. Johnson",
      Thursday: "Algebra (Room 210) - Prof. Johnson",
      Friday: "Algebra (Room 210) - Prof. Johnson",
    },
    "10:00 AM - 11:00 AM": {
      Monday: "Calculus (Room 205) - Dr. Williams",
      Tuesday: "Calculus (Room 205) - Dr. Williams",
      Wednesday: "Calculus (Room 205) - Dr. Williams",
      Thursday: "Prep Time - Dr. Williams",
      Friday: "Calculus (Room 205) - Dr. Williams",
    },
    "11:00 AM - 12:00 PM": {
      Monday: "Office Hours - Dr. Williams",
      Tuesday: "Statistics (Room 201) - Prof. Davis",
      Wednesday: "Statistics (Room 201) - Prof. Davis",
      Thursday: "Statistics (Room 201) - Prof. Davis",
      Friday: "Faculty Meeting - All Faculty",
    },
    "12:00 PM - 1:00 PM": {
      Monday: "Lunch Break",
      Tuesday: "Lunch Break",
      Wednesday: "Lunch Break",
      Thursday: "Lunch Break",
      Friday: "Lunch Break",
    },
    "1:00 PM - 2:00 PM": {
      Monday: "Geometry (Room 208) - Ms. Brown",
      Tuesday: "Geometry (Room 208) - Ms. Brown",
      Wednesday: "Geometry (Room 208) - Ms. Brown",
      Thursday: "Geometry (Room 208) - Ms. Brown",
      Friday: "Prep Time - Ms. Brown",
    },
    "2:00 PM - 3:00 PM": {
      Monday: "Math Club - Dr. Smith",
      Tuesday: "Prep Time - Prof. Johnson",
      Wednesday: "Student Advising - Dr. Williams",
      Thursday: "Math Club - Dr. Smith",
      Friday: "Department Meeting - All Faculty",
    },
    "3:00 PM - 4:00 PM": {
      Monday: "Prep Time - Ms. Brown",
      Tuesday: "Student Advising - Prof. Davis",
      Wednesday: "Office Hours - Dr. Smith",
      Thursday: "Prep Time - Prof. Johnson",
      Friday: "Early Dismissal - All Faculty",
    },
  }

  return (
    <div className="flex flex-col w-full h-screen" style={{ backgroundColor: theme.colors.cream }}>
        <InsideNavbar />
     
        <div className="flex flex-col flex-grow overflow-hidden">
          <CardHeader className="flex-shrink-0">
            
          </CardHeader>
          <CardContent className="flex-grow overflow-hidden">
            <div className="rounded-md border h-full flex flex-col" style={{ borderColor: theme.colors.lightBlue }}>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[150px] bg-muted/50">Time</TableHead>
                    {days.map((day) => (
                      <TableHead key={day} className="bg-muted/50 text-center">
                        {day}
                      </TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {timeSlots.map((time) => (
                    <TableRow key={time}>
                      <TableCell className="font-medium bg-muted/20">{time}</TableCell>
                      {days.map((day) => (
                        <TableCell 
                          key={`${day}-${time}`} 
                          className="text-center"
                          style={{ 
                            backgroundColor: time === "12:00 PM - 1:00 PM" ? `${theme.colors.lightBlue}20` : undefined 
                          }}
                        >
                          {schedule[time]?.[day] || "—"}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
          <CardFooter className="flex-shrink-0">
            <p className="text-sm" style={{ color: theme.colors.mediumBlue }}>
              Note: This faculty schedule is subject to change. Office hours are available by appointment. Please contact
              the respective teacher directly to confirm availability outside of scheduled office hours.
            </p>
          </CardFooter>
        </div>
    </div>
  )
}
