import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Koshur Kalaam', style: TextStyle(fontFamily: 'Playfair Display', fontSize: 24)),
        backgroundColor: const Color(0xFF2F4F4F),
        actions: [
          IconButton(
            icon: const Icon(Icons.person),
            onPressed: () {
              // Profile action
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Kalaam of the Day Banner
          Container(
            margin: const EdgeInsets.all(10.0),
            padding: const EdgeInsets.all(15.0),
            decoration: BoxDecoration(
              color: const Color(0xFF2F4F4F),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Text(
              'Kalaam of the Day',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),

          // Recently Interacted Row
          SizedBox(
            height: 100.0,
            child: ListView(
              scrollDirection: Axis.horizontal,
              children: List.generate(5, (index) {
                return Container(
                  width: 80.0,
                  margin: const EdgeInsets.symmetric(horizontal: 10.0),
                  decoration: BoxDecoration(
                    color: const Color(0xFFD4AF37),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Center(
                    child: Text(
                      'Feature ${index + 1}',
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: Color(0xFF2F4F4F),
                        fontSize: 14,
                      ),
                    ),
                  ),
                );
              }),
            ),
          ),

          // Divider for sections
          Divider(
            thickness: 1,
            color: Colors.grey[300],
            height: 30,
          ),

          // Feature Grid
          Expanded(
            child: GridView.count(
              padding: const EdgeInsets.all(10),
              crossAxisCount: 3,
              crossAxisSpacing: 10,
              mainAxisSpacing: 10,
              children: [
                _buildFeatureTile(Icons.history, 'Last Read'),
                _buildFeatureTile(Icons.book, 'Poems'),
                _buildFeatureTile(Icons.person, 'Poets'),
                _buildFeatureTile(Icons.menu_book, 'Books'),
                _buildFeatureTile(Icons.music_note, 'Songs'),
                _buildFeatureTile(Icons.translate, 'Dictionary'),
                _buildFeatureTile(Icons.language, 'Language'),
              ],
            ),
          ),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: const Color(0xFF2F4F4F),
        selectedItemColor: const Color(0xFFD4AF37),
        unselectedItemColor: Colors.white,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  // Helper Widget for Feature Tiles
  Widget _buildFeatureTile(IconData icon, String label) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon, color: const Color(0xFF2F4F4F), size: 30),
        const SizedBox(height: 5),
        Text(label, style: const TextStyle(color: Color(0xFF2F4F4F))),
      ],
    );
  }
}