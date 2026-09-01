import 'package:flutter/material.dart';
class AssessmentScreen extends StatelessWidget {
  const AssessmentScreen({super.key});
  @override Widget build(BuildContext context)=>Scaffold(
    appBar:AppBar(title:const Text('التقييمات التكيفية')),
    body:Center(child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
      const Icon(Icons.quiz,size:80),const SizedBox(height:16),
      const Text('التقييمات التكيفية',style:TextStyle(fontSize:24,fontWeight:FontWeight.bold))
    ]))
  );
}
