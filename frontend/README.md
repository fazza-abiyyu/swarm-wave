# Swarm Lab – Swarm Algorithm Playground

An educational web application built with Vue 3 + Nuxt 4 and Tailwind CSS for managing experimental data tables, specifically designed for swarm intelligence algorithm research and learning.

## 🎯 Features

### 🎯 Features

### Dynamic Data Table (CRUD Operations)
- **Add/Remove Rows**: Create new data entries dynamically
- **Add/Remove Columns**: Extend your data structure as needed
- **Inline Editing**: Edit cell values directly like in Excel/Notion
- **Real-time JSON Sync**: Two-way binding between table and JSON input
- **JSON Import/Export**: Load and save data in JSON format
- **CSV Import/Export**: Full CSV support for data exchange with external tools
- **Sample Data**: Built-in swarm intelligence experiment datasets
- **Error Handling**: Robust validation and user-friendly error messages
- **Toast Notifications**: Elegant, non-intrusive feedback system
- **Custom Modals**: No native alert/confirm dialogs
- **Responsive Toolbar**: Grid layout for mobile, flex for desktop

### Algorithm Simulation
- **Swarm Algorithms**: Run Ant Colony Optimization (ACO) and Particle Swarm Optimization (PSO)
- **Real-time Visualization**: See algorithm performance metrics update in real-time
- **Parameter Tuning**: Adjust algorithm parameters directly in the table
- **Performance Tracking**: Monitor iterations, best scores, and convergence

### Educational Theme
- **Academic Color Scheme**: Blue and yellow as primary colors
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Clean UI**: Modern, intuitive interface for educational use
- **English Language**: All labels, buttons, and messages in English

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd swarm-lab

# Install dependencies
npm install

# Start the development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Open your browser
Navigate to http://localhost:3000/dashboard
```

## 📁 Project Structure

```
swarm-lab/
└── frontend
    ├── .gitignore
    ├── AI_CHAT_SETUP.md
    ├── README.md
    ├── app.vue
    ├── app
        ├── app.vue
        ├── components
        │   ├── DynamicTable.vue
        │   └── SimulationPage.vue
        ├── composables
        │   └── useAiChatStream.ts
        └── pages
        │   ├── about.vue
        │   ├── dashboard
        │       └── index.vue
        │   └── index.vue
    ├── assets
        └── css
        │   └── main.css
    ├── nuxt.config.ts
    ├── package.json
    ├── public
        ├── afavicon.ico
        ├── favicon.ico
        └── robots.txt
    ├── server
        └── api
        │   ├── chat-stream.post.ts
        │   └── test.get.ts
    ├── tailwind.config.js
    └── tsconfig.json
```

## 🎨 UI Components

### DynamicTable.vue
- **Buttons**: "Add Row", "Add Column", "Import JSON", "Export JSON", "Delete"
- **Features**: 
  - Inline cell editing
  - Column header editing
  - Row deletion with confirmation
  - Column deletion with confirmation
  - JSON validation and error display

### Dashboard.vue
- **Sample Data**: Pre-loaded swarm intelligence experiment data
- **Instructions**: Clear usage guidelines
- **Navigation**: Clean header and footer
- **Responsive**: Mobile-friendly design

## 📊 Sample Data

The application comes with sample data for swarm intelligence experiments:

```json
[
  {
    "Student": "Alice Johnson",
    "Age": "22",
    "Algorithm": "Ant Colony Optimization",
    "Iterations": "1000",
    "Best_Score": "95.5",
    "Parameters": "alpha=1.0, beta=2.0"
  }
]
```

## 🛠️ Technologies Used

- **Vue 3** - Progressive JavaScript framework
- **Nuxt 3** - Vue.js meta-framework
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type safety (Nuxt config)
- **Vite** - Fast build tool

## 🎓 Educational Use Cases

Perfect for:
- **Computer Science Courses**: Data structure visualization
- **Research Projects**: Algorithm performance tracking
- **Student Experiments**: Swarm intelligence algorithm testing
- **Data Analysis**: Real-time data manipulation
- **Teaching Tools**: Interactive data management

## 📱 Responsive Design

The application is fully responsive:
- **Desktop**: Full-featured table view
- **Tablet**: Optimized touch interactions
- **Mobile**: Scrollable table with mobile-friendly buttons

## 🔄### 📊 Data Flow

```
JSON/CSV Input ↔ Table Display ↔ Export Options ↔ Algorithm Simulation
        ↓            ↓                ↓                    ↓
    Import JSON    Edit Cells     JSON Export          ACO Algorithm
    Import CSV     Add/Remove     CSV Export          PSO Algorithm
    Validate       Columns        Sample Data         Performance Tracking
    Sync           Inline Edit    Real-time Sync       
```

## 🎨 Color Scheme

- **Primary Blue**: `#3b82f6` (buttons, links, accents)
- **Primary Yellow**: `#eab308` (secondary actions, highlights)
- **Background**: Gradient from blue-50 to yellow-50
- **Text**: Gray scale for readability
- **Success**: Green for success states
- **Error**: Red for error states

## 🔧 Customization

Easy to customize:
- Change colors in `tailwind.config.js`
- Modify sample data in `Dashboard.vue`
- Add new columns/fields as needed
- Extend functionality in `DynamicTable.vue`

---

**Swarm Lab** - Making data management intuitive for educational swarm intelligence research.

Built with ❤️ for educators and students in computer science.
