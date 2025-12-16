class Intent {
  final String type; // "CONVERSATION" or "INSTRUCTION"
  final String language;
  final String action; // "TURN_ON", "TURN_OFF", or "NONE"
  final String device; // "LIGHT", "FAN", or "NONE"
  final String responseText;

  Intent({
    required this.type,
    required this.language,
    required this.action,
    required this.device,
    required this.responseText,
  });

  factory Intent.fromJson(Map<String, dynamic> json) {
    return Intent(
      type: json['type'] ?? 'CONVERSATION',
      language: json['language'] ?? 'en',
      action: json['action'] ?? 'NONE',
      device: json['device'] ?? 'NONE',
      responseText: json['response_text'] ?? '',
    );
  }

  bool get isInstruction => type == 'INSTRUCTION';
  bool get hasDeviceAction => action != 'NONE' && device != 'NONE';
}
