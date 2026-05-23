import 'package:flutter/material.dart';
import '../screens/splash_screen.dart';
import '../screens/home_screen.dart';
import '../screens/settings_screen.dart';
import '../screens/category_screen.dart';
import '../screens/reminder_form_screen.dart';
import '../screens/history_screen.dart';

class AppRoutes {
  static const String splash = '/';
  static const String home = '/home';
  static const String settings = '/settings';
  static const String categories = '/categories';
  static const String reminderForm = '/reminder_form';
  static const String history = '/history';

  static Map<String, WidgetBuilder> get routes => {
    splash: (ctx) => const SplashScreen(),
    home: (ctx) => const HomeScreen(),
    settings: (ctx) => const SettingsScreen(),
    categories: (ctx) => const CategoryScreen(),
    reminderForm: (ctx) => const ReminderFormScreen(),
    history: (ctx) => const HistoryScreen(),
  };
}
