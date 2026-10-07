// Side Chat Panel for Phase 5 - Persistent AI chatbot interface
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'chat_widget.dart';

class SideChatPanel extends ConsumerStatefulWidget {
  final String userId;
  final String? initialDialect;
  final Function(String)? onSendMessage;
  final Function()? onVoiceInput;
  
  const SideChatPanel({
    super.key,
    required this.userId,
    this.initialDialect,
    this.onSendMessage,
    this.onVoiceInput,
  });
  
  @override
  ConsumerState<SideChatPanel> createState() => _SideChatPanelState();
}

class _SideChatPanelState extends ConsumerState<SideChatPanel> {
  bool _isExpanded = false;
  
  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      width: _isExpanded ? 350 : 60,
      curve: Curves.easeInOut,
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 10,
              spreadRadius: 2,
            ),
          ],
          borderRadius: BorderRadius.circular(16),
        ),
        child: _isExpanded ? _buildExpandedPanel() : _buildCollapsedPanel(),
      ),
    );
  }
  
  Widget _buildCollapsedPanel() {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () {
          setState(() {
            _isExpanded = true;
          });
        },
        borderRadius: BorderRadius.circular(16),
        child: const Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.chat_bubble_outline,
              size: 28,
              color: Colors.blue,
            ),
            SizedBox(height: 4),
            Text(
              'AI',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.bold,
                color: Colors.blue,
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildExpandedPanel() {
    return Column(
      children: [
        // Header
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            color: Theme.of(context).primaryColor,
            borderRadius: const BorderRadius.only(
              topLeft: Radius.circular(16),
              topRight: Radius.circular(16),
            ),
          ),
          child: Row(
            children: [
              const Icon(
                Icons.smart_toy,
                color: Colors.white,
                size: 20,
              ),
              const SizedBox(width: 8),
              const Expanded(
                child: Text(
                  'المعلم الذكي',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
              ),
              IconButton(
                icon: const Icon(Icons.close, color: Colors.white),
                onPressed: () {
                  setState(() {
                    _isExpanded = false;
                  });
                },
                padding: EdgeInsets.zero,
                constraints: const BoxConstraints(),
              ),
            ],
          ),
        ),
        
        // Chat content
        Expanded(
          child: ChatWidget(
            userId: widget.userId,
            initialDialect: widget.initialDialect,
            onSendMessage: widget.onSendMessage,
            onVoiceInput: widget.onVoiceInput,
          ),
        ),
      ],
    );
  }
}