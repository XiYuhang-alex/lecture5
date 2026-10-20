import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Counter Deep',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Counter Deep Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;
  int _step = 1;

  @override
  void initState() {
    super.initState();
    print('[Lifecycle] initState: 一次性初始化');
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    print('[Lifecycle] didChangeDependencies: 依赖(如主题)变化');
  }

  @override
  void didUpdateWidget(covariant MyHomePage oldWidget) {
    super.didUpdateWidget(oldWidget);
    print('[Lifecycle] didUpdateWidget: 父重建传入新配置');
  }

  @override
  void dispose() {
    print('[Lifecycle] dispose: 销毁清理');
    super.dispose();
  }

  void _incrementCounter() {
    setState(() {
      _counter += _step;
    });
  }

  Future<void> _chooseStep() async {
    final int? picked = await showDialog<int>(
      context: context,
      builder: (BuildContext context) {
        return SimpleDialog(
          title: const Text('选择步长'),
          children: [1, 2, 5].map((int value) {
            return SimpleDialogOption(
              onPressed: () => Navigator.pop(context, value),
              child: Text('每次 +$value'),
            );
          }).toList(),
        );
      },
    );
    if (picked != null) {
      setState(() {
        _step = picked;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    print('[Lifecycle] build: counter=$_counter, step=$_step');
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
        actions: [
          IconButton(
            onPressed: _chooseStep,
            icon: const Icon(Icons.tune),
            tooltip: '选择步长',
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: .center,
          children: [
            if (_counter == 0)
              Image.asset(
                'assets/images/empty_counter.png',
                width: 260,
              ),
            const Text('You have pushed the button this many times:'),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 12),
            Text(
              '当前步长：+$_step',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: Theme.of(context).colorScheme.primary,
                  ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
