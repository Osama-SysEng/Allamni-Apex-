import 'package:flutter/material.dart';
class MetricCard extends StatelessWidget {
  final String title,value;
  const MetricCard({super.key,required this.title,required this.value});
  @override Widget build(BuildContext context)=>Card(
    child:Padding(padding:const EdgeInsets.all(16),child:Column(children:[
      Text(title),const SizedBox(height:8),
      Text(value,style:const TextStyle(fontSize:28,fontWeight:FontWeight.bold))
    ]))
  );
}
