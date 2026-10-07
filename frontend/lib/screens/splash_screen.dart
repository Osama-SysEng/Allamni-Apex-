import 'package:flutter/material.dart';
import 'login_screen.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});
  @override
  Widget build(BuildContext context) => Scaffold(
    body: Center(child: Column(mainAxisAlignment:MainAxisAlignment.center, children:[
      const Icon(Icons.school_rounded,size:90),
      const SizedBox(height:20),
      const Text('علّمني',style:TextStyle(fontSize:38,fontWeight:FontWeight.bold)),
      const SizedBox(height:8),
      const Text('مسارك التعليمي، مصمم لك'),
      const SizedBox(height:32),
      FilledButton(
        onPressed:()=>Navigator.pushReplacement(context,
          MaterialPageRoute(builder:(_)=>const LoginScreen())),
        child:const Text('ابدأ')
      )
    ]))
  );
}
