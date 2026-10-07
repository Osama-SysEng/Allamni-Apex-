// Clean Architecture Repository Pattern based on open source best practices
import 'package:dio/dio.dart';
import '../../core/api/api_client.dart';
import '../../core/database/database_helper.dart';
import '../models/user_model.dart';

abstract class UserRepository {
  Future<UserModel?> getCurrentUser();
  Future<UserModel?> getUserById(String userId);
  Future<void> saveUser(UserModel user);
  Future<void> clearUser();
}

class UserRepositoryImpl implements UserRepository {
  final ApiClient _apiClient;
  final DatabaseHelper _databaseHelper;
  
  UserRepositoryImpl(this._apiClient, this._databaseHelper);
  
  @override
  Future<UserModel?> getCurrentUser() async {
    try {
      // Try to get from API first
      final response = await _apiClient.get('/api/users/me');
      final user = UserModel.fromJson(response.data);
      
      // Cache in local database
      await _databaseHelper.saveUser(user.toJson());
      
      return user;
    } catch (e) {
      // Fallback to local database
      final cachedData = await _databaseHelper.getUser('current');
      if (cachedData != null) {
        return UserModel.fromJson(cachedData);
      }
      return null;
    }
  }
  
  @override
  Future<UserModel?> getUserById(String userId) async {
    try {
      final response = await _apiClient.get('/api/users/$userId');
      return UserModel.fromJson(response.data);
    } catch (e) {
      // Try local database
      final cachedData = await _databaseHelper.getUser(userId);
      if (cachedData != null) {
        return UserModel.fromJson(cachedData);
      }
      return null;
    }
  }
  
  @override
  Future<void> saveUser(UserModel user) async {
    await _databaseHelper.saveUser(user.toJson());
  }
  
  @override
  Future<void> clearUser() async {
    await _databaseHelper.delete('users', where: 'id = ?', whereArgs: ['current']);
  }
}

// Repository Provider
final userRepositoryProvider = Provider<UserRepository>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return UserRepositoryImpl(apiClient, DatabaseHelper.instance);
});