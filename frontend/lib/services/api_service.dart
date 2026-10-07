import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;
  String? token;
  ApiService({this.baseUrl='http://localhost:8000'});

  Map<String,String> get headers => {
    'Content-Type':'application/json',
    if (token != null) 'Authorization':'Bearer $token'
  };

  Future<Map<String,dynamic>> get(String path) async {
    final r = await http.get(Uri.parse('$baseUrl$path'), headers: headers);
    if (r.statusCode >= 400) throw Exception(r.body);
    return jsonDecode(r.body) as Map<String,dynamic>;
  }

  Future<Map<String,dynamic>> post(String path, Map<String,dynamic> body) async {
    final r = await http.post(Uri.parse('$baseUrl$path'),
      headers: headers, body: jsonEncode(body));
    if (r.statusCode >= 400) throw Exception(r.body);
    return jsonDecode(r.body) as Map<String,dynamic>;
  }
}
