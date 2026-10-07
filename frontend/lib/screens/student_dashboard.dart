import 'package:flutter/material.dart';
import '../services/api_service.dart';

class StudentDashboard extends StatefulWidget {
  final ApiService api;
  const StudentDashboard({super.key,required this.api});
  @override State<StudentDashboard> createState()=>_StudentDashboardState();
}
class _StudentDashboardState extends State<StudentDashboard> {
  Map<String,dynamic>? profile, action;
  bool loading=true;
  @override void initState(){super.initState();load();}
  Future<void> load() async {
    setState(()=>loading=true);
    try {
      final p=await widget.api.get('/api/learning/students/me');
      final a=await widget.api.get('/api/learning/students/me/next-best-action');
      setState(() { profile=p; action=a; });
    } catch(_) {} finally {if(mounted)setState(()=>loading=false);}
  }
  @override Widget build(BuildContext context) {
    final nodes=(profile?['roadmap']?['nodes'] as List?)??[];
    return Scaffold(
      appBar:AppBar(title:const Text('علّمني'),actions:[IconButton(onPressed:load,icon:const Icon(Icons.refresh))]),
      body:loading && profile==null
        ? const Center(child:CircularProgressIndicator())
        : RefreshIndicator(onRefresh:load,child:ListView(padding:const EdgeInsets.all(16),children:[
            const Text('أفضل خطوة تالية',style:TextStyle(fontSize:22,fontWeight:FontWeight.bold)),
            Card(child:ListTile(
              leading:const CircleAvatar(child:Icon(Icons.auto_awesome)),
              title:Text(action?['message']??'لا توجد توصية'),
              subtitle:Text((action?['reasons'] as List?)?.join(' • ')??''),
            )),
            const SizedBox(height:24),
            const Text('خارطة التعلم',style:TextStyle(fontSize:22,fontWeight:FontWeight.bold)),
            ...nodes.map((n)=>Card(child:ListTile(
              leading:CircleAvatar(child:Text('${n['sequence']}')),
              title:Text(n['title']??''),
              subtitle:Text('المستوى ${(100*(n['mastery_current']??0)).round()}% ← الهدف ${(100*(n['mastery_target']??0)).round()}%'),
              trailing:const Icon(Icons.chevron_left),
            ))),
          ]))
    );
  }
}
