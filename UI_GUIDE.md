# 🎨 UI Guide

## What You'll See

### Main Interface

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              🛡️ Bengali Hate Speech Classifier             │
│              Enter Bengali text to classify hate speech     │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Enter Text:                                           │ │
│  │ ┌───────────────────────────────────────────────────┐ │ │
│  │ │                                                   │ │ │
│  │ │  এখানে বাংলা টেক্সট লিখুন...                      │ │ │
│  │ │                                                   │ │ │
│  │ │                                                   │ │ │
│  │ └───────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Analyze Text                             │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### After Clicking "Analyze Text"

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              🛡️ Bengali Hate Speech Classifier             │
│              Enter Bengali text to classify hate speech     │
│                                                             │
│  [Text Input Area with your Bengali text]                  │
│                                                             │
│  [Analyze Text Button]                                     │
│                                                             │
│  ⏳ Analyzing...                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Results Display

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              🛡️ Bengali Hate Speech Classifier             │
│              Enter Bengali text to classify hate speech     │
│                                                             │
│  [Text Input Area]                                         │
│  [Analyze Text Button]                                     │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Predicted Class: 0                                    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Confidence Scores:                                        │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Class 0  ████████████████████████░░░░░░  85.23%      │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Class 1  ████░░░░░░░░░░░░░░░░░░░░░░░░░░  10.12%      │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Class 2  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   3.12%      │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Class 3  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   1.53%      │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Color Scheme

- **Background**: Purple gradient (from #667eea to #764ba2)
- **Container**: White with rounded corners and shadow
- **Text**: Dark gray (#333) for headings, medium gray (#555) for labels
- **Buttons**: Purple gradient with hover effects
- **Progress Bars**: Purple gradient fill
- **Scores**: Purple text (#667eea)

## Interactive Elements

### Text Input
- Large textarea with rounded corners
- Border changes to purple on focus
- Placeholder text in Bengali
- Resizable vertically

### Analyze Button
- Full-width purple gradient button
- Lifts up on hover (transform effect)
- Shows shadow on hover
- Disabled state (gray) during processing
- White text, bold font

### Results Section
- Fades in with animation
- Predicted class in highlighted box
- Progress bars animate from 0 to actual percentage
- Scores sorted by confidence (highest first)

### Loading State
- Shows "⏳ Analyzing..." message
- Purple text color
- Centered alignment

### Error Messages
- Red background (#fee)
- Red text (#e74c3c)
- Rounded corners
- Only shows when there's an error

## Responsive Design

The UI adapts to different screen sizes:

- **Desktop**: Full width up to 700px, centered
- **Tablet**: Adjusts padding and font sizes
- **Mobile**: Stacks elements vertically, touch-friendly buttons

## Keyboard Shortcuts

- **Ctrl + Enter**: Submit text for analysis (when focused on textarea)

## Animations

1. **Fade In**: Results section fades in smoothly
2. **Button Hover**: Lifts up with shadow
3. **Progress Bars**: Animate from 0% to actual percentage
4. **Focus**: Input border color transitions smoothly

## Accessibility

- Clear labels for all inputs
- High contrast text
- Large, touch-friendly buttons
- Keyboard navigation support
- Screen reader friendly structure

## Browser Compatibility

Works on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Tips for Best Experience

1. Use a modern browser
2. Enable JavaScript
3. Use Bengali Unicode font
4. Stable internet connection (for first model download)
5. Desktop or tablet for best experience

## Example Workflow

1. **Open** http://localhost:5000
2. **See** the beautiful purple gradient interface
3. **Type** Bengali text in the textarea
4. **Click** "Analyze Text" button
5. **Wait** for "Analyzing..." message
6. **View** predicted class and confidence scores
7. **Analyze** more text by typing again

## Visual Hierarchy

1. **Title** (largest, centered)
2. **Subtitle** (smaller, gray)
3. **Input Label** (medium, bold)
4. **Textarea** (large, prominent)
5. **Button** (full-width, eye-catching)
6. **Results** (highlighted, animated)
7. **Scores** (detailed, visual bars)

Enjoy the beautiful interface! 🎨
