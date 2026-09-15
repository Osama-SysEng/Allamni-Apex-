# Allamni Flutter App

AI Education Operating System - Flutter Frontend Application

## 🌟 Features

- **Multi-Role Support**: Student, Teacher, Institution Admin, Parent, Super Admin
- **Bilingual Interface**: Arabic and English with RTL support
- **Arabic Dialect Support**: Modern Standard, Egyptian, Gulf, Levantine
- **Offline Capability**: SQLite database for offline access
- **Real-time Sync**: Automatic synchronization with backend
- **AI-Powered Learning**: Chat, explanations, voice input, image analysis
- **Interactive Dashboard**: Personalized learning analytics
- **Progress Tracking**: Real-time learning progress monitoring
- **Spaced Repetition**: Smart review scheduling based on learning science
- **Clean Architecture**: Separation of concerns with Repository pattern
- **Riverpod State Management**: Reactive state management with code generation

## 🏗️ Architecture

```
lib/
├── main.dart                 # App entry point
├── app.dart                  # App widget with providers
├── config/                   # Configuration files
│   ├── api_config.dart      # API endpoints
│   └── theme_config.dart    # Theme configuration
├── core/                     # Core functionality
│   ├── api/                 # API client layer
│   ├── database/            # SQLite database
│   ├── storage/             # Local storage
│   └── network/             # Network monitoring
├── features/                 # Feature modules
│   ├── auth/                # Authentication
│   ├── student/             # Student features
│   ├── teacher/             # Teacher features
│   ├── admin/               # Admin features
│   ├── learning/            # Learning features
│   └── ai/                  # AI features
├── shared/                   # Shared components
│   ├── widgets/             # Reusable widgets
│   ├── models/              # Data models
│   ├── providers/           # Riverpod providers
│   ├── repositories/        # Repository pattern
│   └── services/            # Shared services
└── l10n/                     # Localization
    ├── ar.json              # Arabic translations
    └── en.json              # English translations
```

## 🛠️ Technology Stack

- **Flutter**: 3.0.0+
- **Riverpod**: State management with code generation
- **SQLite**: Local database for offline support
- **Dio**: Advanced HTTP client
- **Easy Localization**: Bilingual support
- **Fl Chart**: Data visualization
- **Speech to Text**: Voice input

## 📦 Getting Started

### Prerequisites
- Flutter SDK 3.0.0+
- Dart SDK 3.0.0+
- Backend server running on http://localhost:8000

### Installation
```bash
cd flutter_app
flutter pub get
flutter run
```

### Code Generation
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

## 🎨 UI Components

### Enhanced Widgets
- **LoadingShimmer**: Loading animations
- **ErrorCard**: Error display with retry
- **EmptyState**: Empty state placeholders
- **ProgressCard**: Progress tracking
- **StatCard**: Statistics display
- **ChatWidget**: AI chat interface
- **SkillProgressWidget**: Skill tracking with milestones
- **SimpleRadarChartWidget**: Skill visualization

## 🔄 Architecture Patterns

### Clean Architecture
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic separation
- **Dependency Injection**: Riverpod providers
- **Offline-First**: Local database sync

### State Management
- **Riverpod**: Reactive state management
- **Async Notifiers**: Async operations
- **Family Modifiers**: Dynamic providers
- **Code Generation**: Type-safe providers

## 🚀 Build & Deploy

### Development
```bash
flutter run
```

### Production
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

## 📱 Supported Platforms
- Android
- iOS
- Web
- Windows
- Linux
- macOS

## 🔒 Security
- Secure token storage
- HTTPS/TLS communication
- Input validation
- Permission-based access

## 🌐 Localization
- Arabic (RTL)
- English (LTR)
- Easy language switching

## 📊 Features by Role

### Student
- Personalized learning dashboard
- AI-powered tutoring
- Progress tracking
- Assessments and quizzes
- Voice input for questions
- Image analysis for homework help
- Spaced repetition reviews

### Teacher
- Student management
- Content creation
- Assessment tools
- Progress analytics
- AI assistant for lesson planning

### Institution Admin
- Institution management
- Student/teacher code generation
- Subscription management
- Billing and payments
- Analytics and reports

## 🧪 Testing
```bash
# Unit tests
flutter test

# Widget tests
flutter test test/widget/

# Integration tests
flutter test integration_test/
```

## 📚 Documentation
- [Flutter Documentation](FLUTTER_DOCUMENTATION.md)
- [Backend API Documentation](../docs/)
- [Architecture Overview](../README.md)

## 🤝 Open Source Inspiration
This project incorporates best practices from:
- **Deep-Learn**: Clean architecture with Riverpod and Gemini AI
- **Holom Said**: Arabic e-learning with Supabase and Riverpod
- **Edu-App**: Bilingual support with Firebase
- **Seekho**: Interactive learning with code execution

## 📄 License
Proprietary - All rights reserved