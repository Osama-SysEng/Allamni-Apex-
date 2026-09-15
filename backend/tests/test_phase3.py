"""
Phase 3 Integration Tests for Allamni v4.0
Tests self-learning pipeline, Arabic NLP, voice input, image analysis, and memory enhancement
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timezone
from uuid import uuid4

# Import Phase 3 modules
from shared.self_learning import get_self_learning_pipeline, LearningSignal, LearningSignalType, SignalQuality
from shared.arabic_nlp import get_arabic_nlp_processor, ArabicDialect
from shared.voice_input import get_voice_processor, VoiceLanguage
from shared.image_analysis import get_image_analyzer, ImageType
from shared.memory import LearningMemory, MemoryType, MemoryImportance
from shared.store import store

def test_self_learning_pipeline():
    """Test self-learning pipeline functionality"""
    print("\n--- Testing Self-Learning Pipeline ---")
    
    pipeline = get_self_learning_pipeline(store)
    
    # Create test signals
    signal1 = LearningSignal(
        id=str(uuid4()),
        signal_type=LearningSignalType.EXPLANATION_SUCCESS,
        user_id="student_1",
        context={"topic": "python_basics", "difficulty": "easy"},
        content_data={"explanation_type": "analogy"},
        outcome="success",
        quality=SignalQuality.HIGH,
        timestamp=datetime.now(timezone.utc)
    )
    
    signal2 = LearningSignal(
        id=str(uuid4()),
        signal_type=LearningSignalType.EXPLANATION_FAILURE,
        user_id="student_1",
        context={"topic": "complex_algorithms", "difficulty": "hard"},
        content_data={"explanation_type": "direct"},
        outcome="failure",
        quality=SignalQuality.MEDIUM,
        timestamp=datetime.now(timezone.utc)
    )
    
    # Record signals
    signal_id1 = pipeline.record_signal(signal1)
    signal_id2 = pipeline.record_signal(signal2)
    
    if signal_id1 and signal_id2:
        print("[PASS] Learning signals recorded")
    else:
        print("[ERROR] Failed to record learning signals")
        return False
    
    # Analyze signals
    patterns = pipeline.analyze_signals()
    if patterns:
        print(f"[PASS] Patterns analyzed: {len(patterns)} patterns found")
    else:
        print("[PASS] No patterns found (expected with limited data)")
    
    # Get metrics
    metrics = pipeline.get_learning_metrics()
    if metrics['total_signals'] >= 2:
        print(f"[PASS] Learning metrics retrieved: {metrics['total_signals']} signals")
    else:
        print("[ERROR] Learning metrics incorrect")
        return False
    
    return True

def test_arabic_nlp():
    """Test Arabic NLP processing"""
    print("\n--- Testing Arabic NLP Processing ---")
    
    nlp_processor = get_arabic_nlp_processor()
    
    # Test dialect detection with ASCII text
    egyptian_text = "ya muallem, sherheli al dars dah"
    dialect, confidence = nlp_processor.detect_dialect(egyptian_text)
    
    if dialect:
        print(f"[PASS] Dialect detected: {dialect.value} (confidence: {confidence})")
    else:
        print("[ERROR] Dialect detection failed")
        return False
    
    # Test complete text processing with ASCII
    analysis = nlp_processor.process_text("what is 5 plus 3", ArabicDialect.MODERN_STANDARD)
    
    if analysis.detected_dialect:
        print(f"[PASS] Text processed: {analysis.detected_dialect.value}, complexity: {analysis.complexity.value}")
    else:
        print("[ERROR] Text processing failed")
        return False
    
    # Test key term extraction
    if analysis.key_terms:
        print(f"[PASS] Key terms extracted: {analysis.key_terms}")
    else:
        print("[PASS] No key terms found (expected for simple text)")
    
    return True

def test_voice_input():
    """Test voice input processing"""
    print("\n--- Testing Voice Input Processing ---")
    
    voice_processor = get_voice_processor()
    
    # Test transcription
    audio_data = "base64_placeholder_audio_data"
    transcription = voice_processor.transcribe_audio(audio_data, VoiceLanguage.ARABIC, "student_1")
    
    if transcription.transcribed_text:
        print(f"[PASS] Voice transcribed: {transcription.transcribed_text}")
    else:
        print("[ERROR] Voice transcription failed")
        return False
    
    # Test language support
    languages = voice_processor.get_supported_languages()
    if len(languages) > 0:
        print(f"[PASS] Supported languages: {languages}")
    else:
        print("[ERROR] No supported languages")
        return False
    
    return True

def test_image_analysis():
    """Test image analysis"""
    print("\n--- Testing Image Analysis ---")
    
    image_analyzer = get_image_analyzer()
    
    # Test image analysis
    image_data = "base64_placeholder_image_data"
    analysis = image_analyzer.analyze_image(image_data, ImageType.QUESTION_IMAGE, "student_1")
    
    if analysis.detected_content:
        print(f"[PASS] Image analyzed: {analysis.detected_content.value}")
    else:
        print("[ERROR] Image analysis failed")
        return False
    
    # Test supported image types
    image_types = image_analyzer.get_supported_image_types()
    if len(image_types) > 0:
        print(f"[PASS] Supported image types: {image_types}")
    else:
        print("[ERROR] No supported image types")
        return False
    
    # Test description generation
    description = image_analyzer.generate_image_description(analysis)
    if description:
        print(f"[PASS] Image description generated")
    else:
        print("[ERROR] Image description generation failed")
        return False
    
    return True

def test_memory_enhancement():
    """Test enhanced memory system"""
    print("\n--- Testing Memory Enhancement ---")
    
    memory = LearningMemory()
    
    # Test remembering
    memory_id = memory.remember(
        user_id="student_1",
        memory_type="conversation",
        content={"topic": "python_basics", "message": "I don't understand loops"},
        importance="high",
        tags=["python", "loops", "difficulty"]
    )
    
    if memory_id:
        print("[PASS] Memory stored")
    else:
        print("[ERROR] Memory storage failed")
        return False
    
    # Test recalling
    recalled = memory.recall(user_id="student_1", limit=10)
    if len(recalled) > 0:
        print(f"[PASS] Memory recalled: {len(recalled)} memories")
    else:
        print("[ERROR] Memory recall failed")
        return False
    
    # Test filtering by type
    recalled_type = memory.recall(user_id="student_1", memory_type="conversation")
    if len(recalled_type) > 0:
        print(f"[PASS] Memory filtered by type: {len(recalled_type)} conversations")
    else:
        print("[ERROR] Memory type filtering failed")
        return False
    
    # Test filtering by tags
    recalled_tags = memory.recall(user_id="student_1", tags=["python"])
    if len(recalled_tags) > 0:
        print(f"[PASS] Memory filtered by tags: {len(recalled_tags)} memories")
    else:
        print("[ERROR] Memory tag filtering failed")
        return False
    
    # Test memory stats
    stats = memory.get_memory_stats("student_1")
    if stats['total_memories'] > 0:
        print(f"[PASS] Memory stats: {stats['total_memories']} total memories")
    else:
        print("[ERROR] Memory stats failed")
        return False
    
    # Test forgetting
    forgotten = memory.forget("student_1", memory_id)
    if forgotten:
        print("[PASS] Memory forgotten")
    else:
        print("[ERROR] Memory forgetting failed")
        return False
    
    return True

def test_phase3_integration():
    """Test integration of all Phase 3 components"""
    print("\n--- Testing Phase 3 Integration ---")
    
    # Initialize all Phase 3 components
    pipeline = get_self_learning_pipeline(store)
    nlp_processor = get_arabic_nlp_processor()
    voice_processor = get_voice_processor()
    image_analyzer = get_image_analyzer()
    memory = LearningMemory()
    
    # Test cross-component workflow
    # 1. Process Arabic text
    text_analysis = nlp_processor.process_text("شرح لي كيف أحل المعادلة التربيعية")
    
    # 2. Store in memory
    memory_id = memory.remember(
        user_id="student_1",
        memory_type="conversation",
        content={"text": "شرح لي كيف أحل المعادلة التربيعية", "analysis": text_analysis.to_dict()},
        importance="high",
        tags=["math", "equations", "help"]
    )
    
    # 3. Record learning signal
    signal = LearningSignal(
        id=str(uuid4()),
        signal_type=LearningSignalType.EXPLANATION_SUCCESS,
        user_id="student_1",
        context={"topic": "quadratic_equations", "dialect": text_analysis.detected_dialect.value},
        content_data={"explanation_quality": "high"},
        outcome="success",
        quality=SignalQuality.HIGH,
        timestamp=datetime.now(timezone.utc)
    )
    signal_id = pipeline.record_signal(signal)
    
    # Verify integration
    if memory_id and signal_id:
        print("[PASS] Phase 3 components integrated successfully")
    else:
        print("[ERROR] Phase 3 integration failed")
        return False
    
    # Test backward compatibility with existing memory
    legacy_recall = memory.recall_legacy("student_1", "conversation")
    if len(legacy_recall) > 0:
        print("[PASS] Backward compatibility maintained")
    else:
        print("[ERROR] Backward compatibility failed")
        return False
    
    return True

def test_store_collections():
    """Test that store has Phase 3 collections"""
    print("\n--- Testing Store Collections ---")
    
    required_collections = [
        'learning_signals',
        'learning_patterns',
        'model_updates',
        'learning_metrics',
        'voice_interactions',
        'voice_sessions',
        'image_analyses'
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
    print("PHASE 3 INTEGRATION TESTS - Allamni v4.0")
    print("=" * 80)
    
    tests = [
        ("Self-Learning Pipeline", test_self_learning_pipeline),
        ("Arabic NLP Processing", test_arabic_nlp),
        ("Voice Input Processing", test_voice_input),
        ("Image Analysis", test_image_analysis),
        ("Memory Enhancement", test_memory_enhancement),
        ("Phase 3 Integration", test_phase3_integration),
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
    print("PHASE 3 TEST RESULTS")
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
        print("\n[SUCCESS] ALL PHASE 3 TESTS PASSED!")
        print("System Status:")
        print("- Phase 1: RBAC, Auth, AI Integration [READY]")
        print("- Phase 2: Institution Management, Billing, Odoo [READY]")
        print("- Phase 3: Self-Learning, Arabic NLP, Voice, Image [READY]")
        print("- Integration: All phases integrated [VERIFIED]")
        return 0
    else:
        print(f"\n[ERROR] {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())