# Teacher Dashboard UI Mockup

This document describes the visual layout and functionality of the enhanced teacher dashboard.

## Dashboard Layout

### Header Section
```
┌─────────────────────────────────────────────────────────────────┐
│  Teacher Attendance Dashboard                        [Logout]   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Welcome, Dr. John Smith!                  [Edit Profile]       │
└─────────────────────────────────────────────────────────────────┘
```

### Statistics Cards
```
┌──────────────┐  ┌──────────────┐  ┌─────────────────────────┐
│ Teacher ID   │  │ Total Courses│  │ Email                   │
│     1        │  │      3       │  │ john.smith@school.edu   │
└──────────────┘  └──────────────┘  └─────────────────────────┘
```

### Course List Section

```
┌─────────────────────────────────────────────────────────────────┐
│  Courses You Teach                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Mathematics 101  [Session Active]                             │
│  Section: A | Year: 1                                          │
│  Classes Taken: Room 101, Room 102                             │
│  [Edit Course Info]                                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ [Show QR Code]  [Stop Attendance Session]              │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Physics 201                                                   │
│  Section: B | Year: 2                                          │
│  Classes Taken: Lab 5                                          │
│  [Edit Course Info]                                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ [Start Attendance Session]                              │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Profile Edit Modal

When clicking "Edit Profile", a modal appears:

```
┌─────────────────────────────────────────────────────────────┐
│  Edit Profile                                           ✕   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Teacher Name:                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Dr. John Smith                                        │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Email:                                                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ john.smith@school.edu                                 │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Teacher Code (optional):                                   │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ TS001                                                 │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│            [Save Changes]  [Cancel]                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Course Edit Inline Form

When clicking "Edit Course Info", an inline form appears below the course:

```
┌─────────────────────────────────────────────────────────────────┐
│  Mathematics 101                                                │
│  Section: A | Year: 1                                          │
│  Classes Taken: Room 101, Room 102                             │
│  [Edit Course Info]                                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Edit Mathematics 101                                     │  │
│  │                                                          │  │
│  │ Section:                                                 │  │
│  │ ┌──────────────────┐                                    │  │
│  │ │ A                │                                    │  │
│  │ └──────────────────┘                                    │  │
│  │                                                          │  │
│  │ Year:                                                    │  │
│  │ ┌──────────────────┐                                    │  │
│  │ │ 1                │                                    │  │
│  │ └──────────────────┘                                    │  │
│  │                                                          │  │
│  │ Classes Taken:                                           │  │
│  │ ┌──────────────────────────────────────────────────┐   │  │
│  │ │ Room 101, Room 102                                │   │  │
│  │ │                                                    │   │  │
│  │ └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │ [Save Changes]  [Cancel]                                │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Color Scheme

The UI uses a consistent maroon color scheme:

- **Primary Maroon**: `#800020` - Main buttons, headers, active badges
- **Light Maroon**: `#A0324B` - Edit buttons, hover states
- **Salmon**: `#FA8072` - QR code buttons, secondary actions
- **Stop Red**: `#C0392B` - Stop session buttons
- **Light Gray**: `#F5F5F5`, `#FAFAFA` - Backgrounds, form areas
- **White**: `#FFFFFF` - Cards, modals, input fields

## Button Styles

### Primary Action (Maroon - #800020)
- Start Attendance Session
- Save Changes
- Hover: Darker maroon (#600018)

### Edit Action (Light Maroon - #A0324B)
- Edit Profile
- Edit Course Info
- Hover: Darker (#8B2A3F)

### Secondary Action (Salmon - #FA8072)
- Show QR Code
- Hover: Darker salmon (#E8735F)

### Danger Action (Red - #C0392B)
- Stop Attendance Session
- Hover: Darker red (#A93226)

### Cancel Action (Gray - #95a5a6)
- Cancel buttons
- Hover: Darker gray (#7f8c8d)

## Interactive Features

### Profile Edit
1. Click "Edit Profile" button
2. Modal slides in with overlay
3. Form pre-filled with current values
4. Real-time validation
5. Success message on save
6. Display updates immediately

### Course Edit
1. Click "Edit Course Info" button
2. Inline form expands below course card
3. Form pre-filled with current values
4. Real-time validation
5. Page reloads on successful save
6. Cancel collapses the form

### Session Management
1. Start session creates attendance session
2. QR code can be displayed/hidden
3. Stop session ends attendance tracking
4. Active badge shows session status

## User Flow Examples

### Update Profile
```
1. Teacher logs in → Dashboard loads
2. Click "Edit Profile" → Modal opens
3. Change name to "Dr. Jane Smith"
4. Click "Save Changes"
5. API call to /api/teachers/update_profile/
6. Success: Display name updates, modal closes
7. Error: Alert shown, modal stays open
```

### Update Course Section
```
1. Teacher views courses
2. Click "Edit Course Info" on Physics 201
3. Inline form appears
4. Change section from "B" to "C"
5. Change year from 2 to 3
6. Click "Save Changes"
7. API call to /api/taught-courses/2/teacher-update/
8. Success: Page reloads with updated info
9. Error: Alert shown, form stays visible
```

### Start Attendance Session
```
1. Teacher views courses without active session
2. Click "Start Attendance Session" for Math 101
3. Confirm dialog appears
4. Click OK
5. API call to /api/attendance-sessions/
6. Success: Page reloads, session controls appear
7. QR code can now be displayed
8. "Session Active" badge shown
```

## Responsive Design

The UI is responsive and works on different screen sizes:
- Desktop: Full layout with side-by-side cards
- Tablet: Stacked cards, full-width modals
- Mobile: Single column, touch-friendly buttons

## Accessibility

- Semantic HTML structure
- Proper form labels
- Keyboard navigation support
- Clear error messages
- Color contrast meets WCAG standards
- Focus indicators on interactive elements

## Security Features

- CSRF token included in all POST requests
- JWT authentication required
- Authorization checks on server side
- Input validation on client and server
- XSS protection through proper escaping
