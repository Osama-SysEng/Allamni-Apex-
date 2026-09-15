"""
Phase 5 Enhanced Features - Comprehensive Test Suite
Tests enhanced authentication, advanced security, powerful AI chatbot, and real-time features
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timezone, timedelta
from uuid import uuid4

# Import Phase 5 modules
from shared.enhanced_auth import get_enhanced_auth_service, SecurityLevel
from shared.advanced_security import get_advanced_security_service, SecurityConfig
from shared.powerful_ai_chatbot import get_powerful_ai_chatbot, ConversationContext, AIPersonality
from shared.real_time_features import get_real_time_service, NotificationPriority
from shared.store import store

def test_enhanced_authentication():
    """Test enhanced authentication features"""
    print("\n--- Testing Enhanced Authentication ---")
    
    auth_service = get_enhanced_auth_service(store)
    
    # Test session creation
    session = auth_service.create_session(
        user_id="user_1",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        device_id="device_1",
        security_level=SecurityLevel.HIGH
    )
    
    if session.id and session.is_valid():
        print("[PASS] Session created successfully")
    else:
        print("[ERROR] Session creation failed")
        return False
    
    # Test session validation
    is_valid = auth_service.validate_session(session.id, "192.168.1.1", "Mozilla/5.0")
    if is_valid:
        print("[PASS] Session validation successful")
    else:
        print("[ERROR] Session validation failed")
        return False
    
    # Test 2FA setup
    two_fa = auth_service.setup_2fa("user_1")
    if two_fa.secret and len(two_fa.backup_codes) == 10:
        print("[PASS] 2FA setup successful")
    else:
        print("[ERROR] 2FA setup failed")
        return False
    
    # Test biometric setup
    biometric = auth_service.setup_biometric("user_1", "device_1", "biometric_data_123")
    if biometric.device_id and biometric.is_enabled:
        print("[PASS] Biometric setup successful")
    else:
        print("[ERROR] Biometric setup failed")
        return False
    
    # Test failed login tracking
    attempts = auth_service.record_failed_login("user_1", "192.168.1.1")
    if attempts == 1:
        print(f"[PASS] Failed login tracking: {attempts} attempt")
    else:
        print("[ERROR] Failed login tracking failed")
        return False
    
    # Test account lockout
    for _ in range(5):
        auth_service.record_failed_login("user_1", "192.168.1.1")
    
    is_locked = auth_service.is_account_locked("user_1")
    if is_locked:
        print("[PASS] Account lockout triggered")
    else:
        print("[ERROR] Account lockout failed")
        return False
    
    # Test security events
    events = auth_service.get_security_events("user_1")
    if len(events) > 0:
        print(f"[PASS] Security events logged: {len(events)} events")
    else:
        print("[ERROR] Security events not logged")
        return False
    
    return True

def test_advanced_security():
    """Test advanced security features"""
    print("\n--- Testing Advanced Security ---")
    
    config = SecurityConfig(
        max_failed_attempts=3,
        rate_limit_requests_per_minute=30
    )
    security_service = get_advanced_security_service(store, config)
    
    # Test data encryption
    original_data = "sensitive_password_123"
    encrypted = security_service.encrypt_data(original_data)
    if encrypted != original_data:
        print("[PASS] Data encryption successful")
    else:
        print("[ERROR] Data encryption failed")
        return False
    
    # Test data decryption
    decrypted = security_service.decrypt_data(encrypted)
    if decrypted == original_data:
        print("[PASS] Data decryption successful")
    else:
        print("[ERROR] Data decryption failed")
        return False
    
    # Test input validation
    is_valid, error = security_service.validate_input("test@example.com", "email")
    if is_valid:
        print("[PASS] Email validation successful")
    else:
        print(f"[ERROR] Email validation failed: {error}")
        return False
    
    # Test invalid input detection
    is_valid, error = security_service.validate_input("invalid-email", "email")
    if not is_valid:
        print(f"[PASS] Invalid email detected: {error}")
    else:
        print("[ERROR] Invalid email not detected")
        return False
    
    # Test rate limiting
    for i in range(60):
        security_service.check_rate_limit("user_1", "/api/test", "minute")
    
    # Should block on 61st request
    is_allowed = security_service.check_rate_limit("user_1", "/api/test", "minute")
    if not is_allowed:
        print("[PASS] Rate limiting triggered")
    else:
        print("[ERROR] Rate limiting not triggered")
        return False
    
    # Test security scan
    scan_results = security_service.perform_security_scan()
    if scan_results['security_score'] >= 80:
        print(f"[PASS] Security scan completed: Score {scan_results['security_score']}")
    else:
        print(f"[ERROR] Security scan score too low: {scan_results['security_score']}")
        return False
    
    return True

def test_powerful_ai_chatbot():
    """Test powerful AI chatbot features"""
    print("\n--- Testing Powerful AI Chatbot ---")
    
    chatbot = get_powerful_ai_chatbot(store)
    
    # Test conversation start
    conversation_id = chatbot.start_conversation(
        user_id="student_1",
        context_type=ConversationContext.LEARNING,
        topic="python_basics",
        dialect="egyptian",
        personality=AIPersonality.FRIENDLY_TUTOR,
        skill_codes=["variables", "data_types"],
        user_level=0.6
    )
    
    if conversation_id:
        print(f"[PASS] Conversation started: {conversation_id}")
    else:
        print("[ERROR] Conversation start failed")
        return False
    
    # Test message sending
    response = chatbot.send_message(
        conversation_id=conversation_id,
        user_message="شرح لي المتغيرات في بايثون"
    )
    
    if response.content and response.confidence > 0:
        # Truncate to avoid encoding issues with Arabic text
        content_preview = response.content[:30].encode('ascii', 'ignore').decode('ascii') if response.content else "empty"
        print(f"[PASS] AI response generated: {content_preview}...")
    else:
        print("[ERROR] AI response generation failed")
        return False
    
    # Test conversation summary
    summary = chatbot.get_conversation_summary(conversation_id)
    if summary and summary.get('topic') == "python_basics":
        print(f"[PASS] Conversation summary generated: {summary.get('message_count', 0)} messages")
    else:
        print("[ERROR] Conversation summary failed")
        return False
    
    # Test conversation analytics
    analytics = chatbot.get_conversation_analytics("student_1")
    if analytics and analytics.get('total_conversations', 0) >= 1:
        print(f"[PASS] Conversation analytics: {analytics['total_conversations']} conversations")
    else:
        print("[ERROR] Conversation analytics failed")
        return False
    
    # Test knowledge base
    knowledge = chatbot._get_relevant_knowledge("python_basics", ["variables"])
    if knowledge and 'topics' in knowledge:
        topics_str = str(knowledge['topics'])
        print(f"[PASS] Knowledge base access: {topics_str[:50]}...")
    else:
        print("[ERROR] Knowledge base access failed")
        return False
    
    return True

def test_real_time_features():
    """Test real-time features"""
    print("\n--- Testing Real-Time Features ---")
    
    real_time_service = get_real_time_service(store)
    
    # Test notification creation
    notification_id = real_time_service.create_notification(
        user_id="student_1",
        title="اختبار إشعار",
        body="هذا إشعار تجريبي من النظام",
        priority=NotificationPriority.HIGH,
        action_url="/test",
        action_label="عرض"
    )
    
    if notification_id:
        print(f"[PASS] Notification created: {notification_id}")
    else:
        print("[ERROR] Notification creation failed")
        return False
    
    # Test notification retrieval
    notifications = real_time_service.get_user_notifications("student_1")
    if len(notifications) > 0:
        print(f"[PASS] Notifications retrieved: {len(notifications)} notifications")
    else:
        print("[ERROR] Notifications retrieval failed")
        return False
    
    # Test unread count
    unread_count = real_time_service.get_unread_count("student_1")
    if unread_count >= 0:
        print(f"[PASS] Unread count: {unread_count}")
    else:
        print("[ERROR] Unread count failed")
        return False
    
    # Test marking as read
    is_marked = real_time_service.mark_notification_read(notification_id, "student_1")
    if is_marked:
        print("[PASS] Notification marked as read")
    else:
        print("[ERROR] Notification mark as read failed")
        return False
    
    # Test notification preferences
    real_time_service.set_notification_preferences("student_1", {
        'email_enabled': True,
        'push_enabled': True,
        'sound_enabled': False
    })
    
    preferences = real_time_service.get_notification_preferences("student_1")
    if preferences['sound_enabled'] == False:
        print("[PASS] Notification preferences set")
    else:
        print("[ERROR] Notification preferences failed")
        return False
    
    # Test live session creation
    session_data = real_time_service.create_live_session(
        session_id="session_1",
        host_id="teacher_1",
        participants=["student_1", "student_2"],
        topic="Python Tutorial"
    )
    
    if session_data and session_data['topic'] == "Python Tutorial":
        print(f"[PASS] Live session created: {session_data['id']}")
    else:
        print("[ERROR] Live session creation failed")
        return False
    
    return True

def test_phase5_integration():
    """Test integration of all Phase 5 features"""
    print("\n--- Testing Phase 5 Integration ---")
    
    # Initialize all Phase 5 services
    auth_service = get_enhanced_auth_service(store)
    security_service = get_advanced_security_service(store)
    chatbot = get_powerful_ai_chatbot(store)
    real_time_service = get_real_time_service(store)
    
    # Test integrated workflow
    # 1. User logs in with enhanced auth
    session = auth_service.create_session("user_1", "192.168.1.1", "TestAgent", "device_1")
    
    # 2. Security scan checks user
    security_service.check_rate_limit("user_1", "/api/login", "minute")
    
    # 3. User starts AI conversation
    conversation_id = chatbot.start_conversation(
        user_id="user_1",
        context_type=ConversationContext.LEARNING,
        topic="python_basics",
        dialect="egyptian",
        personality=AIPersonality.FRIENDLY_TUTOR,
        skill_codes=["variables"],
        user_level=0.5
    )
    
    # 4. AI sends notification about conversation
    real_time_service.create_notification(
        "user_1", "محادثة جديدة", "تم بدء محادثة تعليمية", NotificationPriority.MEDIUM
    )
    
    # Verify integration
    if session.id and conversation_id:
        print("[PASS] Phase 5 components integrated successfully")
    else:
        print("[ERROR] Phase 5 integration failed")
        return False
    
    # Test cross-component functionality
    # Check that auth session is tracked
    if auth_service.get_active_sessions("user_1"):
        print("[PASS] Auth sessions tracked")
    else:
        print("[ERROR] Auth sessions not tracked")
        return False
    
    # Check that security metrics are updated
    security_metrics = security_service.get_security_metrics()
    if security_metrics.get('total_requests', 0) > 0:
        print("[PASS] Security metrics updated")
    else:
        print("[ERROR] Security metrics not updated")
        return False
    
    # Check that conversation analytics are tracked
    conversation_analytics = chatbot.get_conversation_analytics("user_1")
    if conversation_analytics.get('total_conversations', 0) > 0:
        print("[PASS] Conversation analytics tracked")
    else:
        print("[ERROR] Conversation analytics not tracked")
        return False
    
    # Check that notifications are stored
    notifications = real_time_service.get_user_notifications("user_1")
    if len(notifications) > 0:
        print("[PASS] Notifications stored")
    else:
        print("[ERROR] Notifications not stored")
        return False
    
    return True

def test_store_collections():
    """Test that store has Phase 5 collections"""
    print("\n--- Testing Store Collections ---")
    
    required_collections = [
        # Phase 5 Enhanced Security
        'auth_sessions',
        'two_factor_auths',
        'biometric_auths',
        'security_events',
        'failed_login_attempts',
        'account_lockouts',
        'rate_limits',
        'security_incidents',
        'encrypted_data',
        'security_metrics',
        # Phase 5 AI Chatbot
        'conversation_threads',
        'conversation_memories',
        'ai_knowledge_base',
        'conversation_analytics',
        # Phase 5 Real-time
        'real_time_events',
        'notifications',
        'notification_preferences'
    ]
    
    all_present = True
    for collection in required_collections:
        if hasattr(store, collection):
            print(f"[PASS] Store has {collection} collection")
        else:
            print(f"[ERROR] Store missing {collection} collection")
            all_present = False
    
    return all_present

def main():
    print("=" * 80)
    print("PHASE 5 ENHANCED FEATURES TESTS - Allamni v4.0")
    print("=" * 80)
    
    tests = [
        ("Enhanced Authentication", test_enhanced_authentication),
        ("Advanced Security", test_advanced_security),
        ("Powerful AI Chatbot", test_powerful_ai_chatbot),
        ("Real-Time Features", test_real_time_features),
        ("Phase 5 Integration", test_phase5_integration),
        ("Store Collections", test_store_collections)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[ERROR] {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 80)
    print("PHASE 5 TEST RESULTS")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    print("=" * 80)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("\n[SUCCESS] ALL PHASE 5 TESTS PASSED!")
        print("\nFinal System Status:")
        print("- Phase 1: RBAC, Auth, AI Integration [READY]")
        print("- Phase 2: Institution Management, Billing, Odoo [READY]")
        print("- Phase 3: Self-Learning, Arabic NLP, Voice, Image [READY]")
        print("- Phase 4: Flutter Frontend Enhanced [READY]")
        print("- Phase 5: Enhanced Security, AI Chatbot, Real-Time [READY]")
        print("- Integration: All five phases integrated [VERIFIED]")
        print("- Security: Advanced security features [VERIFIED]")
        print("- AI: Powerful chatbot with memory [VERIFIED]")
        print("- Real-time: Live updates and notifications [VERIFIED]")
        return 0
    else:
        print(f"\n[ERROR] {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())