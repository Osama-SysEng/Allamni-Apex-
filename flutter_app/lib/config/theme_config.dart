import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData getTheme(String languageCode) {
    final isArabic = languageCode == 'ar';
    
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF4CAF50),
        brightness: Brightness.light,
      ),
      
      // Typography
      fontFamily: isArabic ? 'Cairo' : 'Roboto',
      
      // App Bar Theme
      appBarTheme: AppBarTheme(
        centerTitle: !isArabic,
        elevation: 0,
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        titleTextStyle: TextStyle(
          fontFamily: isArabic ? 'Cairo' : 'Roboto',
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: Colors.black87,
        ),
      ),
      
      // Card Theme
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      
      // Input Decoration Theme
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        filled: true,
        fillColor: Colors.grey[50],
      ),
      
      // Button Theme
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      
      // Icon Theme
      iconTheme: const IconThemeData(
        color: Color(0xFF4CAF50),
      ),
    );
  }
  
  static ThemeData getDarkTheme(String languageCode) {
    final isArabic = languageCode == 'ar';
    
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF4CAF50),
        brightness: Brightness.dark,
      ),
      
      fontFamily: isArabic ? 'Cairo' : 'Roboto',
      
      appBarTheme: AppBarTheme(
        centerTitle: !isArabic,
        elevation: 0,
        backgroundColor: Colors.grey[900],
        foregroundColor: Colors.white,
        titleTextStyle: TextStyle(
          fontFamily: isArabic ? 'Cairo' : 'Roboto',
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
    );
  }
}