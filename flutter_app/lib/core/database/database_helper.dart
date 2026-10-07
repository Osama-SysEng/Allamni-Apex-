import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';

class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;
  
  DatabaseHelper._init();
  
  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('allamni.db');
    return _database!;
  }
  
  Future<Database> _initDB(String filePath) async {
    final dbPath = await getApplicationDocumentsDirectory();
    final path = join(dbPath.path, filePath);
    
    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }
  
  Future<void> _createDB(Database db, int version) async {
    // Users table
    await db.execute('''
      CREATE TABLE users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        institution_id TEXT,
        name TEXT,
        avatar TEXT,
        created_at TEXT,
        updated_at TEXT
      )
    ''');
    
    // Learning profiles table
    await db.execute('''
      CREATE TABLE learning_profiles (
        student_id TEXT PRIMARY KEY,
        goal_domain TEXT,
        skills TEXT,
        preferences TEXT,
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (student_id) REFERENCES users(id)
      )
    ''');
    
    // Progress table
    await db.execute('''
      CREATE TABLE progress (
        id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL,
        skill_code TEXT,
        current_level REAL,
        target_level REAL,
        completed_lessons INTEGER,
        total_lessons INTEGER,
        last_updated TEXT,
        FOREIGN KEY (student_id) REFERENCES users(id)
      )
    ''');
    
    // Offline actions table
    await db.execute('''
      CREATE TABLE offline_actions (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        action_type TEXT NOT NULL,
        payload TEXT,
        synced INTEGER DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
      )
    ''');
    
    // Cache table
    await db.execute('''
      CREATE TABLE cache (
        key TEXT PRIMARY KEY,
        value TEXT,
        expires_at TEXT
      )
    ''');
    
    // Conversations table
    await db.execute('''
      CREATE TABLE conversations (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        messages TEXT,
        dialect TEXT,
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
      )
    ''');
  }
  
  // Generic CRUD operations
  Future<int> insert(String table, Map<String, dynamic> data) async {
    final db = await database;
    return await db.insert(table, data);
  }
  
  Future<List<Map<String, dynamic>>> query(
    String table, {
    bool? distinct,
    List<String>? columns,
    String? where,
    List<dynamic>? whereArgs,
    String? groupBy,
    String? having,
    String? orderBy,
    int? limit,
    int? offset,
  }) async {
    final db = await database;
    return await db.query(
      table,
      distinct: distinct,
      columns: columns,
      where: where,
      whereArgs: whereArgs,
      groupBy: groupBy,
      having: having,
      orderBy: orderBy,
      limit: limit,
      offset: offset,
    );
  }
  
  Future<int> update(
    String table,
    Map<String, dynamic> values, {
    String? where,
    List<dynamic>? whereArgs,
  }) async {
    final db = await database;
    return await db.update(table, values, where: where, whereArgs: whereArgs);
  }
  
  Future<int> delete(
    String table, {
    String? where,
    List<dynamic>? whereArgs,
  }) async {
    final db = await database;
    return await db.delete(table, where: where, whereArgs: whereArgs);
  }
  
  // Specific operations
  Future<void> saveUser(Map<String, dynamic> user) async {
    await insert('users', user);
  }
  
  Future<Map<String, dynamic>?> getUser(String userId) async {
    final results = await query('users', where: 'id = ?', whereArgs: [userId]);
    return results.isNotEmpty ? results.first : null;
  }
  
  Future<void> saveProgress(Map<String, dynamic> progress) async {
    await insert('progress', progress);
  }
  
  Future<List<Map<String, dynamic>>> getStudentProgress(String studentId) async {
    return await query('progress', where: 'student_id = ?', whereArgs: [studentId]);
  }
  
  Future<void> cacheData(String key, String value, {DateTime? expiresAt}) async {
    await insert('cache', {
      'key': key,
      'value': value,
      'expires_at': expiresAt?.toIso8601String(),
    });
  }
  
  Future<String?> getCachedData(String key) async {
    final results = await query('cache', where: 'key = ?', whereArgs: [key]);
    if (results.isEmpty) return null;
    
    final expiresAt = results.first['expires_at'];
    if (expiresAt != null && DateTime.parse(expiresAt).isBefore(DateTime.now())) {
      await delete('cache', where: 'key = ?', whereArgs: [key]);
      return null;
    }
    
    return results.first['value'];
  }
  
  Future<void> clearCache() async {
    await delete('cache');
  }
  
  Future<void> close() async {
    final db = await database;
    await db.close();
  }
}