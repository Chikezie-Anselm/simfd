# GSM Subscription Fraud Detection System - Frontend

A modern, responsive Next.js 14 frontend application for the GSM Subscription Fraud Detection System. This application provides an intuitive interface for uploading CSV files containing subscriber data and viewing AI-powered fraud detection results.

## 🚀 Features

- **Modern UI/UX**: Clean, responsive design built with Tailwind CSS
- **File Upload**: Drag-and-drop CSV file upload with validation
- **Real-time Results**: Interactive dashboard with fraud detection results
- **Data Visualization**: Charts and analytics powered by Chart.js
- **TypeScript**: Full type safety and developer experience
- **Mobile Responsive**: Optimized for all device sizes
- **Error Handling**: Comprehensive error states and user feedback

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Chart.js
- **HTTP Client**: Axios
- **State Management**: React Hooks
- **Notifications**: React Hot Toast

## 📁 Project Structure

```
gsm-fraud-ui/
├── app/                    # Next.js App Router pages
│   ├── about/             # About page
│   ├── results/           # Results dashboard
│   ├── upload/            # File upload page
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # Reusable React components
│   ├── AlertMessage.tsx   # Alert/notification component
│   ├── FileUpload.tsx     # File upload with drag-and-drop
│   ├── LoadingSpinner.tsx # Loading state component
│   ├── Navbar.tsx         # Navigation component
│   ├── ResultsTable.tsx   # Results data table
│   └── SummaryChart.tsx   # Charts and analytics
├── lib/                   # Utility libraries
│   └── api.ts            # Axios configuration
├── types/                 # TypeScript type definitions
│   └── index.ts          # Interface definitions
├── public/               # Static assets
└── config files          # Next.js, Tailwind, TypeScript configs
```

## 🚦 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Flask backend running on `http://localhost:5000`

### Installation

1. **Clone or create the project directory:**
   ```bash
   cd gsm-fraud-ui
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🔗 Backend Integration

The frontend integrates with the Flask backend API through the following endpoints:

- `POST /upload` - Upload CSV file for fraud detection
- Backend should be running on `http://localhost:5000`

### Environment Variables

Create a `.env.local` file for custom configuration:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## 📊 Usage Flow

1. **Home Page**: Overview and introduction to the system
2. **Upload Page**: 
   - Upload CSV file with subscriber data
   - Drag-and-drop or click to browse
   - File validation and progress feedback
3. **Results Page**:
   - View fraud detection results in a table
   - Interactive charts showing fraud vs legitimate ratios
   - Summary statistics and risk analysis
4. **About Page**: System information and technical details

### CSV Format Requirements

Your CSV file should include these columns:
- `subscriber_id` - Unique subscriber identifier
- `IMEI` - Device IMEI number
- `registration_date` - Registration date (YYYY-MM-DD)
- `location` - Geographic location
- `initial_call_count` - Number of initial calls
- `average_call_duration` - Average call duration in seconds
- `device_switch_count` - Number of device switches

## 🎨 UI Components

### Core Components

- **FileUpload**: Handles file selection with drag-and-drop support
- **ResultsTable**: Displays fraud detection results with color coding
- **SummaryChart**: Pie chart showing fraud vs legitimate distribution
- **LoadingSpinner**: Loading states during API calls
- **AlertMessage**: Error and success notifications
- **Navbar**: Responsive navigation with mobile menu

### Design System

- **Colors**: Blue primary theme with red/green for fraud indicators
- **Typography**: Clean, academic-style fonts
- **Cards**: Consistent card-based layout
- **Responsive**: Mobile-first design approach

## 🔧 Development

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Code Quality

- TypeScript for type safety
- ESLint for code quality
- Tailwind CSS for consistent styling
- Component-based architecture

## 🚀 Deployment

### Local Production Build

```bash
npm run build
npm run start
```

### Vercel Deployment

1. Connect your repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Environment Variables for Production

```env
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

## 🔍 Features in Detail

### File Upload
- Drag-and-drop interface
- File type validation (CSV only)
- Size limit enforcement (10MB)
- Progress indicators
- Error handling for invalid files

### Results Dashboard
- Interactive data table with sorting
- Color-coded fraud indicators
- Fraud probability visualization
- Summary statistics cards
- Risk level categorization
- Export capabilities

### Charts and Analytics
- Pie chart for fraud distribution
- Progress bars for individual risk scores
- Summary statistics
- Risk level breakdowns

## 🛡️ Security Considerations

- Client-side file validation
- Secure API communication
- No sensitive data stored locally
- Session-based result storage
- Input sanitization

## 📱 Mobile Support

- Responsive design for all screen sizes
- Touch-friendly interfaces
- Mobile-optimized navigation
- Adaptive layout components

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is part of an academic research system for GSM fraud detection.

## 🔗 Related Projects

- [Flask Backend API](../flask-gsm-fraud-detection/) - The backend API that powers this frontend

---

**GSM Subscription Fraud Detection System © 2025**