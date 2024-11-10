import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Get the current theme for color consistency
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Koshur Kalaam',
          style: theme.textTheme.headlineMedium, // Use theme text style for the title
        ),
        backgroundColor: theme.colorScheme.primary, // Use primary color from theme
        actions: [
          IconButton(
            icon: Icon(Icons.account_circle, color: theme.colorScheme.onPrimary), // Icon color from theme
            onPressed: () {
              // Profile screen logic
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Kalaam of the day (Scrollable Banner)
            Container(
              height: 200,
              color: theme.colorScheme.primary, // Use primary color
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Container(
                  width: 600,
                  padding: EdgeInsets.all(20),
                  child: Text(
                    "“Raat bhar ka chand hai, aur kuch nahi, \nSaath tera tha, aur kuch nahi.”\n- Unknown",
                    style: theme.textTheme.displayLarge?.copyWith(color: Colors.white), // Text style from theme
                  ),
                ),
              ),
            ),
            SizedBox(height: 20),

            // Recently Interacted Section (Scrollable Row of Boxes)
            Container(
              height: 150,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: 5,
                itemBuilder: (context, index) {
                  return Padding(
                    padding: EdgeInsets.symmetric(horizontal: 10),
                    child: Container(
                      width: 100,
                      color: theme.colorScheme.secondary, // Use secondary color from theme
                      child: Center(child: Icon(Icons.book, color: Colors.white)),
                    ),
                  );
                },
              ),
            ),
            SizedBox(height: 30),

            // Features of the app section with buttons
            GridView.count(
              shrinkWrap: true,
              crossAxisCount: 3,
              crossAxisSpacing: 10,
              mainAxisSpacing: 10,
              padding: EdgeInsets.all(10),
              children: [
                _buildFeatureBox(Icons.book, 'Last Read', theme),
                _buildFeatureBox(Icons.bookmark, 'Poems', theme),
                _buildFeatureBox(Icons.person, 'Poets', theme),
                _buildFeatureBox(Icons.library_books, 'Books', theme),
                _buildFeatureBox(Icons.music_note, 'Songs', theme),
                _buildFeatureBox(Icons.translate, 'Dictionary', theme),
                _buildFeatureBox(Icons.language, 'Language', theme),
              ],
            ),
          ],
        ),
      ),

      // Bottom Navigation Bar
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: theme.colorScheme.primary, // Bottom navigation bar color
        selectedItemColor: theme.colorScheme.onPrimary, // Selected item color
        unselectedItemColor: theme.colorScheme.onSurface, // Unselected item color
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.search),
            label: 'Search',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.account_circle),
            label: 'Profile',
          ),
        ],
      ),
    );
  }

  // Helper function to create feature buttons with theme consistency
  Widget _buildFeatureBox(IconData icon, String label, ThemeData theme) {
    return GestureDetector(
      onTap: () {
        // Handle navigation or functionality
      },
      child: Container(
        decoration: BoxDecoration(
          color: theme.colorScheme.secondary, // Use secondary color from theme
          borderRadius: BorderRadius.circular(10),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 30, color: Colors.white),
            SizedBox(height: 5),
            Text(
              label,
              style: theme.textTheme.bodyLarge?.copyWith(color: Colors.white), // Use theme text style
            ),
          ],
        ),
      ),
    );
  }
}
