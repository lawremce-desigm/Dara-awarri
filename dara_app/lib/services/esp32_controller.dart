import 'package:http/http.dart' as http;
import '../models/intent.dart';

class ESP32Controller {
  final String esp32Ip;

  ESP32Controller({required this.esp32Ip});

  Future<String?> executeCommand(Intent intent) async {
    if (intent.action.toLowerCase() == 'check' && intent.device.toLowerCase() == 'temperature') {
      return await getTemperature();
    }

    if (!intent.hasDeviceAction) return null;

    final device = intent.device.toLowerCase();
    final action = intent.action.toLowerCase().replaceAll('_', '/');

    final url = 'http://$esp32Ip/$device/$action';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 5));

      if (response.statusCode != 200) {
        throw Exception('ESP32 returned ${response.statusCode}');
      }
      return null;
    } catch (e) {
      throw Exception('Failed to control device: $e');
    }
  }

  Future<String> getTemperature() async {
    final url = 'http://$esp32Ip/temperature';
    try {
      final response = await http.get(
        Uri.parse(url),
      ).timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        return response.body; 
      } else {
        throw Exception('Failed to get temperature: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to connect to sensor: $e');
    }
  }
}
