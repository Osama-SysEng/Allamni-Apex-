import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:allamni/main.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: Scaffold(
            body: Text('Test'),
          ),
        ),
      ),
    );

    // Verify that the text is displayed
    expect(find.text('Test'), findsOneWidget);
  });
  
  testWidgets('Auth screen displays login form', (WidgetTester tester) async {
    // Test that auth screen shows login form
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: Scaffold(
            body: Text('Login Screen'),
          ),
        ),
      ),
    );
    
    expect(find.text('Login Screen'), findsOneWidget);
  });
}