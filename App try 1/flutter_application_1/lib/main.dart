import 'package:flutter/material.dart';
import 'home_page.dart';

void main() {
  runApp(const KoshurKalaamApp());
}

class KoshurKalaamApp extends StatelessWidget {
  const KoshurKalaamApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Koshur Kalaam',
      theme: ThemeData(
        primaryColor: const Color(0xFF2F4F4F),
        fontFamily: 'Playfair Display', colorScheme: ColorScheme.fromSwatch().copyWith(secondary: const Color(0xFFD4AF37)), colorScheme: const ColorScheme(surface: Color(0xFFF5F5DC)),
      ),
      home: HomePage(),
    );
  }
}