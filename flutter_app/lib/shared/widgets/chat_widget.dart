// Enhanced Chat Widget based on best practices from open source projects
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/chatbot_service.dart';
import '../services/app_services.dart';
import '../../core/api/api_client.dart';

class ChatMessage {
  final String id;
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final String? dialect;
  
  ChatMessage({
    required this.id,
    required this.text,
    required this.isUser,
    required this.timestamp,
    this.dialect,
  });
}

class ChatWidget extends ConsumerStatefulWidget {
  final String userId;
  final String? initialDialect;
  final Function(String) onSendMessage;
  final Function()? onVoiceInput;
  
  const ChatWidget({
    super.key,
    required this.userId,
    this.initialDialect,
    required this.onSendMessage,
    this.onVoiceInput,
  });
  
  @override
  ConsumerState<ChatWidget> createState() => _ChatWidgetState();
}

class _ChatWidgetState extends ConsumerState<ChatWidget> {
  final TextEditingController _messageController = TextEditingController();
  final List<ChatMessage> _messages = [];
  String? _selectedDialect;
  bool _isTyping = false;
  String? _conversationId;
  ChatbotService? _chatbotService;
  
  @override
  void initState() {
    super.initState();
    _selectedDialect = widget.initialDialect;
    _initializeChatbot();
  }
  
  Future<void> _initializeChatbot() async {
    try {
      _chatbotService = ref.read(chatbotServiceProvider);
      
      // Start a new conversation
      final response = await _chatbotService!.startConversation(
        userId: widget.userId,
        contextType: 'learning',
        topic: 'general',
        dialect: _selectedDialect ?? 'modern_standard',
      );
      
      setState(() {
        _conversationId = response.conversationId;
      });
      
      // Add initial greeting
      _addInitialMessages();
    } catch (e) {
      // Fallback to local mode if API fails
      _addInitialMessages();
    }
  }
  
  void _addInitialMessages() {
    _messages.addAll([
      ChatMessage(
        id: '1',
        text: 'مرحباً! كيف يمكنني مساعدتك اليوم؟',
        isUser: false,
        timestamp: DateTime.now(),
        dialect: _selectedDialect,
      ),
    ]);
  }
  
  void _sendMessage() async {
    if (_messageController.text.trim().isEmpty) return;
    
    final userMessage = _messageController.text;
    
    setState(() {
      _messages.add(ChatMessage(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        text: userMessage,
        isUser: true,
        timestamp: DateTime.now(),
        dialect: _selectedDialect,
      ));
      _isTyping = true;
      _messageController.clear();
    });
    
    // Try to use real chatbot service
    try {
      if (_chatbotService != null && _conversationId != null) {
        final response = await _chatbotService!.sendMessage(
          conversationId: _conversationId!,
          userMessage: userMessage,
          additionalContext: {
            'dialect': _selectedDialect,
          },
        );
        
        if (mounted) {
          setState(() {
            _messages.add(ChatMessage(
              id: DateTime.now().millisecondsSinceEpoch.toString(),
              text: response.content,
              isUser: false,
              timestamp: DateTime.now(),
              dialect: _selectedDialect,
            ));
            _isTyping = false;
          });
        }
      } else {
        // Fallback to mock response
        _sendMockResponse();
      }
    } catch (e) {
      // Fallback to mock response on error
      _sendMockResponse();
    }
    
    widget.onSendMessage(userMessage);
  }
  
  void _sendMockResponse() {
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        setState(() {
          _messages.add(ChatMessage(
            id: DateTime.now().millisecondsSinceEpoch.toString(),
            text: 'أنا هنا لمساعدتك! اسألني أي سؤال عن البرمجة أو التعلم.',
            isUser: false,
            timestamp: DateTime.now(),
            dialect: _selectedDialect,
          ));
          _isTyping = false;
        });
      }
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Dialect selector
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: Colors.grey[100],
            border: const Border(bottom: BorderSide(color: Colors.grey)),
          ),
          child: Row(
            children: [
              const Icon(Icons.language, size: 20),
              const SizedBox(width: 8),
              DropdownButton<String>(
                value: _selectedDialect,
                hint: const Text('اختر اللهجة'),
                items: const [
                  DropdownMenuItem(value: 'modern_standard', child: Text('الفصحى الحديثة')),
                  DropdownMenuItem(value: 'egyptian', child: Text('مصرية')),
                  DropdownMenuItem(value: 'gulf', child: Text('خليجية')),
                  DropdownMenuItem(value: 'levantine', child: Text('شامية')),
                ],
                onChanged: (value) {
                  setState(() {
                    _selectedDialect = value;
                  });
                },
              ),
            ],
          ),
        ),
        
        // Chat messages
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: _messages.length + (_isTyping ? 1 : 0),
            itemBuilder: (context, index) {
              if (index == _messages.length && _isTyping) {
                return _buildTypingIndicator();
              }
              
              final message = _messages[index];
              return _buildMessageBubble(message);
            },
          ),
        ),
        
        // Input field
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity(0.1),
                spreadRadius: 1,
                blurRadius: 3,
              ),
            ],
          ),
          child: Row(
            children: [
              if (widget.onVoiceInput != null)
                IconButton(
                  icon: const Icon(Icons.mic),
                  onPressed: widget.onVoiceInput,
                ),
              Expanded(
                child: TextField(
                  controller: _messageController,
                  decoration: InputDecoration(
                    hintText: 'اكتب رسالتك هنا...',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(24),
                    ),
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 12,
                    ),
                  ),
                  onSubmitted: (_) => _sendMessage(),
                ),
              ),
              const SizedBox(width: 8),
              IconButton(
                icon: const Icon(Icons.send),
                onPressed: _sendMessage,
                style: IconButton.styleFrom(
                  backgroundColor: Theme.of(context).primaryColor,
                  foregroundColor: Colors.white,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
  
  Widget _buildMessageBubble(ChatMessage message) {
    return Align(
      alignment: message.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: message.isUser 
              ? Theme.of(context).primaryColor 
              : Colors.grey[200],
          borderRadius: BorderRadius.circular(16),
        ),
        constraints: const BoxConstraints(maxWidth: 280),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              message.text,
              style: TextStyle(
                color: message.isUser ? Colors.white : Colors.black87,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              _formatTime(message.timestamp),
              style: TextStyle(
                color: message.isUser ? Colors.white70 : Colors.black54,
                fontSize: 12,
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildTypingIndicator() {
    return const Align(
      alignment: Alignment.centerLeft,
      child: Padding(
        padding: EdgeInsets.only(bottom: 12),
        child: Row(
          children: [
            SizedBox(
              width: 24,
              height: 24,
              child: CircularProgressIndicator(strokeWidth: 2),
            ),
            SizedBox(width: 8),
            Text('جاري الكتابة...'),
          ],
        ),
      ),
    );
  }
  
  String _formatTime(DateTime time) {
    final now = DateTime.now();
    final difference = now.difference(time);
    
    if (difference.inMinutes < 1) {
      return 'الآن';
    } else if (difference.inHours < 1) {
      return 'منذ ${difference.inMinutes} دقيقة';
    } else if (difference.inDays < 1) {
      return 'منذ ${difference.inHours} ساعة';
    } else {
      return 'منذ ${difference.inDays} يوم';
    }
  }
  
  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }
}