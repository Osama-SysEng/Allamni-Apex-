import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';

void main() => runApp(const AllamniApp());

class AllamniApp extends StatelessWidget {
  const AllamniApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
    debugShowCheckedModeBanner: false,
    title: 'علّمني',
    theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.indigo),
    home: const SplashScreen(),
  );
}
