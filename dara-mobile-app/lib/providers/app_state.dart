import 'dart:io';
import 'package:flutter/material.dart';
import '../models/intent.dart';
import '../services/dara_api_service.dart';
import '../services/voice_recorder.dart';
import '../services/audio_player_service.dart';
import '../services/esp32_controller.dart';

enum AppStatus {
  idle,
  recording,
  processing,
  speaking,
  error,
}

class AppState with ChangeNotifier {
  final DaraApiService _apiService;
  final VoiceRecorderService _voiceRecorder = VoiceRecorderService();
  final AudioPlayerService _audioPlayer = AudioPlayerService();
  ESP32Controller? _esp32Controller;

  AppStatus _status = AppStatus.idle;
  String _errorMessage = '';
  String _lastUserInput = '';
  String _lastAssistantResponse = '';
  String? _lastDeviceAction;
  String _selectedLanguage = 'en'; // Default language
  ThemeMode _themeMode = ThemeMode.light; // Default to Light Mode (Sleek White)

  AppStatus get status => _status;
  String get errorMessage => _errorMessage;
  bool get isRecording => _voiceRecorder.isRecording;
  String get lastUserInput => _lastUserInput;
  String get lastAssistantResponse => _lastAssistantResponse;
  String? get lastDeviceAction => _lastDeviceAction;
  String get selectedLanguage => _selectedLanguage;
  ThemeMode get themeMode => _themeMode;

  AppState({
    required String backendUrl,
    String? esp32Ip,
  }) : _apiService = DaraApiService(baseUrl: backendUrl) {
    if (esp32Ip != null && esp32Ip.isNotEmpty) {
      _esp32Controller = ESP32Controller(esp32Ip: esp32Ip);
    }
  }

  void toggleTheme() {
    _themeMode = _themeMode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    notifyListeners();
  }

  void setLanguage(String languageCode) {
    _selectedLanguage = languageCode;
    notifyListeners();
  }

  void updateESP32Ip(String ip) {
    _esp32Controller = ESP32Controller(esp32Ip: ip);
    notifyListeners();
  }

  Future<void> toggleRecording() async {
    if (_status == AppStatus.recording) {
      await _stopRecordingAndProcess();
    } else if (_status == AppStatus.idle) {
      await _startRecording();
    }
  }

  Future<void> _startRecording() async {
    try {
      await _voiceRecorder.startRecording();
      _status = AppStatus.recording;
      _errorMessage = '';
      notifyListeners();
    } catch (e) {
      _status = AppStatus.error;
      _errorMessage = 'Failed to start recording: $e';
      notifyListeners();
    }
  }

  Future<void> _stopRecordingAndProcess() async {
    try {
      final audioFile = await _voiceRecorder.stopRecording();
      if (audioFile == null) {
        throw Exception('No audio recorded');
      }

      _status = AppStatus.processing;
      notifyListeners();

      final response = await _apiService.sendVoiceCommand(audioFile);

      _lastUserInput = response.transcript;

      // Execute ESP32 command if needed
      String? deviceAction;
      if (response.intent.hasDeviceAction && _esp32Controller != null) {
        try {
          final result = await _esp32Controller!.executeCommand(response.intent);
          
          if (result != null) {
            // It was a sensor check (Temperature)
            deviceAction = result;
          } else {
            // Standard action
            deviceAction =
              '${response.intent.action.replaceAll('_', ' ')} ${response.intent.device}';
          }
        } catch (e) {
          debugPrint('ESP32 error: $e');
        }
      }

      _lastAssistantResponse = response.intent.responseText;
      _lastDeviceAction = deviceAction;

      // Play audio response
      _status = AppStatus.speaking;
      notifyListeners();

      await _audioPlayer.playBase64Audio(response.responseAudioBase64);

      _status = AppStatus.idle;
      notifyListeners();
    } catch (e) {
      _status = AppStatus.error;
      _errorMessage = 'Error: $e';
      notifyListeners();
      
      // Auto-reset to idle after 3 seconds
      Future.delayed(const Duration(seconds: 3), () {
        if (_status == AppStatus.error) {
          _status = AppStatus.idle;
          notifyListeners();
        }
      });
    }
  }

  @override
  void dispose() {
    _voiceRecorder.dispose();
    _audioPlayer.dispose();
    super.dispose();
  }
}
