import 'package:flutter/material.dart';
class ReportsScreen extends StatelessWidget {
  const ReportsScreen({super.key});
  @override Widget build(BuildContext context)=>Scaffold(
    appBar:AppBar(title:const Text('التقارير والتحليلات')),
    body:Center(child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
      const Icon(Icons.analytics,size:80),const SizedBox(height:16),
      const Text('التقارير والتحليلات',style:TextStyle(fontSize:24,fontWeight:FontWeight.bold))
    ]))
  );
}
