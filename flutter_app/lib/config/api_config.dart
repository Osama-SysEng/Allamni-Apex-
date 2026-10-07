class ApiConfig {
  // Base URLs
  static const String baseUrl = 'http://localhost:8000';
  static const String apiVersion = '/api/v1';
  
  // Service-specific URLs (for direct service access)
  static const String authBaseUrl = 'http://localhost:8001';
  static const String aiBaseUrl = 'http://localhost:8003';
  static const String institutionBaseUrl = 'http://localhost:8005';
  
  // Endpoints
  static const String auth = '/auth';
  static const String students = '/students';
  static const String teachers = '/teachers';
  static const String institutions = '/institutions';
  static const String learning = '/learning';
  static const String ai = '/ai';
  static const String billing = '/billing';
  
  // Timeout settings
  static const int connectTimeout = 30000; // 30 seconds
  static const int receiveTimeout = 30000; // 30 seconds
  static const int sendTimeout = 30000; // 30 seconds
  
  // API Keys (to be configured in production)
  static String? geminiApiKey;
  static String? odooApiKey;
  
  // Feature flags
  static const bool enableVoiceInput = true;
  static const bool enableImageAnalysis = true;
  static const bool enableOfflineMode = true;
  static const bool enableNotifications = true;
  static const bool enablePhase5Chatbot = true;
  
  // Pagination
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;
  
  // File upload limits
  static const int maxFileSize = 10 * 1024 * 1024; // 10MB
  static const List<String> allowedImageFormats = ['jpg', 'jpeg', 'png', 'gif'];
  static const List<String> allowedDocumentFormats = ['pdf', 'doc', 'docx'];
}