import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final _backendUrlController = TextEditingController();
  final _esp32IpController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _backendUrlController.text =
          prefs.getString('backend_url') ?? 'http://127.0.0.1:8000';
      _esp32IpController.text =
          prefs.getString('esp32_ip') ?? '192.168.1.100';
    });
  }

  Future<void> _saveSettings() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('backend_url', _backendUrlController.text);
    await prefs.setString('esp32_ip', _esp32IpController.text);

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Settings saved!')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[900],
      appBar: AppBar(
        title: const Text('Settings'),
        backgroundColor: Colors.green[700],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildTextField(
            controller: _backendUrlController,
            label: 'Backend API URL',
            hint: 'http://127.0.0.1:8000',
          ),
          const SizedBox(height: 24),
          _buildTextField(
            controller: _esp32IpController,
            label: 'ESP32 IP Address',
            hint: '192.168.1.100',
          ),
          const SizedBox(height: 32),
          ElevatedButton(
            onPressed: _saveSettings,
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green[700],
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
            child: const Text(
              'Save Settings',
              style: TextStyle(fontSize: 16),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required String hint,
  }) {
    return TextField(
      controller: controller,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        labelStyle: TextStyle(color: Colors.grey[400]),
        hintStyle: TextStyle(color: Colors.grey[600]),
        enabledBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Colors.grey[700]!),
        ),
        focusedBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Colors.green[700]!),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _backendUrlController.dispose();
    _esp32IpController.dispose();
    super.dispose();
  }
}
