import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:dio/dio.dart';
import '../../core/api/api_client.dart';
import '../models/user_model.dart';
import '../services/chatbot_service.dart';

// Auth State
class AuthState {
  final bool isAuthenticated;
  final String? userId;
  final String? userRole;
  final String? token;
  final String? enhancedSessionId;
  final bool isLoading;
  final String? error;
  
  const AuthState({
    this.isAuthenticated = false,
    this.userId,
    this.userRole,
    this.token,
    this.enhancedSessionId,
    this.isLoading = false,
    this.error,
  });
  
  AuthState copyWith({
    bool? isAuthenticated,
    String? userId,
    String? userRole,
    String? token,
    String? enhancedSessionId,
    bool? isLoading,
    String? error,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      userId: userId ?? this.userId,
      userRole: userRole ?? this.userRole,
      token: token ?? this.token,
      enhancedSessionId: enhancedSessionId ?? this.enhancedSessionId,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
    );
  }
}

// Auth Provider
class AuthNotifier extends StateNotifier<AuthState> {
  final ApiClient _apiClient;
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  
  AuthNotifier(this._apiClient) : super(const AuthState()) {
    _checkAuthStatus();
  }
  
  Future<void> _checkAuthStatus() async {
    final token = await _secureStorage.read(key: 'access_token');
    final userId = await _secureStorage.read(key: 'user_id');
    final userRole = await _secureStorage.read(key: 'user_role');
    final enhancedSessionId = await _secureStorage.read(key: 'enhanced_session_id');
    
    if (token != null && userId != null) {
      state = state.copyWith(
        isAuthenticated: true,
        userId: userId,
        userRole: userRole,
        token: token,
        enhancedSessionId: enhancedSessionId,
      );
    }
  }
  
  Future<bool> login(String email, String password, String? code) async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      final response = await _apiClient.post(
        '/api/auth/login',
        data: {
          'email': email,
          'password': password,
          if (code != null) 'code': code,
        },
      );
      
      final token = response.data['access_token'];
      final userId = response.data['user']['id'];
      final userRole = response.data['user']['role'];
      final enhancedSessionId = response.data['enhanced_session_id'];
      
      await _secureStorage.write(key: 'access_token', value: token);
      await _secureStorage.write(key: 'refresh_token', value: response.data['refresh_token']);
      await _secureStorage.write(key: 'user_id', value: userId);
      await _secureStorage.write(key: 'user_role', value: userRole);
      if (enhancedSessionId != null) {
        await _secureStorage.write(key: 'enhanced_session_id', value: enhancedSessionId);
      }
      
      state = state.copyWith(
        isAuthenticated: true,
        userId: userId,
        userRole: userRole,
        token: token,
        enhancedSessionId: enhancedSessionId,
        isLoading: false,
      );
      
      return true;
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
      return false;
    }
  }
  
  Future<bool> registerWithCode(String code, String email, String password, String name) async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      final response = await _apiClient.post(
        '/api/auth/register-code',
        data: {
          'code': code,
          'email': email,
          'password': password,
          'name': name,
        },
      );
      
      final token = response.data['access_token'];
      final userId = response.data['user_id'];
      final userRole = response.data['role'];
      
      await _secureStorage.write(key: 'auth_token', value: token);
      await _secureStorage.write(key: 'user_id', value: userId);
      await _secureStorage.write(key: 'user_role', value: userRole);
      
      state = state.copyWith(
        isAuthenticated: true,
        userId: userId,
        userRole: userRole,
        token: token,
        isLoading: false,
      );
      
      return true;
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
      return false;
    }
  }
  
  Future<void> logout() async {
    try {
      // Call enhanced auth logout endpoint if we have a session
      if (state.enhancedSessionId != null && state.token != null) {
        await _apiClient.post(
          '/api/auth/sessions/${state.enhancedSessionId}/revoke',
          options: Options(
            headers: {
              'Authorization': 'Bearer ${state.token}',
            },
          ),
        );
      }
    } catch (e) {
      // Continue with local cleanup even if API call fails
    }
    
    // Clear all stored auth data
    await _secureStorage.delete(key: 'access_token');
    await _secureStorage.delete(key: 'refresh_token');
    await _secureStorage.delete(key: 'user_id');
    await _secureStorage.delete(key: 'user_role');
    await _secureStorage.delete(key: 'enhanced_session_id');
    
    state = const AuthState();
  }
  
  Future<UserModel?> getCurrentUser() async {
    if (state.userId == null) return null;
    
    try {
      final response = await _apiClient.get('/api/users/${state.userId}');
      return UserModel.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }
}

// Provider
final apiClientProvider = Provider<ApiClient>((ref) => ApiClient());
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(apiClientProvider));
});