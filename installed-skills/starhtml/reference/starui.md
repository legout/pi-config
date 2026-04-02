# StarUI — Component Reference

StarUI is a Python-first shadcn/ui component library for StarHTML. Components are copied into your project (no npm, no React) and built with Tailwind CSS.

**Install:**
```bash
pip install starui
star init
star add <component-name>
```

**Docs:** https://ui.starhtml.com/ | https://github.com/banditburai/starUI

---

## Quick Reference by Category

### Layout
| Component | Use For |
|-----------|---------|
| [`Card`](#card) | Content containers with header, content, footer |
| [`Separator`](#separator) | Visual dividers |
| [`Skeleton`](#skeleton) | Loading placeholders |

### Interactive
| Component | Use For |
|-----------|---------|
| [`Button`](#button) | Clickable actions with variants |
| [`Switch`](#switch) | Boolean toggles |
| [`Checkbox`](#checkbox) | Multi-select options |
| [`RadioGroup`](#radiogroup) | Single-select options |
| [`Slider`](#slider) | Range selection |
| [`Toggle`](#toggle) | On/off state buttons |
| [`ToggleGroup`](#togglegroup) | Multiple toggle buttons |

### Forms
| Component | Use For |
|-----------|---------|
| [`Input`](#input) | Text inputs, emails, passwords |
| [`Label`](#label) | Form field labels |
| [`Textarea`](#textarea) | Multi-line text |
| [`Select`](#select) | Dropdown selection |
| [`Combobox`](#combobox) | Searchable dropdowns |

### Overlays
| Component | Use For |
|-----------|---------|
| [`Dialog`](#dialog) | Modal dialogs |
| [`AlertDialog`](#alertdialog) | Confirmation dialogs |
| [`Sheet`](#sheet) | Side panels |
| [`Popover`](#popover) | Floating popups |
| [`Tooltip`](#tooltip) | Hover hints |
| [`HoverCard`](#hovercard) | Preview cards on hover |

### Navigation
| Component | Use For |
|-----------|---------|
| [`Tabs`](#tabs) | Tabbed content |
| [`Breadcrumb`](#breadcrumb) | Navigation paths |
| [`Pagination`](#pagination) | Page navigation |
| [`NavigationMenu`](#navigationmenu) | Nav menus |
| [`Menubar`](#menubar) | App menu bars |

### Data Display
| Component | Use For |
|-----------|---------|
| [`Table`](#table) | Data tables |
| [`Badge`](#badge) | Status labels |
| [`Avatar`](#avatar) | User images |
| [`Progress`](#progress) | Progress bars |
| [`Accordion`](#accordion) | Expandable sections |
| [`Calendar`](#calendar) | Date pickers |
| [`DatePicker`](#datepicker) | Date input |

### Feedback
| Component | Use For |
|-----------|---------|
| [`Alert`](#alert) | Important messages |
| [`Toast`](#toast) | Notifications |
| [`Spinner`](#spinner) | Loading indicators |

### Utilities
| Component | Use For |
|-----------|---------|
| [`Command`](#command) | Command palettes |
| [`DropdownMenu`](#dropdownmenu) | Context menus |
| [`ThemeToggle`](#themetoggle) | Light/dark mode |
| [`Typography`](#typography) | Text styles |
| [`CodeBlock`](#codeblock) | Code display |

---

## Component Details

### Button

**Variants:** `default`, `secondary`, `destructive`, `outline`, `ghost`, `link`
**Sizes:** `default`, `sm`, `lg`, `icon`

```python
from components.button import Button
from starhtml import Icon, Div

Div(
    # Variants
    Button("Default"),
    Button("Secondary", variant="secondary"),
    Button("Delete", variant="destructive"),
    Button("Outline", variant="outline"),
    Button("Ghost", variant="ghost"),
    Button("Link", variant="link"),
    
    # Sizes
    Button("Small", size="sm"),
    Button("Default"),
    Button("Large", size="lg"),
    Button(Icon("lucide:check", cls="h-4 w-4"), size="icon", aria_label="Confirm"),
    
    # With icons
    Button(Icon("lucide:mail", cls="h-4 w-4"), "Send Email"),
    Button("Loading...", Icon("lucide:loader", cls="h-4 w-4 animate-spin"), disabled=True),
    
    # Reactive
    Button(
        "Clicks: " + count,
        data_on_click=count.add(1),
    ),
    
    cls="flex flex-wrap gap-2"
)
```

---

### Card

**Subcomponents:** `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardAction`, `CardContent`, `CardFooter`

```python
from components.card import (
    Card, CardHeader, CardTitle, CardDescription,
    CardContent, CardFooter, CardAction
)
from components.button import Button
from components.dropdown_menu import DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem
from starhtml import P, Icon

Card(
    CardHeader(
        CardTitle("Project Status"),
        CardDescription("Track deployment progress"),
        CardAction(
            DropdownMenu(
                DropdownMenuTrigger(
                    Icon("lucide:ellipsis", cls="h-4 w-4"),
                    variant="ghost", size="icon", aria_label="Options"
                ),
                DropdownMenuContent(
                    DropdownMenuItem("Edit"),
                    DropdownMenuItem("Delete"),
                )
            )
        ),
    ),
    CardContent(
        P("Production is running v2.4.1 with zero errors.")
    ),
    CardFooter(
        Button("Deploy"),
        Button("Cancel", variant="outline"),
    ),
    cls="w-full max-w-md"
)
```

---

### Input

**Types:** All HTML input types (`text`, `email`, `password`, `number`, etc.)

```python
from components.input import Input, InputWithLabel
from starhtml import Signal, Div

# Basic
Input(placeholder="Enter text...")

# With label
InputWithLabel(
    label="Email",
    type="email",
    placeholder="you@example.com",
    signal=email_signal,
    helper_text="We'll never share your email"
)

# With validation
Input(
    type="password",
    placeholder="Min 8 characters",
    data_class_invalid=~password_valid,
)

# Reactive binding
Div(
    (name := Signal("name", "")),
    Input(data_bind=name, placeholder="Type your name"),
    P("Hello, " + name),
)
```

---

### Dialog

**Sizes:** `sm`, `md`, `lg`, `xl`, `full`

```python
from components.dialog import (
    Dialog, DialogTrigger, DialogContent, DialogHeader,
    DialogTitle, DialogDescription, DialogFooter, DialogClose
)

# Basic dialog
Dialog(
    DialogTrigger("Open Dialog", variant="outline"),
    DialogContent(
        DialogHeader(
            DialogTitle("Edit Profile"),
            DialogDescription("Update your information"),
        ),
        Div(
            InputWithLabel(label="Name", signal=name),
            InputWithLabel(label="Email", type="email", signal=email),
            cls="space-y-4 py-4"
        ),
        DialogFooter(
            DialogClose("Cancel", variant="outline"),
            DialogClose("Save")
        )
    )
)

# Confirmation dialog
Dialog(
    DialogTrigger("Delete", variant="destructive"),
    DialogContent(
        DialogHeader(
            DialogTitle("Are you sure?"),
            DialogDescription("This action cannot be undone"),
        ),
        DialogFooter(
            DialogClose("Cancel", variant="outline"),
            DialogClose("Delete", variant="destructive")
        )
    )
)

# Size variants
Dialog(
    DialogTrigger("Large Dialog"),
    DialogContent(size="lg", ...),
)
```

---

### Table

```python
from components.table import (
    Table, TableHeader, TableHead, TableBody, TableRow, TableCell,
    TableCaption, TableFooter
)

Table(
    TableCaption("Employee Directory"),
    TableHeader(
        TableRow(
            TableHead("Name"),
            TableHead("Role"),
            TableHead("Status"),
            TableHead("Actions"),
        )
    ),
    TableBody(
        *[
            TableRow(
                TableCell(name, cls="font-medium"),
                TableCell(role),
                TableCell(Badge(status)),
                TableCell(
                    Button("Edit", size="sm", variant="ghost"),
                    Button("Delete", size="sm", variant="ghost"),
                ),
            )
            for name, role, status in employees
        ]
    ),
    TableFooter(
        TableRow(
            TableCell("Total", cls="font-bold"),
            TableCell(len(employees)),
        )
    ),
    cls="w-full"
)
```

---

### Badge

**Variants:** `default`, `secondary`, `destructive`, `outline`

```python
from components.badge import Badge

Badge("Default")
Badge("Secondary", variant="secondary")
Badge("Destructive", variant="destructive")
Badge("Outline", variant="outline")

# Status indicators
Badge("Active", variant="default")
Badge("Pending", variant="secondary")
Badge("Error", variant="destructive")

# With icons
Badge(Icon("lucide:check", cls="h-3 w-3 mr-1"), "Verified")
```

---

### Alert

**Variants:** `default`, `destructive`

```python
from components.alert import Alert, AlertTitle, AlertDescription
from starhtml import Icon

# Default
Alert(
    Icon("lucide:info", cls="h-4 w-4"),
    AlertTitle("Heads up!"),
    AlertDescription("This action will update your profile"),
)

# Destructive
Alert(
    Icon("lucide:alert-circle", cls="h-4 w-4"),
    AlertTitle("Error"),
    AlertDescription("Your session has expired. Please log in again"),
    variant="destructive"
)
```

---

### Tabs

```python
from components.tabs import Tabs, TabsList, TabsTrigger, TabsContent

Tabs(
    TabsList(
        TabsTrigger("account", "Account"),
        TabsTrigger("password", "Password"),
        TabsTrigger("settings", "Settings"),
    ),
    TabsContent("account",
        Card(...),  # Account settings form
    ),
    TabsContent("password",
        Card(...),  # Password change form
    ),
    TabsContent("settings",
        Card(...),  # General settings
    ),
    cls="w-full max-w-md"
)
```

---

### Switch

```python
from components.switch import Switch, SwitchWithLabel
from starhtml import Signal, Div

# Basic
(notifications := Signal("notifications", True))
Switch(signal=notifications)

# With label
Div(
    SwitchWithLabel(
        label="Push Notifications",
        signal=notifications,
        helper_text="Receive alerts on your device"
    ),
    SwitchWithLabel(
        label="Marketing Emails",
        signal=marketing,
        helper_text="Product news and offers"
    ),
    cls="space-y-4"
)
```

---

### Checkbox

```python
from components.checkbox import Checkbox, CheckboxWithLabel
from starhtml import Signal, Div

# Basic
(agree := Signal("agree", False))
Checkbox(signal=agree)

# With label
Div(
    CheckboxWithLabel(
        label="I agree to the terms",
        signal=agree,
        helper_text="By checking this, you accept our ToS"
    ),
    CheckboxWithLabel(
        label="Subscribe to newsletter",
        signal=newsletter,
    ),
    cls="space-y-3"
)
```

---

### Select

```python
from components.select import (
    Select, SelectTrigger, SelectValue,
    SelectContent, SelectItem, SelectLabel, SelectGroup
)

Select(
    SelectTrigger(cls="w-[180px]"),
    SelectValue(placeholder="Select a fruit"),
    SelectContent(
        SelectGroup(
            SelectLabel("Fruits"),
            SelectItem("Apple", "apple"),
            SelectItem("Banana", "banana"),
            SelectItem("Orange", "orange"),
        )
    )
)
```

---

### Progress

```python
from components.progress import Progress
from starhtml import Signal

(progress := Signal("progress", 60))

Div(
    P("Upload progress: " + progress + "%"),
    Progress(value=progress, max=100, cls="w-full"),
)
```

---

### Avatar

```python
from components.avatar import Avatar, AvatarImage, AvatarFallback
from starhtml import Icon

Avatar(
    AvatarImage(src="https://github.com/username.png", alt="User"),
    AvatarFallback(
        Icon("lucide:user", cls="h-4 w-4")
    )
)

# With initials
Avatar(
    AvatarImage(src="..."),
    AvatarFallback("JD"),  # John Doe
)
```

---

### Accordion

```python
from components.accordion import (
    Accordion, AccordionItem, AccordionTrigger, AccordionContent
)

Accordion(
    AccordionItem("item-1",
        AccordionTrigger("What is StarUI?"),
        AccordionContent("A Python-first component library...")
    ),
    AccordionItem("item-2",
        AccordionTrigger("How do I install?"),
        AccordionContent("pip install starui...")
    ),
    AccordionItem("item-3",
        AccordionTrigger("Is it free?"),
        AccordionContent("Yes, MIT licensed...")
    ),
    type="single",  # or "multiple"
    collapsible=True
)
```

---

### Calendar / DatePicker

```python
from components.calendar import Calendar
from components.date_picker import DatePicker

# Calendar
Calendar(
    signal=selected_date,
    on_select=selected_date.set,
)

# DatePicker (combines input + calendar popover)
DatePicker(
    label="Select date",
    signal=selected_date,
    placeholder="Pick a date"
)
```

---

### Command (Command Palette)

```python
from components.command import (
    Command, CommandInput, CommandList, CommandEmpty,
    CommandGroup, CommandItem, CommandShortcut
)

Command(
    CommandInput(placeholder="Type a command or search..."),
    CommandList(
        CommandEmpty("No results found"),
        CommandGroup(
            heading="Suggestions",
            CommandItem("Calendar", shortcut="⌘C"),
            CommandItem("Search", shortcut="⌘S"),
        ),
        CommandGroup(
            heading="Settings",
            CommandItem("Profile"),
            CommandItem("Billing"),
        )
    )
)
```

---

### Dropdown Menu

```python
from components.dropdown_menu import (
    DropdownMenu, DropdownMenuTrigger, DropdownMenuContent,
    DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator,
    DropdownMenuShortcut, DropdownMenuSub, DropdownMenuSubTrigger,
    DropdownMenuSubContent, DropdownMenuRadioGroup, DropdownMenuRadioItem
)

# Basic
DropdownMenu(
    DropdownMenuTrigger(Button("Open", variant="outline")),
    DropdownMenuContent(
        DropdownMenuLabel("My Account"),
        DropdownMenuSeparator(),
        DropdownMenuItem("Profile"),
        DropdownMenuItem("Settings"),
        DropdownMenuSeparator(),
        DropdownMenuItem("Log out"),
    )
)

# With submenu
DropdownMenu(
    DropdownMenuTrigger(Button("Actions")),
    DropdownMenuContent(
        DropdownMenuSub(
            DropdownMenuSubTrigger("Share"),
            DropdownMenuSubContent(
                DropdownMenuItem("Email"),
                DropdownMenuItem("Copy link"),
            )
        )
    )
)
```

---

### Toast

```python
from components.toast import Toast, ToastProvider, ToastAction
from starhtml import Signal, Button

# Provider (add once to your app)
ToastProvider()

# Trigger toast
(toast_msg := Signal("toast_msg", ""))
(is_toast_open := Signal("is_toast_open", False))

Div(
    is_toast_open,
    Button(
        "Show Toast",
        data_on_click=[
            toast_msg.set("File uploaded successfully!"),
            is_toast_open.set(True)
        ]
    ),
    Toast(
        signal=is_toast_open,
        title="Success",
        description=toast_msg,
        ToastAction("Dismiss"),
    )
)
```

---

### Theme Toggle

```python
from components.theme_toggle import ThemeToggle

# Simple toggle
ThemeToggle()

# With custom labels
ThemeToggle(
    light_label="Light mode",
    dark_label="Dark mode"
)
```

---

### Typography

```python
from components.typography import (
    H1, H2, H3, H4, H5, H6,
    P, Blockquote, Code, Pre, Kbd,
    Lead, Large, Small, Muted
)

Div(
    H1("Heading 1"),
    H2("Heading 2"),
    P("Regular paragraph with ", Code("inline code"), "."),
    Blockquote("This is a blockquote"),
    Pre(Code("code block")),
    Lead("Lead text for introductions"),
    Muted("Muted text"),
    cls="prose"
)
```

---

## Tailwind Customization

All StarUI components use Tailwind CSS. Customize with:

```python
# Override with cls prop
Button("Custom", cls="bg-custom-500 hover:bg-custom-600")

# Use Tailwind v4 CSS variables
Card(cls="bg-[var(--my-color)]")

# Responsive classes
Div(cls="w-full md:w-1/2 lg:w-1/3")
```

---

## Best Practices

1. **Import only what you need:**
   ```python
   from components.button import Button
   from components.card import Card, CardHeader, CardContent
   ```

2. **Use signals for reactivity:**
   ```python
   (count := Signal("count", 0))
   Button("Clicks: " + count, data_on_click=count.add(1))
   ```

3. **Compose components:**
   ```python
   def SettingsCard():
       return Card(
           CardHeader(CardTitle("Settings")),
           CardContent(...),
       )
   ```

4. **Follow accessibility:**
   ```python
   Button(Icon(...), size="icon", aria_label="Close dialog")
   ```

5. **Use variants consistently:**
   ```python
   Button("Save")                    # default for primary
   Button("Cancel", variant="outline")  # outline for secondary
   Button("Delete", variant="destructive")  # destructive for danger
   ```
