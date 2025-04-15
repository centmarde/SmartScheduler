import * as React from "react"
import { cn } from "@/lib/utils"
import { useTheme } from "@/theme/theme"


const Table = React.forwardRef<
  HTMLTableElement,
  React.HTMLAttributes<HTMLTableElement>
>(({ className, ...props }, ref) => {
  const theme = useTheme();
  
  return (
    <div className="w-full h-full">
      <div className="relative w-full h-full overflow-hidden">
        <table
          ref={ref}
          className={cn("w-full h-full caption-bottom text-sm", className)}
          style={{ color: theme.colors.darkGray }}
          {...props}
        />
      </div>
    </div>
  );
})
Table.displayName = "Table"

const TableHeader = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => {
  const theme = useTheme();
  return (
    <thead 
      ref={ref} 
      className={cn("[&_tr]:border-b", className)} 
      style={{ 
        borderColor: theme.colors.lightBlue,
        backgroundColor: `${theme.colors.cream}40` 
      }}
      {...props} 
    />
  )
})
TableHeader.displayName = "TableHeader"

const TableBody = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <tbody
    ref={ref}
    className={cn("[&_tr:last-child]:border-0", className)}
    {...props}
  />
))
TableBody.displayName = "TableBody"

const TableFooter = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => {
  const theme = useTheme();
  return (
    <tfoot
      ref={ref}
      className={cn(
        "border-t font-medium [&>tr]:last:border-b-0",
        className
      )}
      style={{ 
        borderColor: theme.colors.mediumBlue,
        backgroundColor: `${theme.colors.cream}80` // Adding transparency
      }}
      {...props}
    />
  )
})
TableFooter.displayName = "TableFooter"

const TableRow = React.forwardRef<
  HTMLTableRowElement,
  React.HTMLAttributes<HTMLTableRowElement>
>(({ className, ...props }, ref) => {
  const theme = useTheme();
  return (
    <tr
      ref={ref}
      className={cn(
        "border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",
        className
      )}
      style={{ 
        borderColor: theme.colors.lightBlue,
        minHeight: '3rem'
      }}
      onMouseOver={(e) => {
        e.currentTarget.style.backgroundColor = `${theme.colors.cream}50`;
      }}
      onMouseOut={(e) => {
        e.currentTarget.style.backgroundColor = '';
      }}
      {...props}
    />
  )
})
TableRow.displayName = "TableRow"

const TableHead = React.forwardRef<
  HTMLTableCellElement,
  React.ThHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => {
  const theme = useTheme();
  return (
    <th
      ref={ref}
      className={cn(
        "h-16 px-2 text-left align-middle font-medium [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        className
      )}
      style={{ 
        color: theme.colors.darkGray,
        backgroundColor: className?.includes("bg-muted") ? `${theme.colors.cream}70` : undefined
      }}
      {...props}
    />
  )
})
TableHead.displayName = "TableHead"

const TableCell = React.forwardRef<
  HTMLTableCellElement,
  React.TdHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => {
  const theme = useTheme();
  return (
    <td
      ref={ref}
      className={cn(
        "py-5 px-2 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        className
      )}
      style={{ 
        color: theme.colors.darkGray,
        backgroundColor: className?.includes("bg-muted") ? `${theme.colors.cream}30` : undefined
      }}
      {...props}
    />
  )
})
TableCell.displayName = "TableCell"

const TableCaption = React.forwardRef<
  HTMLTableCaptionElement,
  React.HTMLAttributes<HTMLTableCaptionElement>
>(({ className, ...props }, ref) => {
  const theme = useTheme();
  return (
    <caption
      ref={ref}
      className={cn("mt-4 text-sm", className)}
      style={{ color: theme.colors.mediumBlue }}
      {...props}
    />
  )
})
TableCaption.displayName = "TableCaption"

export {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  TableCell,
  TableCaption,
}
