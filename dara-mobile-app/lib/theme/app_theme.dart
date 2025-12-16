import 'package:flutter/material.dart';

class AppTheme {
  // Color palette - Deep Indigo & Emerald
  static const _primaryColor = Color(0xFF1A237E); // Deep Indigo
  static const _accentColor = Color(0xFF00897B); // Soft Emerald
  static const _surfaceDark = Color(0xFF121212);
  static const _surfaceLight = Color(0xFFFAFAFA);

  static ThemeData darkTheme() {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: const Color(0xFF121212),
      colorScheme: ColorScheme.fromSeed(
        seedColor: _primaryColor,
        brightness: Brightness.dark,
        primary: _primaryColor,
        secondary: _accentColor,
        surface: const Color(0xFF1E1E1E),
        onSurface: Colors.white,
      ),
      cardTheme: const CardThemeData(
        elevation: 0,
        color: Color(0xFF1E1E1E),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(20)),
          side: BorderSide(color: Color(0xFF2C2C2C), width: 1),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: _primaryColor,
          foregroundColor: Colors.white,
          elevation: 0,
          shape: const CircleBorder(),
          padding: const EdgeInsets.all(32),
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
    );
  }

  static ThemeData lightTheme() {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: Colors.white, // Pure white for sleek look
      colorScheme: ColorScheme.fromSeed(
        seedColor: _primaryColor,
        brightness: Brightness.light,
        primary: _primaryColor,
        secondary: _accentColor,
        surface: const Color(0xFFF5F5F7), // Subtle contrast for cards
        onSurface: const Color(0xFF1D1D1F), // Soft black
        surfaceContainerHighest: Colors.white,
      ),
      cardTheme: const CardThemeData(
        elevation: 0, // Flat design
        color: Color(0xFFF5F5F7), // Light grey cards
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(20)),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: _primaryColor,
          foregroundColor: Colors.white,
          elevation: 0,
          shape: const CircleBorder(),
          padding: const EdgeInsets.all(32),
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        scrolledUnderElevation: 0,
      ),
    );
  }
}
