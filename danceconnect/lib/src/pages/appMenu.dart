import 'package:flutter/material.dart';

import '../settings/settings_view.dart';
import '../sample_feature/sample_item.dart';
import '../sample_feature/sample_item_details_view.dart';
import 'calendar.dart';
import 'events.dart';
import 'home.dart';
import 'people.dart';
// import '../sample sample_item.dart';
// import 'sample_item_details_view.dart';

/// Displays a list of SampleItems.
class AppMenu extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        ElevatedButton(
            onPressed: () {
              Navigator.restorablePushNamed(context, HomePage.routeName);
            },
            child: Text("Home")),
        ElevatedButton(
            onPressed: () {
              Navigator.restorablePushNamed(context, CalendarPage.routeName);
            },
            child: Text("Calendar")),
        ElevatedButton(
            onPressed: () {
              Navigator.restorablePushNamed(context, EventsPage.routeName);
            },
            child: Text("Events")),
        ElevatedButton(
            onPressed: () {
              Navigator.restorablePushNamed(context, PeoplePage.routeName);
            },
            child: Text("People"))
      ],
    );

    // Scaffold(
    //   appBar: AppBar(
    //     title: const Text('Sample Items'),
    //     actions: [
    //       IconButton(
    //         icon: const Icon(Icons.settings),
    //         onPressed: () {
    //           // Navigate to the settings page. If the user leaves and returns
    //           // to the app after it has been killed while running in the
    //           // background, the navigation stack is restored.
    //           Navigator.restorablePushNamed(context, SettingsView.routeName);
    //         },
    //       ),
    //     ],
    //   ),

    //   // To work with lists that may contain a large number of items, it’s best
    //   // to use the ListView.builder constructor.
    //   //
    //   // In contrast to the default ListView constructor, which requires
    //   // building all Widgets up front, the ListView.builder constructor lazily
    //   // builds Widgets as they’re scrolled into view.
    //   body: Column(
    //     children: [
    //       ListView.builder(
    //         // Providing a restorationId allows the ListView to restore the
    //         // scroll position when a user leaves and returns to the app after it
    //         // has been killed while running in the background.
    //         restorationId: 'sampleItemListView',
    //         itemCount: items.length,
    //         itemBuilder: (BuildContext context, int index) {
    //           final item = items[index];

    //           return ListTile(
    //               title: Text('SampleItem ${item.id}'),
    //               leading: const CircleAvatar(
    //                 // Display the Flutter Logo image asset.
    //                 foregroundImage:
    //                     AssetImage('assets/images/flutter_logo.png'),
    //               ),
    //               onTap: () {
    //                 // Navigate to the details page. If the user leaves and returns to
    //                 // the app after it has been killed while running in the
    //                 // background, the navigation stack is restored.
    //                 Navigator.restorablePushNamed(
    //                   context,
    //                   SampleItemDetailsView.routeName,
    //                 );
    //               });
    //         },
    //       ),
    //       const Text("Home Tab"),
    //     ],
    //   ),
    // );
  }
}
