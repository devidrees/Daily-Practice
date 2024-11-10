import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'homepage2.dart';

void main() {
  runApp(KoshurKalaamApp());
}

class KoshurKalaamApp extends StatelessWidget {
  const KoshurKalaamApp({super.key});  // Adding the key here

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Koshur Kalaam',
      theme: ThemeData(
        // Define the overall color scheme
        colorScheme: ColorScheme.light(
          primary: Color(0xFF2F4F4F),  // Dark Green Primary Color
          secondary: Color(0xFFD4AF37),  // Gold Secondary Color
          surface: Colors.white,  // White surface
          //background: Color(0xFFF5F5DC),  // Light Beige background
          error: Colors.red,  // Red error color
          onPrimary: Colors.white,  // Text/icon color when on Primary
          onSecondary: Colors.black,  // Text/icon color when on Secondary
          onSurface: Colors.black,  // Text/icon color when on Surface
          onError: Colors.white,  // Text/icon color when on Error
        ),
        textTheme: TextTheme(
          bodySmall: GoogleFonts.lato(color: Color(0xFF333333)),
          bodyLarge: GoogleFonts.lato(color: Color(0xFF333333)),
          displayLarge: GoogleFonts.playfairDisplay(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Color(0xFF2F4F4F),
          ),
          headlineMedium: GoogleFonts.playfairDisplay(
            fontSize: 18,
            color: Color(0xFF2F4F4F),
          ),
        ),
      ),
      home: Homepage2(),
    );
  }
}
