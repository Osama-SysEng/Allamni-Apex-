# Allamni Flutter Frontend - Complete Documentation

## 📱 Project Overview

Allamni Flutter App is the mobile frontend for the Allamni AI Education Operating System. It provides a complete, bilingual (Arabic/English) mobile application with offline capabilities, supporting students, teachers, and institution administrators.

## 🏗️ Architecture

### Directory Structure
```
flutter_app/
├── lib/
│   ├── main.dart                 # App entry point
│   ├── app.dart                  # App widget with providers
│   ├── config/                   # Configuration files
│   │   ├── api_config.dart      # API endpoints and settings
│   │   └── theme_config.dart    # Theme configuration
│   ├── core/                     # Core functionality
│   │   ├── api/                 # API client layer
│   │   │   └── api_client.dart  # HTTP client with interceptors
│   │   ├── database/            # SQLite database
│   │   │   └── database_helper.dart  # Local database operations
│   │   ├── storage/             # Local storage
│   │   ├── network/             # Network monitoring
│   │   └── utils/               # Utility functions
│   ├── features/                 # Feature modules
│   │   ├── auth/                # Authentication
│   │   │   └── screens/
│   │   │       └── auth_screen.dart
│   │   ├── student/             # Student features
│   │   │   └── screens/
│   │   │       └── student_dashboard_screen.dart
│   │   ├── teacher/             # Teacher features
│   │   │   └── screens/
│   │   │       └── teacher_dashboard_screen.dart
│   │   ├── admin/               # Admin features
│   │   │   └── screens/
│   │   │       └── admin_dashboard_screen.dart
│   │   ├── learning/            # Learning features
│   │   ├── ai/                  # AI features
│   │   └── billing/             # Billing features
│   ├── shared/                   # Shared components
│   │   ├── widgets/             # Reusable widgets
│   │   ├── models/              # Data models
│   │   │   ├── user_model.dart
│   │   │   └── user_model.g.dart
│   │   ├── providers/           # Riverpod providers
│   │   │   └── auth_provider.dart
│   │   └── services/            # Shared services
│   └── l10n/                     # Localization
│       ├── ar.json              # Arabic translations
│       └── en.json              # English translations
├── assets/
│   ├── images/
│   ├── icons/
│   ├── fonts/
│   └── translations/
│       ├── ar.json
│       └── en.json
├── test/
│   └── widget_test.dart
├── pubspec.yaml
└── README.md
```

## 🔧 Technology Stack

### Core Dependencies
- **Flutter SDK**: 3.0.0+
- **Dart SDK**: 3.0.0+

### State Management
- **flutter_riverpod**: ^2.4.9 - Reactive state management
- **riverpod_annotation**: ^2.3.3 - Code generation for Riverpod

### Data Persistence
- **sqflite**: ^2.3.0 - SQLite database for offline storage
- **path_provider**: ^2.1.1 - File system access
- **shared_preferences**: ^2.2.2 - Simple key-value storage
- **flutter_secure_storage**: ^9.0.0 - Secure token storage

### Networking
- **http**: ^1.1.0 - HTTP client
- **dio**: ^5.4.0 - Advanced HTTP client with interceptors
- **connectivity_plus**: ^5.0.2 - Network connectivity monitoring

### Localization
- **intl**: ^0.18.1 - Internationalization
- **easy_localization**: ^3.0.3 - Easy localization management

### UI Components
- **cupertino_icons**: ^1.0.6 - iOS-style icons
- **flutter_svg**: ^2.0.9 - SVG image support
- **cached_network_image**: ^3.3.0 - Cached network images
- **shimmer**: ^3.0.0 - Loading shimmer effects
- **fl_chart**: ^0.66.0 - Charts and graphs

### Forms & Validation
- **flutter_form_builder**: ^9.1.1 - Form building
- **form_builder_validators**: ^9.1.0 - Form validation

