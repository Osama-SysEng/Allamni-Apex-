import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../shared/providers/auth_provider.dart';

class TeacherDashboardScreen extends ConsumerStatefulWidget {
  const TeacherDashboardScreen({super.key});

  @override
  ConsumerState<TeacherDashboardScreen> createState() => _TeacherDashboardScreenState();
}

class _TeacherDashboardScreenState extends ConsumerState<TeacherDashboardScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const TeacherHomeScreen(),
    const TeacherStudentsScreen(),
    const TeacherContentScreen(),
    const TeacherProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        type: BottomNavigationBarType.fixed,
        items: [
          BottomNavigationBarItem(
            icon: const Icon(Icons.dashboard),
            label: 'dashboard'.tr(),
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.people),
            label: 'students'.tr(),
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.edit_note),
            label: 'content'.tr(),
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.person),
            label: 'profile'.tr(),
          ),
        ],
      ),
    );
  }
}

class TeacherHomeScreen extends StatelessWidget {
  const TeacherHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('teacher_dashboard'.tr()),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications),
            onPressed: () {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Stats cards
            Row(
              children: [
                Expanded(
                  child: _buildStatCard('total_students'.tr(), '150', Icons.people, Colors.blue),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: _buildStatCard('active_students'.tr(), '120', Icons.trending_up, Colors.green),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _buildStatCard('lessons_created'.tr(), '45', Icons.edit, Colors.orange),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: _buildStatCard('assessments_created'.tr(), '20', Icons.quiz, Colors.purple),
                ),
              ],
            ),
            const SizedBox(height: 24),
            
            // Recent activity
            Text(
              'recent_activity'.tr(),
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            _buildActivityCard('student_completed_lesson'.tr(), 'Ahmed - Python Basics'),
            _buildActivityCard('student_submitted_assessment'.tr(), 'Sara - Data Structures'),
            _buildActivityCard('student_asked_question'.tr(), 'Mohamed - Python Loops'),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 8),
            Text(
              value,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              title,
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActivityCard(String title, String subtitle) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: const Icon(Icons.history),
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: Text('2h ago'),
      ),
    );
  }
}

class TeacherStudentsScreen extends StatelessWidget {
  const TeacherStudentsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('students'.tr()),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildStudentCard('Ahmed Mohamed', 'Grade 10', 'Python', 0.85),
          _buildStudentCard('Sara Ali', 'Grade 11', 'Data Structures', 0.72),
          _buildStudentCard('Mohamed Hassan', 'Grade 10', 'Algorithms', 0.65),
          _buildStudentCard('Fatima Ahmed', 'Grade 12', 'Databases', 0.90),
        ],
      ),
    );
  }

  Widget _buildStudentCard(String name, String grade, String currentLesson, double progress) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: const CircleAvatar(child: Icon(Icons.person)),
        title: Text(name),
        subtitle: Text('$grade - $currentLesson'),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('${(progress * 100).toInt()}%'),
            SizedBox(
              width: 50,
              child: LinearProgressIndicator(value: progress),
            ),
          ],
        ),
        onTap: () {},
      ),
    );
  }
}

class TeacherContentScreen extends StatelessWidget {
  const TeacherContentScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('content_management'.tr()),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () {},
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildContentCard('Python Basics', 'Lesson', 'Published', Icons.play_circle),
          _buildContentCard('Data Structures', 'Course', 'Published', Icons.library_books),
          _buildContentCard('Algorithms Quiz', 'Assessment', 'Draft', Icons.quiz),
          _buildContentCard('Problem Solving', 'Exercise', 'Published', Icons.assignment),
        ],
      ),
    );
  }

  Widget _buildContentCard(String title, String type, String status, IconData icon) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: Icon(icon),
        title: Text(title),
        subtitle: Text('$type - $status'),
        trailing: IconButton(
          icon: const Icon(Icons.more_vert),
          onPressed: () {},
        ),
        onTap: () {},
      ),
    );
  }
}

class TeacherProfileScreen extends ConsumerWidget {
  const TeacherProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);
    
    return Scaffold(
      appBar: AppBar(
        title: Text('profile'.tr()),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await ref.read(authProvider.notifier).logout();
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const CircleAvatar(
              radius: 50,
              child: Icon(Icons.person, size: 50),
            ),
            const SizedBox(height: 16),
            Text(
              authState.userId ?? 'Unknown',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            Text(
              authState.userRole ?? 'Teacher',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 24),
            Card(
              child: Column(
                children: [
                  ListTile(
                    leading: const Icon(Icons.edit),
                    title: Text('edit_profile'.tr()),
                    trailing: const Icon(Icons.arrow_forward_ios),
                    onTap: () {},
                  ),
                  ListTile(
                    leading: const Icon(Icons.settings),
                    title: Text('settings'.tr()),
                    trailing: const Icon(Icons.arrow_forward_ios),
                    onTap: () {},
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}