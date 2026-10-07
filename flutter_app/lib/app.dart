import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'config/theme_config.dart';
import 'features/auth/screens/auth_screen.dart';
import 'features/student/screens/student_dashboard_screen.dart';
import 'features/teacher/screens/teacher_dashboard_screen.dart';
import 'features/admin/screens/admin_dashboard_screen.dart';
import 'shared/providers/auth_provider.dart';

class AllamniApp extends ConsumerWidget {
  const AllamniApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);
    final theme = AppTheme.getTheme(context.locale.languageCode);

    return MaterialApp(
      title: 'Allamni - علّمني',
      debugShowCheckedModeBanner: false,
      theme: theme,
      localizationsDelegates: context.localizationDelegates,
      supportedLocales: context.supportedLocales,
      locale: context.locale,
      
      // Route configuration
      initialRoute: authState.isAuthenticated ? '/dashboard' : '/auth',
      routes: {
        '/auth': (context) => const AuthScreen(),
        '/dashboard': (context) => _getDashboardScreen(authState.userRole),
      },
      
      // RTL support for Arabic
      builder: (context, child) {
        return Directionality(
          textDirection: context.locale.languageCode == 'ar' 
              ? TextDirection.rtl 
              : TextDirection.ltr,
          child: child!,
        );
      },
    );
  }

  Widget _getDashboardScreen(String? role) {
    switch (role) {
      case 'student':
        return const StudentDashboardScreen();
      case 'teacher':
        return const TeacherDashboardScreen();
      case 'institution_admin':
      case 'super_admin':
        return const AdminDashboardScreen();
      default:
        return const AuthScreen();
    }
  }
}