import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/app_state.dart';

class VoiceMicButton extends StatefulWidget {
  const VoiceMicButton({super.key});

  @override
  State<VoiceMicButton> createState() => _VoiceMicButtonState();
}

class _VoiceMicButtonState extends State<VoiceMicButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    );

    _scaleAnimation = Tween<double>(begin: 1.0, end: 1.15).animate(
      CurvedAnimation(
        parent: _pulseController,
        curve: Curves.easeInOut,
      ),
    );
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);
    final status = appState.status;
    final theme = Theme.of(context);

    // Control pulse animation
    if (status == AppStatus.recording) {
      if (!_pulseController.isAnimating) {
        _pulseController.repeat(reverse: true);
      }
    } else {
      _pulseController.stop();
      _pulseController.reset();
    }

    final isProcessing = status == AppStatus.processing;
    final isDisabled = status == AppStatus.processing || status == AppStatus.speaking;

    return GestureDetector(
      onTap: isDisabled ? null : appState.toggleRecording,
      child: AnimatedBuilder(
        animation: _pulseController,
        builder: (context, child) {
          return Container(
            width: 140,
            height: 140,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              boxShadow: status == AppStatus.recording
                  ? [
                      BoxShadow(
                        color: theme.colorScheme.primary.withOpacity(
                          0.4 * _scaleAnimation.value,
                        ),
                        blurRadius: 30,
                        spreadRadius: 10,
                      ),
                    ]
                  : null,
            ),
            child: Transform.scale(
              scale: status == AppStatus.recording ? _scaleAnimation.value : 1.0,
              child: FilledButton(
                style: FilledButton.styleFrom(
                  backgroundColor: _getButtonColor(status, theme),
                  shape: const CircleBorder(),
                  padding: const EdgeInsets.all(36),
                ),
                onPressed: isDisabled ? null : appState.toggleRecording,
                child: isProcessing
                    ? CircularProgressIndicator(
                        color: theme.colorScheme.onPrimary,
                        strokeWidth: 3,
                      )
                    : Icon(
                        _getIcon(status),
                        size: 56,
                        color: theme.colorScheme.onPrimary,
                      ),
              ),
            ),
          );
        },
      ),
    );
  }

  Color _getButtonColor(AppStatus status, ThemeData theme) {
    switch (status) {
      case AppStatus.recording:
        return Colors.red;
      case AppStatus.error:
        return Colors.red.shade700;
      case AppStatus.speaking:
        return theme.colorScheme.secondary;
      default:
        return theme.colorScheme.primary;
    }
  }

  IconData _getIcon(AppStatus status) {
    switch (status) {
      case AppStatus.recording:
        return Icons.stop;
      case AppStatus.speaking:
        return Icons.volume_up;
      default:
        return Icons.mic;
    }
  }
}
