import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'providers/app_state.dart';
import 'screens/home_screen.dart';
import 'theme/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load settings
  final prefs = await SharedPreferences.getInstance();
  final backendUrl = prefs.getString('backend_url') ?? 'http://10.0.2.2:8000';
  final esp32Ip = prefs.getString('esp32_ip') ?? '';

  runApp(MyApp(
    backendUrl: backendUrl,
    esp32Ip: esp32Ip,
  ));
}

// Root of the application

class MyApp extends StatelessWidget {
  final String backendUrl;
  final String esp32Ip;

  const MyApp({
    super.key,
    required this.backendUrl,
    required this.esp32Ip,
  });

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AppState(
        backendUrl: backendUrl,
        esp32Ip: esp32Ip.isNotEmpty ? esp32Ip : null,
      ),
      child: Consumer<AppState>(
        builder: (context, appState, child) {
          return MaterialApp(
            title: 'Dára Home',
            debugShowCheckedModeBanner: false,
            theme: AppTheme.lightTheme(),
            darkTheme: AppTheme.darkTheme(),
            themeMode: appState.themeMode,
            home: const HomeScreen(),
          );
        },
      ),
    );
  }
}
