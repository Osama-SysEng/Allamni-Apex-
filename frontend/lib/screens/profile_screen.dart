import 'package:flutter/material.dart';
class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});
  @override Widget build(BuildContext context)=>Scaffold(
    appBar:AppBar(title:const Text('الملف التعليمي')),
    body:Center(child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
      const Icon(Icons.person,size:80),const SizedBox(height:16),
      const Text('الملف التعليمي',style:TextStyle(fontSize:24,fontWeight:FontWeight.bold))
    ]))
  );
}
