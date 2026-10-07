import 'package:flutter/material.dart';
class CoachChatScreen extends StatelessWidget {
  const CoachChatScreen({super.key});
  @override Widget build(BuildContext context)=>Scaffold(
    appBar:AppBar(title:const Text('المساعد الذكي')),
    body:Center(child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
      const Icon(Icons.smart_toy,size:80),const SizedBox(height:16),
      const Text('المساعد الذكي',style:TextStyle(fontSize:24,fontWeight:FontWeight.bold))
    ]))
  );
}
