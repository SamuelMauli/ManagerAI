import React from 'react';
import * as SelectPrimitive from '@headlessui/react';
import { Check, ChevronDown } from 'lucide-react';

const Select = SelectPrimitive.Listbox;

const SelectTrigger = React.forwardRef(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Button
    ref={ref}
    className={`flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
    {...props}
  >
    {children}
    <ChevronDown className="h-4 w-4 opacity-50" />
  </SelectPrimitive.Button>
));
SelectTrigger.displayName = "SelectTrigger";

const SelectContent = React.forwardRef(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Options
    ref={ref}
    className={`absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-popover text-popover-foreground shadow-md ${className}`}
    {...props}
  >
    {children}
  </SelectPrimitive.Options>
));
SelectContent.displayName = "SelectContent";

const SelectItem = React.forwardRef(({ className, children, value, ...props }, ref) => (
    <SelectPrimitive.Option
        ref={ref}
        key={value}
        value={value}
        className={({ active }) =>
            `relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none ${active ? 'bg-accent text-accent-foreground' : ''} ${className}`
        }
        {...props}
    >
        {({ selected }) => (
            <>
                {selected ? (
                    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
                        <Check className="h-4 w-4" />
                    </span>
                ) : null}
                <span className="block truncate">{children}</span>
            </>
        )}
    </SelectPrimitive.Option>
));
SelectItem.displayName = "SelectItem";


const SelectValue = ({ children }) => <span className="block truncate">{children || 'Selecione uma opção'}</span>;


export { Select, SelectTrigger, SelectContent, SelectItem, SelectValue };