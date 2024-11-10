import 'package:flutter/material.dart';

void main() => runApp(KosherKalamApp());

class KosherKalamApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Koshur Kalam',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: Homepage2(),
    );
  }
}

class Homepage2 extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Koshur Kalam'),
        backgroundColor: Colors.green[800],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Popular Section
              _buildPopularSection(),

              SizedBox(height: 20),

              // Last Read Section
              _buildLastReadSection(),

              SizedBox(height: 20),

              // Other categories
              _buildCategorySection('Poems'),
              _buildCategorySection('Poets'),
              _buildCategorySection('Decets'),
              _buildCategorySection('Dongs'),
              _buildCategorySection('Soaps'),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPopularSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'POPULAR',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        SizedBox(height: 10),
        Container(
          height: 200,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10),
            image: DecorationImage(
              image: AssetImage('assets/popular_image.jpg'), // Replace with your image asset
              fit: BoxFit.cover,
            ),
          ),
          child: Align(
            alignment: Alignment.bottomLeft,
            child: Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(
                'Popular Article Title',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                  shadows: [
                    Shadow(
                      blurRadius: 10.0,
                      color: Colors.black,
                      offset: Offset(0, 2),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildLastReadSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'LAST READ',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        SizedBox(height: 10),
        _buildLastReadItem('Kashmiri', 'assets/kashmiri_image.jpg'),
        _buildLastReadItem('Poetry', 'assets/poetry_image.jpg'),
        _buildLastReadItem('Dictionary', 'assets/dictionary_image.jpg'),
        _buildLastReadItem('Designer', 'assets/designer_image.jpg'),
      ],
    );
  }

  Widget _buildLastReadItem(String title, String imagePath) {
    return GestureDetector(
      onTap: () {
        // Navigate to the relevant page
      },
      child: Container(
        margin: EdgeInsets.only(bottom: 10),
        child: Row(
          children: [
            Image.asset(
              imagePath,
              width: 50,
              height: 50,
              fit: BoxFit.cover,
            ),
            SizedBox(width: 10),
            Text(
              title,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCategorySection(String category) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          category.toUpperCase(),
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        SizedBox(height: 10),
        Container(
          height: 120,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10),
            color: Colors.grey[800],
          ),
          child: Center(
            child: Text(
              category,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          ),
        ),
        SizedBox(height: 10),
      ],
    );
  }
}
