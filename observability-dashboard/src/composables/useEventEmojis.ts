const eventTypeToEmoji: Record<string, string> = {
  // Original hook types
  'PreToolUse': '🔧',
  'PostToolUse': '✅',
  'Notification': '🔔',
  'Stop': '🛑',
  'SubagentStop': '👥',
  'PreCompact': '📦',
  'UserPromptSubmit': '💬',
  'SessionStart': '🚀',
  'SessionEnd': '🏁',
  
  // Feedback Loop Workflow events
  'ocr_started': '📷',
  'ocr_completed': '👁️',
  'concept_match_started': '🎯',
  'concept_match_completed': '🧠',
  'pattern_query_started': '🔍',
  'pattern_query_completed': '💭',
  'scaffolding_started': '🏗️',
  'scaffolding_completed': '📝',
  'feedback_started': '💬',
  'feedback_step_collected': '⭐',
  'feedback_completed': '✅',
  'learning_started': '📚',
  'pattern_extracted': '💡',
  'learning_completed': '🧠',
  'neo4j_write_started': '💾',
  'neo4j_write_completed': '🗄️',
  'validation_completed': '✅',
  
  // Test events
  'test_event': '🧪',
  
  // Default
  'default': '❓'
};

export function useEventEmojis() {
  const getEmojiForEventType = (eventType: string): string => {
    return eventTypeToEmoji[eventType] || eventTypeToEmoji.default;
  };
  
  const formatEventTypeLabel = (eventTypes: Record<string, number>): string => {
    const entries = Object.entries(eventTypes)
      .sort((a, b) => b[1] - a[1]); // Sort by count descending
    
    if (entries.length === 0) return '';
    
    // Show up to 3 most frequent event types
    const topEntries = entries.slice(0, 3);
    
    return topEntries
      .map(([type, count]) => {
        const emoji = getEmojiForEventType(type);
        return count > 1 ? `${emoji}×${count}` : emoji;
      })
      .join('');
  };
  
  return {
    getEmojiForEventType,
    formatEventTypeLabel
  };
}