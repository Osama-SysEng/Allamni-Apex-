import 'package:flutter/material.dart';
class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({super.key});
  @override Widget build(BuildContext context)=>Scaffold(
    appBar:AppBar(title:const Text('الإشعارات')),
    body:Center(child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
      const Icon(Icons.notifications,size:80),const SizedBox(height:16),
      const Text('الإشعارات',style:TextStyle(fontSize:24,fontWeight:FontWeight.bold))
    ]))
  );
}
