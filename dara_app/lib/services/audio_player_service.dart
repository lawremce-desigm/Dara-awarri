import 'dart:convert';
import 'dart:typed_data';
import 'package:just_audio/just_audio.dart';

class AudioPlayerService {
  final AudioPlayer _player = AudioPlayer();

  Future<void> playBase64Audio(String base64Audio) async {
    try {
      if (base64Audio.isEmpty) {
        print('⚠️ Audio warning: Received empty audio data');
        return;
      }

      // Decode base64 to bytes
      final bytes = base64Decode(base64Audio);

      if (bytes.isEmpty) {
        print('⚠️ Audio warning: Decoded audio bytes are empty');
        return;
      }
      
      // Create a stream source from bytes
      final audioSource = MyCustomSource(bytes);
      
      // Load and play
      await _player.setAudioSource(audioSource);
      await _player.play();
    } catch (e) {
      print('❌ Audio error: Failed to play audio: $e');
      // Don't throw, just log to prevent app crash
    }
  }

  Future<void> stop() async {
    await _player.stop();
  }

  void dispose() {
    _player.dispose();
  }

  bool get isPlaying => _player.playing;
}

// Custom audio source for loading from bytes
class MyCustomSource extends StreamAudioSource {
  final Uint8List _buffer;

  MyCustomSource(this._buffer);

  @override
  Future<StreamAudioResponse> request([int? start, int? end]) async {
    start ??= 0;
    end ??= _buffer.length;

    return StreamAudioResponse(
      sourceLength: _buffer.length,
      contentLength: end - start,
      offset: start,
      stream: Stream.value(_buffer.sublist(start, end)),
      contentType: 'audio/mpeg',
    );
  }
}
