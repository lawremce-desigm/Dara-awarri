import 'dart:convert';
import 'dart:io';
import 'dart:async';
import 'package:http/http.dart' as http;
import '../models/intent.dart';

class VoiceResponse {
  final String transcript;
  final String language;
  final Intent intent;
  final String responseAudioBase64;

  VoiceResponse({
    required this.transcript,
    required this.language,
    required this.intent,
    required this.responseAudioBase64,
  });

  factory VoiceResponse.fromJson(Map<String, dynamic> json) {
    return VoiceResponse(
      transcript: json['transcript'] ?? '',
      language: json['language'] ?? 'en',
      intent: Intent.fromJson(json['intent']),
      responseAudioBase64: json['response_audio'] ?? '',
    );
  }
}

class DaraApiService {
  final String baseUrl;

  DaraApiService({this.baseUrl = 'http://10.0.2.2:8000'});

  Future<VoiceResponse> sendVoiceCommand(File audioFile) async {
    try {
      print('📡 Sending request to: $baseUrl/voice');
      print('📁 Audio file: ${audioFile.path}');
      print('📊 File size: ${await audioFile.length()} bytes');
      
      final uri = Uri.parse('$baseUrl/voice');
      final request = http.MultipartRequest('POST', uri);

      // Add audio file
      request.files.add(
        await http.MultipartFile.fromPath(
          'audio',
          audioFile.path,
        ),
      );

      print('⏳ Sending request...');
      // Send request with timeout
      final streamedResponse = await request.send().timeout(
        const Duration(seconds: 180),
        onTimeout: () {
          throw Exception('Request timeout - backend may be unreachable');
        },
      );
      
      final response = await http.Response.fromStream(streamedResponse);
      print('✅ Response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        return VoiceResponse.fromJson(jsonData);
      } else {
        print('❌ Error response: ${response.body}');
        throw Exception(
          'Backend error: ${response.statusCode} - ${response.body}',
        );
      }
    } on SocketException catch (e) {
      print('🔌 Socket error: $e');
      throw Exception('Network error: Cannot reach backend at $baseUrl. Is it running?');
    } on TimeoutException catch (e) {
      print('⏱️ Timeout: $e');
      throw Exception('Request timeout: Backend took too long to respond');
    } catch (e) {
      print('💥 Unexpected error: $e');
      throw Exception('Failed to send voice command: $e');
    }
  }
}
