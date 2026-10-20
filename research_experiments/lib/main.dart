import 'package:flutter/material.dart';

void main() {
  runApp(const ResearchApp());
}

class ResearchApp extends StatelessWidget {
  const ResearchApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Research Experiments',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const ExperimentHome(),
    );
  }
}

class ExperimentHome extends StatelessWidget {
  const ExperimentHome({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('独立研究实验')),
      body: ListView(
        children: [
          ListTile(
            title: const Text('实验1：const构造与rebuild优化'),
            onTap: () => Navigator.push(context,
                MaterialPageRoute(builder: (_) => const ConstRebuildPage())),
          ),
          ListTile(
            title: const Text('实验2：InheritedWidget初探'),
            onTap: () => Navigator.push(context,
                MaterialPageRoute(builder: (_) => const InheritedPage())),
          ),
          ListTile(
            title: const Text('实验3：Keys作用实验'),
            onTap: () => Navigator.push(context,
                MaterialPageRoute(builder: (_) => const KeysPage())),
          ),
        ],
      ),
    );
  }
}

// ========== 实验1：const构造与rebuild优化 ==========
int nonConstBuildCount = 0;
int constBuildCount = 0;

class NonConstItem extends StatelessWidget {
  const NonConstItem({super.key, required this.label});
  final String label;

  @override
  Widget build(BuildContext context) {
    nonConstBuildCount++;
    print('[Exp1] NonConstItem build #$nonConstBuildCount ($label)');
    return Text(label);
  }
}

class ConstItem extends StatelessWidget {
  const ConstItem({super.key, required this.label});
  final String label;

  @override
  Widget build(BuildContext context) {
    constBuildCount++;
    print('[Exp1] ConstItem build #$constBuildCount ($label)');
    return Text(label);
  }
}

class ConstRebuildPage extends StatefulWidget {
  const ConstRebuildPage({super.key});

  @override
  State<ConstRebuildPage> createState() => _ConstRebuildPageState();
}

class _ConstRebuildPageState extends State<ConstRebuildPage> {
  int _tick = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('实验1：const与rebuild')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('父级重建次数：$_tick'),
            const SizedBox(height: 16),
            // 非const：每次父重建都会跟着重建
            NonConstItem(label: '非const列表项'),
            // const：父重建时被框架复用，不再重建
            const ConstItem(label: 'const列表项'),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => setState(() => _tick++),
        child: const Icon(Icons.refresh),
      ),
    );
  }
}

// ========== 实验2：InheritedWidget初探 ==========
class CounterScope extends InheritedWidget {
  const CounterScope({
    super.key,
    required this.count,
    required super.child,
  });

  final int count;

  static CounterScope of(BuildContext context) {
    final CounterScope? scope =
        context.dependOnInheritedWidgetOfExactType<CounterScope>();
    assert(scope != null, 'CounterScope not found in context');
    return scope!;
  }

  @override
  bool updateShouldNotify(CounterScope oldWidget) => count != oldWidget.count;
}

class DeepLeaf extends StatelessWidget {
  const DeepLeaf({super.key});

  @override
  Widget build(BuildContext context) {
    // 深层组件直接从 InheritedWidget 取值，无需层层传参
    final count = CounterScope.of(context).count;
    print('[Exp2] DeepLeaf build, count=$count');
    return Text('深层叶子读到 count = $count');
  }
}

class InheritedPage extends StatefulWidget {
  const InheritedPage({super.key});

  @override
  State<InheritedPage> createState() => _InheritedPageState();
}

class _InheritedPageState extends State<InheritedPage> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return CounterScope(
      count: _count,
      child: Scaffold(
        appBar: AppBar(title: const Text('实验2：InheritedWidget')),
        body: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('中间层（不传参）'),
              DeepLeaf(),
            ],
          ),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () => setState(() => _count++),
          child: const Icon(Icons.add),
        ),
      ),
    );
  }
}

// ========== 实验3：Keys作用实验 ==========
class KeysPage extends StatefulWidget {
  const KeysPage({super.key});

  @override
  State<KeysPage> createState() => _KeysPageState();
}

class _KeysPageState extends State<KeysPage> {
  bool _useKey = false;
  List<int> _items = [1, 2, 3];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('实验3：Keys作用')),
      body: Column(
        children: [
          SwitchListTile(
            title: Text(_useKey ? '当前：列表项带 ValueKey' : '当前：列表项不带 Key'),
            value: _useKey,
            onChanged: (v) => setState(() => _useKey = v),
          ),
          Expanded(
            child: ListView(
              children: _items.map((n) {
                final tile = _ColoredTile(
                  key: _useKey ? ValueKey(n) : null,
                  label: '条目 $n',
                );
                return tile;
              }).toList(),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => setState(() => _items = _items.reversed.toList()),
        child: const Icon(Icons.swap_vert),
      ),
    );
  }
}

class _ColoredTile extends StatefulWidget {
  const _ColoredTile({super.key, required this.label});
  final String label;

  @override
  State<_ColoredTile> createState() => _ColoredTileState();
}

class _ColoredTileState extends State<_ColoredTile> {
  // 每个 State 随机生成一个颜色，用来观察状态是否跟着 Widget 走
  final Color _color =
      Colors.primaries[(DateTime.now().microsecond) % Colors.primaries.length];

  @override
  Widget build(BuildContext context) {
    print('[Exp3] _ColoredTile build: ${widget.label}, color=${_color.toARGB32()}');
    return Container(
      margin: const EdgeInsets.all(8),
      padding: const EdgeInsets.all(16),
      color: _color,
      child: Text(widget.label),
    );
  }
}
