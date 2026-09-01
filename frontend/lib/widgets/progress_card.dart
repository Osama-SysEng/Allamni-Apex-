import 'package:flutter/material.dart';
class ProgressCard extends StatelessWidget {
  final String title; final double value;
  const ProgressCard({super.key,required this.title,required this.value});
  @override Widget build(BuildContext context)=>Card(child:Padding(
    padding:const EdgeInsets.all(16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
      Text(title),const SizedBox(height:8),
      LinearProgressIndicator(value:value.clamp(0,1)),const SizedBox(height:6),
      Text('${(value*100).round()}%')
    ])));
}