### File Handling
- **file_picker**: ^6.1.1 - File picking
- **image_picker**: ^1.0.5 - Image selection

### Voice & Speech
- **speech_to_text**: ^6.3.0 - Speech recognition

### Utilities
- **uuid**: ^4.2.1 - UUID generation
- **crypto**: ^3.0.3 - Cryptographic operations
- **logger**: ^2.0.2+1 - Logging

## 🚀 Features

### Multi-Role Support
- **Student Dashboard**: Personalized learning, AI tutoring, progress tracking
- **Teacher Dashboard**: Student management, content creation, analytics
- **Admin Dashboard**: Institution management, billing, code generation

### Bilingual Interface
- **Arabic**: Full RTL support with Cairo font
- **English**: LTR support with Roboto font
- **Easy Switching**: Language switch in settings

### Arabic Dialect Support
- **Modern Standard Arabic** (الفصحى الحديثة)
- **Egyptian Dialect** (مصرية)
- **Gulf Dialect** (خليجية)
- **Levantine Dialect** (شامية)

### Offline Capability
- **SQLite Database**: Local data storage
- **Offline Actions**: Queue actions when offline
- **Auto Sync**: Automatic synchronization when online
- **Cache Management**: Intelligent data caching

### AI-Powered Features
- **AI Chat**: Context-aware conversations
- **Voice Input**: Speech-to-text for questions
- **Image Analysis**: Homework help with image upload
- **Personalized Recommendations**: Adaptive learning paths

### Real-time Features
- **Progress Tracking**: Live progress updates
- **Notifications**: Push notifications
- **Data Sync**: Real-time data synchronization

## 🔐 Security

### Authentication
- **JWT Token Storage**: Secure token storage
- **Token Refresh**: Automatic token refresh
- **Session Management**: Secure session handling

### Data Security
- **HTTPS/TLS**: Encrypted API communication
- **Secure Storage**: Sensitive data in secure storage
- **Input Validation**: Comprehensive input sanitization

### Permission System
- **Role-Based Access**: RBAC implementation
- **Scope-Based Permissions**: Own, institution, all scopes
- **API Authorization**: Token-based API access

## 📱 User Interfaces

### Authentication Screen
- Login/Register toggle
- Email and password fields
- Optional code field
- Form validation
- Error handling

### Student Dashboard
- **Home**: Welcome message, progress overview, recent lessons
- **Learning**: Course content, lessons, assessments
- **AI Tutor**: Chat interface with dialect selector, voice input
- **Profile**: User settings, language selection, logout

### Teacher Dashboard
- **Home**: Statistics, recent activity, quick actions
- **Students**: Student list with progress tracking
- **Content**: Lesson and assessment management
- **Profile**: Teacher settings and logout

### Admin Dashboard
- **Home**: Institution overview, subscription status, quick actions
- **Institution**: Code generation, institution settings
- **Billing**: Invoice management, payment history
- **Profile**: Admin settings and logout

## 🔌 API Integration

### API Client
- **Base URL**: Configurable in `api_config.dart`
- **Interceptors**: Automatic token injection, error handling
- **Timeout**: 30-second timeouts for all requests
- **Error Handling**: Comprehensive error management

### Endpoints
- **Authentication**: `/api/auth/*`
- **Students**: `/api/students/*`
- **Teachers**: `/api/teachers/*`
- **Institutions**: `/api/institutions/*`
- **Learning**: `/api/learning/*`
- **AI**: `/api/ai/*`
- **Billing**: `/api/billing/*`

## 💾 Database Schema

### Tables
- **users**: User information
- **learning_profiles**: Student learning profiles
- **progress**: Learning progress tracking
- **offline_actions**: Queued offline actions
- **cache**: Data caching
- **conversations**: AI conversation history

### Operations
- **CRUD**: Create, Read, Update, Delete operations
- **Queries**: Complex queries with filtering and sorting
- **Transactions**: Database transaction support
- **Migrations**: Schema versioning and migrations

