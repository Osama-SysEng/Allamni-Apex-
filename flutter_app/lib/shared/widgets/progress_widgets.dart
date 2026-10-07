// Progress Tracking Widget based on Spaced Repetition concepts
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class SkillProgressWidget extends StatelessWidget {
  final String skillName;
  final double currentLevel;
  final double targetLevel;
  final int completedItems;
  final int totalItems;
  final List<ProgressMilestone>? milestones;
  
  const SkillProgressWidget({
    super.key,
    required this.skillName,
    required this.currentLevel,
    required this.targetLevel,
    required this.completedItems,
    required this.totalItems,
    this.milestones,
  });
  
  @override
  Widget build(BuildContext context) {
    final progress = totalItems > 0 ? completedItems / totalItems : 0.0;
    final gap = targetLevel - currentLevel;
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  skillName,
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                _buildLevelBadge(currentLevel),
              ],
            ),
            const SizedBox(height: 16),
            
            // Progress bar
            LinearProgressIndicator(
              value: progress,
              backgroundColor: Colors.grey[200],
              valueColor: AlwaysStoppedAnimation<Color>(
                _getProgressColor(progress),
              ),
            ),
            const SizedBox(height: 8),
            
            // Progress details
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('$completedItems/$totalItems مكتمل'),
                Text('${(progress * 100).toInt()}%'),
              ],
            ),
            
            if (gap > 0) ...[
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.orange[50],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.trending_up, color: Colors.orange, size: 16),
                    const SizedBox(width: 4),
                    Text(
                      'الفرق: ${gap.toStringAsFixed(1)} مستوى',
                      style: const TextStyle(color: Colors.orange),
                    ),
                  ],
                ),
              ),
            ],
            
            if (milestones != null && milestones!.isNotEmpty) ...[
              const SizedBox(height: 16),
              _buildMilestonesTimeline(),
            ],
          ],
        ),
      ),
    );
  }
  
  Widget _buildLevelBadge(double level) {
    Color color;
    String label;
    
    if (level >= 0.8) {
      color = Colors.green;
      label = 'متقدم';
    } else if (level >= 0.5) {
      color = Colors.blue;
      label = 'متوسط';
    } else {
      color = Colors.orange;
      label = 'مبتدئ';
    }
    
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        label,
        style: const TextStyle(color: Colors.white, fontSize: 12),
      ),
    );
  }
  
  Color _getProgressColor(double progress) {
    if (progress >= 0.8) return Colors.green;
    if (progress >= 0.5) return Colors.blue;
    if (progress >= 0.3) return Colors.orange;
    return Colors.red;
  }
  
  Widget _buildMilestonesTimeline() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'المحطات الرئيسية',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        ...milestones!.map((milestone) => _buildMilestoneItem(milestone)),
      ],
    );
  }
  
  Widget _buildMilestoneItem(ProgressMilestone milestone) {
    final isCompleted = milestone.isCompleted;
    
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        children: [
          Icon(
            isCompleted ? Icons.check_circle : Icons.radio_button_unchecked,
            color: isCompleted ? Colors.green : Colors.grey,
            size: 20,
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              milestone.title,
              style: TextStyle(
                decoration: isCompleted ? TextDecoration.lineThrough : null,
                color: isCompleted ? Colors.grey : Colors.black87,
              ),
            ),
          ),
          if (milestone.dueDate != null)
            Text(
              _formatDate(milestone.dueDate!),
              style: TextStyle(
                color: isCompleted ? Colors.grey : Colors.black54,
                fontSize: 12,
              ),
            ),
        ],
      ),
    );
  }
  
  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }
}

class ProgressMilestone {
  final String title;
  final bool isCompleted;
  final DateTime? dueDate;
  
  ProgressMilestone({
    required this.title,
    required this.isCompleted,
    this.dueDate,
  });
}

class SimpleRadarChartWidget extends StatelessWidget {
  final Map<String, double> skills;
  
  const SimpleRadarChartWidget({super.key, required this.skills});
  
  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text(
              'نظرة عامة على المهارات',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 200,
              child: RadarChart(
                RadarChartData(
                  dataSets: [
                    RadarDataSet(
                      data: [
                        for (var entry in skills.entries)
                          RadarValue(value: entry.value),
                      ],
                      borderColor: Theme.of(context).primaryColor,
                      borderWidth: 2,
                      fillColor: Theme.of(context).primaryColor.withOpacity(0.2),
                    ),
                  ],
                  titles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      getTitlesWidget: (index, angle) {
                        final keys = skills.keys.toList();
                        if (index < keys.length) {
                          return Text(
                            keys[index],
                            style: const TextStyle(fontSize: 10),
                          );
                        }
                        return const Text('');
                      },
                    ),
                  ),
                  gridBorderData: const FlGridBorder(show: false),
                  borderData: FlBorderData(show: false),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}