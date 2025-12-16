class ConversationMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final String? deviceAction; // e.g., "Turned on light"

  ConversationMessage({
    required this.text,
    required this.isUser,
    DateTime? timestamp,
    this.deviceAction,
  }) : timestamp = timestamp ?? DateTime.now();
}
