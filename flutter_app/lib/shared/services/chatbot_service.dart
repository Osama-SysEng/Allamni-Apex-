// Chatbot Service for Phase 5 Powerful AI Chatbot integration
import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../config/api_config.dart';

class ChatbotService {
  final Dio _dio;
  final FlutterSecureStorage _storage;
  
  ChatbotService({
    String? baseUrl,
    Dio? dio,
    FlutterSecureStorage? storage,
  })  : _dio = dio ?? Dio(BaseOptions(baseUrl: baseUrl ?? ApiConfig.aiBaseUrl)),
        _storage = storage ?? const FlutterSecureStorage();
  
  // Start a new conversation
  Future<ConversationResponse> startConversation({
    required String userId,
    required String contextType,
    required String topic,
    String dialect = 'modern_standard',
    String personality = 'friendly_tutor',
    List<String> skillCodes = const [],
    double userLevel = 0.5,
  }) async {
    try {
      final token = await _storage.read(key: 'access_token');
      
      final response = await _dio.post(
        '/chatbot/start',
        data: {
          'user_id': userId,
          'context_type': contextType,
          'topic': topic,
          'dialect': dialect,
          'personality': personality,
          'skill_codes': skillCodes,
          'user_level': userLevel,
        },
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },
        ),
      );
      
      return ConversationResponse.fromJson(response.data);
    } catch (e) {
      throw Exception('Failed to start conversation: $e');
    }
  }
  
  // Send a message to the chatbot
  Future<ChatbotMessageResponse> sendMessage({
    required String conversationId,
    required String userMessage,
    Map<String, dynamic>? additionalContext,
  }) async {
    try {
      final token = await _storage.read(key: 'access_token');
      
      final response = await _dio.post(
        '/chatbot/message',
        data: {
          'conversation_id': conversationId,
          'user_message': userMessage,
          'additional_context': additionalContext ?? {},
        },
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },
        ),
      );
      
      return ChatbotMessageResponse.fromJson(response.data);
    } catch (e) {
      throw Exception('Failed to send message: $e');
    }
  }
  
  // Get conversation summary
  Future<ConversationSummary> getConversationSummary(String conversationId) async {
    try {
      final token = await _storage.read(key: 'access_token');
      
      final response = await _dio.get(
        '/chatbot/conversation/$conversationId',
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
          },
        ),
      );
      
      return ConversationSummary.fromJson(response.data);
    } catch (e) {
      throw Exception('Failed to get conversation summary: $e');
    }
  }
  
  // Get conversation analytics for a user
  Future<ConversationAnalytics> getConversationAnalytics(String userId) async {
    try {
      final token = await _storage.read(key: 'access_token');
      
      final response = await _dio.get(
        '/chatbot/analytics/$userId',
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
          },
        ),
      );
      
      return ConversationAnalytics.fromJson(response.data);
    } catch (e) {
      throw Exception('Failed to get conversation analytics: $e');
    }
  }
}

// Chatbot models
class ConversationResponse {
  final String conversationId;
  final String status;
  
  ConversationResponse({
    required this.conversationId,
    required this.status,
  });
  
  factory ConversationResponse.fromJson(Map<String, dynamic> json) {
    return ConversationResponse(
      conversationId: json['conversation_id'],
      status: json['status'],
    );
  }
}

class ChatbotMessageResponse {
  final String content;
  final double confidence;
  final List<String> sources;
  final List<String> relatedTopics;
  final List<String> followUpQuestions;
  final String? difficultyLevel;
  final String? estimatedTime;
  
  ChatbotMessageResponse({
    required this.content,
    required this.confidence,
    required this.sources,
    required this.relatedTopics,
    required this.followUpQuestions,
    this.difficultyLevel,
    this.estimatedTime,
  });
  
  factory ChatbotMessageResponse.fromJson(Map<String, dynamic> json) {
    return ChatbotMessageResponse(
      content: json['content'] ?? '',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      sources: List<String>.from(json['sources'] ?? []),
      relatedTopics: List<String>.from(json['related_topics'] ?? []),
      followUpQuestions: List<String>.from(json['follow_up_questions'] ?? []),
      difficultyLevel: json['difficulty_level'],
      estimatedTime: json['estimated_time'],
    );
  }
}

class ConversationSummary {
  final String conversationId;
  final String userId;
  final String topic;
  final String contextType;
  final int messageCount;
  final String createdAt;
  final String lastActivity;
  final String summary;
  final List<String> learningGoals;
  final List<String> confusionPoints;
  final List<String> importantPoints;
  
  ConversationSummary({
    required this.conversationId,
    required this.userId,
    required this.topic,
    required this.contextType,
    required this.messageCount,
    required this.createdAt,
    required this.lastActivity,
    required this.summary,
    required this.learningGoals,
    required this.confusionPoints,
    required this.importantPoints,
  });
  
  factory ConversationSummary.fromJson(Map<String, dynamic> json) {
    return ConversationSummary(
      conversationId: json['conversation_id'],
      userId: json['user_id'],
      topic: json['topic'],
      contextType: json['context_type'],
      messageCount: json['message_count'] ?? 0,
      createdAt: json['created_at'],
      lastActivity: json['last_activity'],
      summary: json['summary'] ?? '',
      learningGoals: List<String>.from(json['learning_goals'] ?? []),
      confusionPoints: List<String>.from(json['confusion_points'] ?? []),
      importantPoints: List<String>.from(json['important_points'] ?? []),
    );
  }
}

class ConversationAnalytics {
  final int totalConversations;
  final int totalMessages;
  final double averageTurnsPerConversation;
  final int activeConversations;
  final List<String> topicsDiscussed;
  
  ConversationAnalytics({
    required this.totalConversations,
    required this.totalMessages,
    required this.averageTurnsPerConversation,
    required this.activeConversations,
    required this.topicsDiscussed,
  });
  
  factory ConversationAnalytics.fromJson(Map<String, dynamic> json) {
    return ConversationAnalytics(
      totalConversations: json['total_conversations'] ?? 0,
      totalMessages: json['total_messages'] ?? 0,
      averageTurnsPerConversation: (json['average_turns_per_conversation'] ?? 0.0).toDouble(),
      activeConversations: json['active_conversations'] ?? 0,
      topicsDiscussed: List<String>.from(json['topics_discussed'] ?? []),
    );
  }
}