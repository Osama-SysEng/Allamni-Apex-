import 'package:flutter/material.dart';
class ResourcesScreen extends StatelessWidget {
  const ResourcesScreen({super.key});
  @override Widget build(BuildContext context)=>Scaffold(
    appBar:AppBar(title:const Text('المصادر التعليمية')),
    body:Center(child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
      const Icon(Icons.library_books,size:80),const SizedBox(height:16),
      const Text('المصادر التعليمية',style:TextStyle(fontSize:24,fontWeight:FontWeight.bold))
    ]))
  );
}
