import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/app_state.dart';
import '../widgets/mic_button.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Column(
          children: [
            Text(
              'Dára Home',
              style: theme.textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.w600,
              ),
            ),
            Text(
              'Your voice-powered home',
              style: theme.textTheme.bodySmall?.copyWith(
                color: theme.colorScheme.onSurface.withOpacity(0.6),
              ),
            ),
          ],
        ),
        centerTitle: true,
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(
              appState.themeMode == ThemeMode.light
                  ? Icons.dark_mode_outlined
                  : Icons.light_mode_outlined,
              color: theme.colorScheme.onSurface,
            ),
            onPressed: appState.toggleTheme,
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(height: 24),
            
            // Language Selector
            _buildLanguageSelector(context, appState, theme),
            
            const Spacer(),
            
            // Mic Button (Hero Element)
            const VoiceMicButton(),
            
            const SizedBox(height: 24),
            
            // Status Text
            _buildStatusText(context, appState, theme),
            
            const SizedBox(height: 32),
            
            // Response Card
            if (appState.lastAssistantResponse.isNotEmpty)
              _buildResponseCard(context, appState, theme),
            
            const Spacer(),
          ],
        ),
      ),
    );
  }

  Widget _buildLanguageSelector(
    BuildContext context,
    AppState appState,
    ThemeData theme,
  ) {
    const languages = {
      'en': '🇬🇧 English',
      'yo': '🇳🇬 Yoruba',
      'ha': '🇳🇬 Hausa',
      'ig': '🇳🇬 Igbo',
    };

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0),
      child: Column(
        children: [
          DropdownMenu<String>(
            width: MediaQuery.of(context).size.width - 48,
            initialSelection: appState.selectedLanguage,
            label: const Text('Language'),
            dropdownMenuEntries: languages.entries.map((entry) {
              return DropdownMenuEntry<String>(
                value: entry.key,
                label: entry.value,
              );
            }).toList(),
            onSelected: (String? value) {
              if (value != null) {
                appState.setLanguage(value);
              }
            },
          ),
          const SizedBox(height: 8),
          Text(
            'Select language before speaking',
            style: theme.textTheme.bodySmall?.copyWith(
              color: theme.colorScheme.onSurface.withOpacity(0.5),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusText(
    BuildContext context,
    AppState appState,
    ThemeData theme,
  ) {
    String statusText;
    switch (appState.status) {
      case AppStatus.recording:
        statusText = 'Listening…';
        break;
      case AppStatus.processing:
        statusText = 'Processing…';
        break;
      case AppStatus.speaking:
        statusText = 'Speaking…';
        break;
      case AppStatus.error:
        statusText = appState.errorMessage;
        break;
      default:
        statusText = 'Tap to speak';
    }

    return AnimatedOpacity(
      opacity: appState.status != AppStatus.idle ? 1.0 : 0.6,
      duration: const Duration(milliseconds: 300),
      child: Text(
        statusText,
        style: theme.textTheme.bodyLarge?.copyWith(
          color: appState.status == AppStatus.error
              ? theme.colorScheme.error
              : theme.colorScheme.onSurface,
        ),
        textAlign: TextAlign.center,
      ),
    );
  }

  Widget _buildResponseCard(
    BuildContext context,
    AppState appState,
    ThemeData theme,
  ) {
    return AnimatedOpacity(
      opacity: 1.0,
      duration: const Duration(milliseconds: 500),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24.0),
        child: Card(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (appState.lastUserInput.isNotEmpty) ...[
                  Row(
                    children: [
                      Icon(
                        Icons.person,
                        size: 16,
                        color: theme.colorScheme.primary,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'You',
                        style: theme.textTheme.labelSmall?.copyWith(
                          color: theme.colorScheme.primary,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    appState.lastUserInput,
                    style: theme.textTheme.bodyMedium?.copyWith(
                      color: theme.colorScheme.onSurface.withOpacity(0.7),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Divider(color: theme.colorScheme.outlineVariant),
                  const SizedBox(height: 16),
                ],
                Row(
                  children: [
                    Icon(
                      Icons.assistant,
                      size: 16,
                      color: theme.colorScheme.secondary,
                    ),
                    const SizedBox(width: 8),
                    Text(
                      'Dára',
                      style: theme.textTheme.labelSmall?.copyWith(
                        color: theme.colorScheme.secondary,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  appState.lastAssistantResponse,
                  style: theme.textTheme.bodyMedium,
                ),
                if (appState.lastDeviceAction != null) ...[
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: theme.colorScheme.secondaryContainer,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.lightbulb_outline,
                          size: 16,
                          color: theme.colorScheme.onSecondaryContainer,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          appState.lastDeviceAction!,
                          style: theme.textTheme.bodySmall?.copyWith(
                            color: theme.colorScheme.onSecondaryContainer,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
