import 'api_service.dart';

class AuthService {
  final ApiService api;
  AuthService(this.api);

  Future<Map<String,dynamic>> login(String email,String password) =>
      api.post('/api/auth/login', {'email':email,'password':password});

  Future<Map<String,dynamic>> register(String email,String password,String name) =>
      api.post('/api/auth/register', {
        'email':email,'password':password,'full_name':name,
        'role':'student','goal_domain':'software_development'
      });
}
