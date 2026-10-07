import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../shared/providers/auth_provider.dart';

class AdminDashboardScreen extends ConsumerStatefulWidget {
  const AdminDashboardScreen({super.key});

  @override
  ConsumerState<AdminDashboardScreen> createState() => _AdminDashboardScreenState();
}

class _AdminDashboardScreenState extends ConsumerState<AdminDashboardScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const AdminHomeScreen(),
    const AdminInstitutionScreen(),
    const AdminBillingScreen(),
    const AdminProfileScreen(),
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
            icon: const Icon(Icons.business),
            label: 'institution'.tr(),
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.payment),
            label: 'billing'.tr(),
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

class AdminHomeScreen extends StatelessWidget {
  const AdminHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('admin_dashboard'.tr()),
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
            // Institution overview
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'institution_overview'.tr(),
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Expanded(
                          child: _buildAdminStatCard('total_students'.tr(), '500', Icons.people, Colors.blue),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: _buildAdminStatCard('total_teachers'.tr(), '45', Icons.school, Colors.green),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Expanded(
                          child: _buildAdminStatCard('active_courses'.tr(), '25', Icons.book, Colors.orange),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: _buildAdminStatCard('completion_rate'.tr(), '78%', Icons.trending_up, Colors.purple),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            
            // Subscription status
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'subscription_status'.tr(),
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 16),
                    ListTile(
                      leading: const Icon(Icons.check_circle, color: Colors.green),
                      title: Text('plan'.tr()),
                      subtitle: Text('Professional Plan'),
                      trailing: Chip(
                        label: Text('active'.tr()),
                        backgroundColor: Colors.green[100],
                      ),
                    ),
                    ListTile(
                      leading: const Icon(Icons.calendar_today),
                      title: Text('renewal_date'.tr()),
                      subtitle: Text('2024-12-31'),
                    ),
                    ListTile(
                      leading: const Icon(Icons.people),
                      title: Text('usage'.tr()),
                      subtitle: Text('450/500 students'),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            
            // Quick actions
            Text(
              'quick_actions'.tr(),
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _buildQuickActionCard('generate_codes'.tr(), Icons.code, () {}),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: _buildQuickActionCard('view_reports'.tr(), Icons.analytics, () {}),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAdminStatCard(String title, String value, IconData icon, Color color) {
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

  Widget _buildQuickActionCard(String title, IconData icon, VoidCallback onTap) {
    return Card(
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Icon(icon, size: 32),
              const SizedBox(height: 8),
              Text(title),
            ],
          ),
        ),
      ),
    );
  }
}

class AdminInstitutionScreen extends StatelessWidget {
  const AdminInstitutionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('institution_management'.tr()),
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
          _buildInstitutionCard('Generate Student Codes', Icons.person_add, () {}),
          _buildInstitutionCard('Generate Teacher Codes', Icons.school, () {}),
          _buildInstitutionCard('View All Codes', Icons.list, () {}),
          _buildInstitutionCard('Institution Settings', Icons.settings, () {}),
        ],
      ),
    );
  }

  Widget _buildInstitutionCard(String title, IconData icon, VoidCallback onTap) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: Icon(icon),
        title: Text(title),
        trailing: const Icon(Icons.arrow_forward_ios),
        onTap: onTap,
      ),
    );
  }
}

class AdminBillingScreen extends StatelessWidget {
  const AdminBillingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('billing_management'.tr()),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'current_invoice'.tr(),
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 16),
                  ListTile(
                    title: Text('invoice_number'.tr()),
                    subtitle: Text('INV-202409-1234'),
                  ),
                  ListTile(
                    title: Text('amount'.tr()),
                    subtitle: Text('\$1,200.00'),
                  ),
                  ListTile(
                    title: Text('due_date'.tr()),
                    subtitle: Text('2024-10-15'),
                  ),
                  ListTile(
                    title: Text('status'.tr()),
                    subtitle: Text('Pending'),
                    trailing: Chip(
                      label: Text('pending'.tr()),
                      backgroundColor: Colors.orange[100],
                    ),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {},
                    child: Text('pay_now'.tr()),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: ListTile(
              title: Text('payment_history'.tr()),
              trailing: const Icon(Icons.arrow_forward_ios),
              onTap: () {},
            ),
          ),
        ],
      ),
    );
  }
}

class AdminProfileScreen extends ConsumerWidget {
  const AdminProfileScreen({super.key});

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
              child: Icon(Icons.admin_panel_settings, size: 50),
            ),
            const SizedBox(height: 16),
            Text(
              authState.userId ?? 'Unknown',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            Text(
              authState.userRole ?? 'Admin',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 24),
            Card(
              child: Column(
                children: [
                  ListTile(
                    leading: const Icon(Icons.business),
                    title: Text('institution_settings'.tr()),
                    trailing: const Icon(Icons.arrow_forward_ios),
                    onTap: () {},
                  ),
                  ListTile(
                    leading: const Icon(Icons.security),
                    title: Text('security_settings'.tr()),
                    trailing: const Icon(Icons.arrow_forward_ios),
                    onTap: () {},
                  ),
                  ListTile(
                    leading: const Icon(Icons.integration_instructions),
                    title: Text('integrations'.tr()),
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