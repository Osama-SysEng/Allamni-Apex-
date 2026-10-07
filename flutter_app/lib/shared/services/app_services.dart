// Clean Architecture Service Layer based on open source best practices
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:dio/dio.dart';
import '../../core/api/api_client.dart';
import '../repositories/user_repository.dart';
import 'chatbot_service.dart';

class NetworkService {
  final Connectivity _connectivity;
  
  NetworkService(this._connectivity);
  
  Future<bool> isConnected() async {
    final result = await _connectivity.checkConnectivity();
    return result != ConnectivityResult.none;
  }
  
  Stream<ConnectivityResult> get onConnectivityChanged =>
      _connectivity.onConnectivityChanged;
}

class CacheService {
  final DatabaseHelper _databaseHelper;
  
  CacheService(this._databaseHelper);
  
  Future<void> cacheData(String key, String value, {DateTime? expiresAt}) async {
    await _databaseHelper.cacheData(key, value, expiresAt: expiresAt);
  }
  
  Future<String?> getCachedData(String key) async {
    return await _databaseHelper.getCachedData(key);
  }
  
  Future<void> clearCache() async {
    await _databaseHelper.clearCache();
  }
}

class SyncService {
  final ApiClient _apiClient;
  final DatabaseHelper _databaseHelper;
  final NetworkService _networkService;
  
  SyncService(this._apiClient, this._databaseHelper, this._networkService);
  
  Future<void> syncOfflineActions() async {
    if (!await _networkService.isConnected()) return;
    
    final offlineActions = await _databaseHelper.query('offline_actions', 
      where: 'synced = ?',
      whereArgs: [0]
    );
    
    for (var action in offlineActions) {
      try {
        await _apiClient.post(
          '/api/sync/${action['action_type']}',
          data: action['payload']
        );
        
        await _databaseHelper.update('offline_actions',
          {'synced': 1},
          where: 'id = ?',
          whereArgs: [action['id']]
        );
      } catch (e) {
        // Keep action for retry
        continue;
      }
    }
  }
  
  Future<void> queueOfflineAction(String actionType, Map<String, dynamic> payload) async {
    await _databaseHelper.insert('offline_actions', {
      'action_type': actionType,
      'payload': payload,
      'synced': 0,
      'created_at': DateTime.now().toIso8601String(),
    });
  }
}

// Service Providers
final networkServiceProvider = Provider<NetworkService>((ref) {
  return NetworkService(Connectivity());
});

final cacheServiceProvider = Provider<CacheService>((ref) {
  return CacheService(DatabaseHelper.instance);
});

final syncServiceProvider = Provider<SyncService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  final networkService = ref.watch(networkServiceProvider);
  return SyncService(apiClient, DatabaseHelper.instance, networkService);
});

final chatbotServiceProvider = Provider<ChatbotService>((ref) {
  return ChatbotService();
});