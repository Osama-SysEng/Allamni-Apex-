import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../shared/providers/auth_provider.dart';

class AuthScreen extends ConsumerStatefulWidget {
  const AuthScreen({super.key});

  @override
  ConsumerState<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends ConsumerState<AuthScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _codeController = TextEditingController();
  final _nameController = TextEditingController();
  
  bool _isLoginMode = true;
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _codeController.dispose();
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });
    
    final authNotifier = ref.read(authProvider.notifier);
    
    bool success;
    if (_isLoginMode) {
      success = await authNotifier.login(
        _emailController.text,
        _passwordController.text,
        _codeController.text.isEmpty ? null : _codeController.text,
      );
    } else {
      success = await authNotifier.registerWithCode(
        _codeController.text,
        _emailController.text,
        _passwordController.text,
        _nameController.text,
      );
    }
    
    setState(() {
      _isLoading = false;
      if (!success) {
        _errorMessage = authNotifier.state.error ?? 'Authentication failed';
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Logo
                  const Icon(
                    Icons.school,
                    size: 80,
                    color: Color(0xFF4CAF50),
                  ),
                  const SizedBox(height: 16),
                  
                  // Title
                  Text(
                    'Allamni',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: const Color(0xFF4CAF50),
                    ),
                    textAlign: TextAlign.center,
                  ),
                  Text(
                    'علّمني',
                    style: Theme.of(context).textTheme.headlineSmall,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),
                  
                  // Mode toggle
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      TextButton(
                        onPressed: () => setState(() => _isLoginMode = true),
                        child: Text(
                          'login'.tr(),
                          style: TextStyle(
                            color: _isLoginMode ? const Color(0xFF4CAF50) : Colors.grey,
                            fontWeight: _isLoginMode ? FontWeight.bold : FontWeight.normal,
                          ),
                        ),
                      ),
                      const SizedBox(width: 16),
                      TextButton(
                        onPressed: () => setState(() => _isLoginMode = false),
                        child: Text(
                          'register'.tr(),
                          style: TextStyle(
                            color: !_isLoginMode ? const Color(0xFF4CAF50) : Colors.grey,
                            fontWeight: !_isLoginMode ? FontWeight.bold : FontWeight.normal,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  
                  // Name field (registration only)
                  if (!_isLoginMode)
                    TextFormField(
                      controller: _nameController,
                      decoration: InputDecoration(
                        labelText: 'name'.tr(),
                        prefixIcon: const Icon(Icons.person),
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'name_required'.tr();
                        }
                        return null;
                      },
                    ),
                  
                  // Email field
                  TextFormField(
                    controller: _emailController,
                    decoration: InputDecoration(
                      labelText: 'email'.tr(),
                      prefixIcon: const Icon(Icons.email),
                    ),
                    keyboardType: TextInputType.emailAddress,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'email_required'.tr();
                      }
                      if (!value.contains('@')) {
                        return 'email_invalid'.tr();
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  
                  // Password field
                  TextFormField(
                    controller: _passwordController,
                    decoration: InputDecoration(
                      labelText: 'password'.tr(),
                      prefixIcon: const Icon(Icons.lock),
                    ),
                    obscureText: true,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'password_required'.tr();
                      }
                      if (value.length < 6) {
                        return 'password_too_short'.tr();
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  
                  // Code field
                  TextFormField(
                    controller: _codeController,
                    decoration: InputDecoration(
                      labelText: _isLoginMode ? 'login_code_optional'.tr() : 'registration_code'.tr(),
                      prefixIcon: const Icon(Icons.code),
                    ),
                  ),
                  const SizedBox(height: 24),
                  
                  // Error message
                  if (_errorMessage != null)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 16),
                      child: Text(
                        _errorMessage!,
                        style: const TextStyle(color: Colors.red),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  
                  // Phase 5 Enhanced Security indicator
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: Colors.green[50],
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.green[200]!),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.security, size: 16, color: Colors.green[700]),
                        const SizedBox(width: 8),
                        Text(
                          'enhanced_security_enabled'.tr(),
                          style: TextStyle(color: Colors.green[700], fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),
                  
                  // Submit button
                  ElevatedButton(
                    onPressed: _isLoading ? null : _submit,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: _isLoading
                        ? const SizedBox(
                            height: 20,
                            width: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : Text(_isLoginMode ? 'login'.tr() : 'register'.tr()),
                  ),
                  
                  const SizedBox(height: 16),
                  
                  // Forgot password
                  TextButton(
                    onPressed: () {
                      // TODO: Implement forgot password
                    },
                    child: Text('forgot_password'.tr()),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}