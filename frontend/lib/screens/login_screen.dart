import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import 'student_dashboard.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override State<LoginScreen> createState()=>_LoginScreenState();
}
class _LoginScreenState extends State<LoginScreen> {
  final email=TextEditingController(), password=TextEditingController();
  bool loading=false;
  Future<void> login() async {
    setState(()=>loading=true);
    try {
      final api=ApiService();
      final result=await AuthService(api).login(email.text.trim(),password.text);
      api.token=result['access_token'];
      if(!mounted)return;
      Navigator.pushReplacement(context,MaterialPageRoute(builder:(_)=>StudentDashboard(api:api)));
    } catch(e) {
      if(mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(e.toString())));
    } finally { if(mounted)setState(()=>loading=false); }
  }
  @override Widget build(BuildContext context)=>Scaffold(
    body:Center(child:SingleChildScrollView(padding:const EdgeInsets.all(24),
      child:ConstrainedBox(constraints:const BoxConstraints(maxWidth:460),
        child:Column(children:[
          const Text('تسجيل الدخول',style:TextStyle(fontSize:30,fontWeight:FontWeight.bold)),
          const SizedBox(height:24),
          TextField(controller:email,decoration:const InputDecoration(labelText:'البريد الإلكتروني',border:OutlineInputBorder())),
          const SizedBox(height:12),
          TextField(controller:password,obscureText:true,decoration:const InputDecoration(labelText:'كلمة المرور',border:OutlineInputBorder())),
          const SizedBox(height:20),
          SizedBox(width:double.infinity,child:FilledButton(onPressed:loading?null:login,child:Text(loading?'جارٍ الدخول...':'دخول')))
        ])))
  );
}