## 🌐 Localization

### Supported Languages
- **Arabic (ar)**: Default language, RTL support
- **English (en)**: LTR support

### Translation Files
- **ar.json**: Arabic translations
- **en.json**: English translations

### Key Translation Categories
- Authentication (login, register, forgot password)
- Navigation (dashboard, home, learning, profile)
- Learning (lessons, progress, assessments)
- AI (tutor, dialect, voice input)
- Settings (language, notifications, privacy)

## 🧪 Testing

### Widget Tests
- **App Smoke Test**: Basic app functionality
- **Auth Screen Tests**: Login form validation
- **Dashboard Tests**: UI component testing

### Integration Tests
- **End-to-End Flows**: Complete user journeys
- **API Integration**: Backend communication tests
- **Database Operations**: Local storage tests

### Running Tests
```bash
# Widget tests
flutter test

# Integration tests
flutter test integration_test/

# With coverage
flutter test --coverage
```

## 📦 Build & Deployment

### Development Build
```bash
flutter run
```

### Production Build
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

### Configuration
1. **API URL**: Update `lib/config/api_config.dart`
2. **API Keys**: Configure Gemini and Odoo API keys
3. **Feature Flags**: Enable/disable features in `api_config.dart`

## 🔧 Configuration

### API Configuration
```dart
class ApiConfig {
  static const String baseUrl = 'http://localhost:8000';
  static const int connectTimeout = 30000;
  static const bool enableVoiceInput = true;
  static const bool enableImageAnalysis = true;
  static const bool enableOfflineMode = true;
}
```

### Theme Configuration
- **Light Theme**: Default light theme with green primary color
- **Dark Theme**: Dark theme variant (to be implemented)
- **Custom Fonts**: Cairo for Arabic, Roboto for English

## 🚧 Known Limitations

### Current Limitations
- **Fonts**: Cairo font files need to be added to assets/fonts/
- **Icons**: Custom icons need to be added to assets/icons/
- **Images**: Placeholder images need to be added to assets/images/
- **Code Generation**: `user_model.g.dart` needs to be regenerated with `flutter pub run build_runner build`

### Future Enhancements
- **Push Notifications**: Full notification system
- **Real-time Updates**: WebSocket integration
- **Advanced Analytics**: Detailed learning analytics
- **Video Support**: Video content integration
- **File Sharing**: Document sharing capabilities

## 📚 Development Guidelines

### Code Style
- **Dart Style**: Follow official Dart style guide
- **Naming**: Use descriptive names for variables and functions
- **Comments**: Add comments for complex logic
- **Structure**: Maintain consistent file structure

### Git Workflow
- **Branching**: Feature branches for new features
- **Commits**: Descriptive commit messages
- **PRs**: Code review before merging

### Testing
- **Unit Tests**: Test individual functions
- **Widget Tests**: Test UI components
- **Integration Tests**: Test complete flows
- **Coverage**: Maintain >80% code coverage

## 🆘 Troubleshooting

### Common Issues

#### Build Errors
- **Missing Dependencies**: Run `flutter pub get`
- **Code Generation**: Run `flutter pub run build_runner build`
- **Font Issues**: Ensure font files are in assets/fonts/

#### Runtime Errors
- **API Connection**: Check backend server is running
- **Database Issues**: Clear app data and reinstall
- **Authentication**: Check token storage

#### UI Issues
- **RTL Problems**: Check locale configuration
- **Font Issues**: Verify font files are present
- **Layout Issues**: Test on different screen sizes

## 📞 Support

For issues and questions:
- Check this documentation
- Review Flutter documentation
- Check backend API documentation
- Contact development team

## 📄 License

Proprietary - All rights reserved

---

**Note**: This Flutter app is designed to work with the Allamni v4.0 backend. Ensure the backend is running and properly configured before using the mobile app.