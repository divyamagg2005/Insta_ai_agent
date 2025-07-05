#!/usr/bin/env python3
"""
Example showing how subtitle timing works
"""

def demonstrate_timing():
    """Show how subtitle timing is calculated"""
    
    print("⏱️ Subtitle Timing Example")
    print("=" * 50)
    
    # Sample script
    script = "Today I learned about machine learning. Supervised learning uses labeled data. Unsupervised learning finds patterns."
    
    print(f"📝 Script: {script}")
    print(f"📊 Total words: {len(script.split())}")
    print(f"⏰ Audio duration: 15 seconds")
    print()
    
    # Calculate timing
    total_words = len(script.split())
    audio_duration = 15
    words_per_second = total_words / audio_duration
    
    print("🔢 Timing Calculation:")
    print(f"   Words per second: {words_per_second:.2f}")
    print()
    
    # Split into sentences
    sentences = script.split('. ')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    print("📋 Subtitle Chunks:")
    current_time = 0
    
    for i, sentence in enumerate(sentences):
        sentence_words = len(sentence.split())
        sentence_duration = sentence_words / words_per_second
        
        # Apply min/max constraints
        min_duration = 1.0
        max_duration = 4.0
        gap = 0.2
        
        actual_duration = max(min_duration, min(sentence_duration, max_duration))
        
        print(f"   Chunk {i+1}: '{sentence}'")
        print(f"      Words: {sentence_words}")
        print(f"      Calculated duration: {sentence_duration:.2f}s")
        print(f"      Actual duration: {actual_duration:.2f}s")
        print(f"      Start time: {current_time:.1f}s")
        print(f"      End time: {current_time + actual_duration:.1f}s")
        print()
        
        current_time += actual_duration + gap
    
    print("⚙️ Timing Settings Impact:")
    print("   • Min Duration (1.0s): Ensures short sentences get enough screen time")
    print("   • Max Duration (4.0s): Prevents long sentences from dominating")
    print("   • Gap (0.2s): Creates clear separation between subtitles")
    print()
    
    print("🎯 Timing Scenarios:")
    print()
    
    # Scenario 1: Fast speech
    print("📈 Fast Speech (3 words/second):")
    fast_script = "AI is amazing. It learns quickly. Neural networks work well."
    fast_words = len(fast_script.split())
    fast_duration = 10  # 10 seconds
    fast_wps = fast_words / fast_duration
    
    print(f"   Script: {fast_script}")
    print(f"   Words per second: {fast_wps:.2f}")
    print(f"   Result: Shorter subtitle durations")
    print()
    
    # Scenario 2: Slow speech
    print("📉 Slow Speech (1.5 words/second):")
    slow_script = "Today I learned about artificial intelligence and machine learning algorithms."
    slow_words = len(slow_script.split())
    slow_duration = 15  # 15 seconds
    slow_wps = slow_words / slow_duration
    
    print(f"   Script: {slow_script}")
    print(f"   Words per second: {slow_wps:.2f}")
    print(f"   Result: Longer subtitle durations")
    print()
    
    print("💡 Tips for Timing Settings:")
    print("   • For fast speakers: Increase min duration to 1.5-2.0s")
    print("   • For slow speakers: Decrease max duration to 3.0-3.5s")
    print("   • For complex content: Increase gap to 0.3-0.5s")
    print("   • For simple content: Decrease gap to 0.1-0.2s")

def show_timing_formula():
    """Show the mathematical formula for timing calculation"""
    print("\n🧮 Timing Formula:")
    print("=" * 30)
    print("1. Calculate words per second:")
    print("   words_per_second = total_words / audio_duration")
    print()
    print("2. For each sentence:")
    print("   sentence_duration = sentence_words / words_per_second")
    print()
    print("3. Apply constraints:")
    print("   actual_duration = max(min_duration, min(sentence_duration, max_duration))")
    print()
    print("4. Add gap between subtitles:")
    print("   next_start_time = current_time + actual_duration + gap")

if __name__ == "__main__":
    demonstrate_timing()
    show_timing_formula() 