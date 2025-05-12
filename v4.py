import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import font as tkfont

# BST Implementation
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        
class BST:
    def __init__(self):
        self.root = None
        
    def insert(self, key):
        def _insert(node, key):
            if not node:
                return BSTNode(key)
            elif key < node.key:
                node.left = _insert(node.left, key)
            else:
                node.right = _insert(node.right, key)
            return node
        self.root = _insert(self.root, key)

    def search(self, key):
        def _search(node, key):
            if not node:
                return False
            if node.key == key:
                return True
            elif key < node.key:
                return _search(node.left, key)
            else:
                return _search(node.right, key)
        return _search(self.root, key)

    def clear(self):
        self.root = None

    def inorder_traversal(self, node, result):
        """Helper method to perform an in-order traversal and collect keys."""
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.key)
            self.inorder_traversal(node.right, result)

    def balance(self):
        """Balance the tree by rebuilding it from a sorted array."""
        def build_balanced_tree(keys, start, end):
            if start > end:
                return None
            mid = (start + end) // 2
            node = BSTNode(keys[mid])
            node.left = build_balanced_tree(keys, start, mid - 1)
            node.right = build_balanced_tree(keys, mid + 1, end)
            return node

        # Get all keys in sorted order
        keys = []
        self.inorder_traversal(self.root, keys)

        # Rebuild the tree
        self.root = build_balanced_tree(keys, 0, len(keys) - 1)

# Hash Table Implementation
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return key % self.size

    def insert(self, key):
        h = self._hash(key)
        if key not in self.table[h]:
            self.table[h].append(key)

    def search(self, key):
        h = self._hash(key)
        return key in self.table[h]

    def clear(self):
        self.table = [[] for _ in range(self.size)]

# Create a tooltip class
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        # Create a toplevel window
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        # Create label
        label = ttk.Label(self.tooltip, text=self.text, background="#ffffd7",
                         font=("Segoe UI", 9), padding=(5, 3))
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# Modern GUI implementation
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Structure Visualization")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f5f5f5")
        self.large_tree_threshold = 2000

        # Initialize data structures
        self.bst = BST()
        self.ht = HashTable()
        self.values = []
        
        # ← Add this line to initialize zoom level
        self.bst_zoom = 1.0
        self.max_depth_var = tk.IntVar(value=0)

        # Setup color scheme
        self.colors = {
            "primary": "#4285f4",      # Google Blue
            "secondary": "#34a853",    # Google Green
            "accent": "#fbbc05",       # Google Yellow 
            "warning": "#ea4335",      # Google Red
            "light_bg": "#f8f9fa",
            "dark_bg": "#202124",
            "text": "#202124",
            "border": "#dadce0"
        }
        
        # Load and configure fonts
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=10)
        
        # Configure ttk style
        self.setup_styles()
        
        # Build UI
        self.setup_ui()
        
        # Add a status bar
        self.setup_status_bar()
    
    def setup_styles(self):
        """Configure ttk styles for a modern look"""
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Base theme
        
        # Configure frame styles
        self.style.configure('Main.TFrame', background=self.colors["light_bg"])
        self.style.configure('Card.TFrame', background='white', relief='solid', borderwidth=1)
        self.style.configure('TabContent.TFrame', background='white', relief='flat', borderwidth=0)

        # Configure label styles
        self.style.configure('TLabel', background=self.colors["light_bg"], foreground=self.colors["text"], font=("Segoe UI", 10))
        self.style.configure('Card.TLabel', background='white', foreground=self.colors["text"], font=("Segoe UI", 10))
        self.style.configure('Title.TLabel', font=("Segoe UI", 16, "bold"))
        self.style.configure('Subtitle.TLabel', font=("Segoe UI", 14, "bold"))
        self.style.configure('Heading.TLabel', font=("Segoe UI", 12, "bold"))
        self.style.configure('Status.TLabel', background=self.colors["dark_bg"], foreground="white",
                          font=("Segoe UI", 9))
        
        # Configure button styles
        self.style.configure('TButton', font=("Segoe UI", 10), padding=8)
        self.style.configure('Primary.TButton', background=self.colors["primary"], foreground="white")
        self.style.configure('Success.TButton', background=self.colors["secondary"], foreground="white")
        self.style.configure('Warning.TButton', background=self.colors["warning"], foreground="white")
        self.style.configure('Action.TButton', background=self.colors["accent"], foreground=self.colors["text"])
        
        self.style.map('Primary.TButton', 
                    background=[('active', '#1a73e8'), ('pressed', '#1967d2')],
                    foreground=[('active', 'white'), ('pressed', 'white')])
        
        self.style.map('Success.TButton', 
                    background=[('active', '#2d9748'), ('pressed', '#27813f')],
                    foreground=[('active', 'white'), ('pressed', 'white')])
        
        self.style.map('Warning.TButton', 
                    background=[('active', '#d93025'), ('pressed', '#c5221f')],
                    foreground=[('active', 'white'), ('pressed', 'white')])
        
        self.style.map('Action.TButton', 
                    background=[('active', '#f6b000'), ('pressed', '#f29900')],
                    foreground=[('active', self.colors["text"]), ('pressed', self.colors["text"])])
        
        # Notebook style (tabs)
        self.style.configure(
            'TNotebook',
            background='white',        # content pane
            borderwidth=0,
            tabmargins=[2, 5, 2, 5]     # left, top, right, bottom
        )
        self.style.configure(
            'TNotebook.Tab',
            padding=(10, 5),
            font=("Segoe UI", 10),
            background=self.colors["light_bg"],    # un‐selected
            borderwidth=0
        )
        self.style.map(
            'TNotebook.Tab',
            background=[
                ('selected', 'white'),            # selected = white
                ('!selected', self.colors["light_bg"])
            ],
            foreground=[
                ('selected', self.colors["primary"]),
                ('!selected', self.colors["text"])
            ]
        )

        # Card LabelFrame → white background
        self.style.configure('Card.TLabelframe',
                             background='white',
                             relief='solid',
                             borderwidth=1)
        self.style.configure('Card.TLabelframe.Label',
                             background='white',
                             foreground=self.colors["text"])

    def setup_ui(self):
        """Set up the main user interface with dashboard layout"""
        # Main container
        main_container = ttk.Frame(self.root, style='Main.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Application title
        title_frame = ttk.Frame(main_container, style='Main.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Data Structure Visualization & Comparison", 
                              style='Title.TLabel')
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Create a resizable paned window for dashboard layout
        self.main_paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Control Center
        self.control_panel = ttk.Frame(self.main_paned, style='Card.TFrame', padding=10)
        self.main_paned.add(self.control_panel, weight=30)
        
        # Right panel - Visualization area
        viz_panel = ttk.Frame(self.main_paned, style='Card.TFrame')
        self.main_paned.add(viz_panel, weight=70)
        
        # Set up the control center with tabs
        self.setup_control_center()
        
        # Set up visualization area with notebook tabs
        self.setup_visualization_area(viz_panel)

    def setup_control_center(self):
        """Create the control center with tabbed interface"""
        # Control center title
        control_title = ttk.Label(self.control_panel, text="Control Center", 
                                style='Subtitle.TLabel')
        control_title.pack(pady=(0, 10))
        
        # Create tabbed interface
        control_tabs = ttk.Notebook(self.control_panel)
        control_tabs.pack(fill=tk.BOTH, expand=True)
        
        # Data Management Tab
        data_tab = ttk.Frame(control_tabs, style='TabContent.TFrame', padding=10)
        control_tabs.add(data_tab, text="Data")
        
        # Testing Tab
        test_tab = ttk.Frame(control_tabs, style='TabContent.TFrame', padding=10)
        control_tabs.add(test_tab, text="Test")
        
        # Analysis Tab
        analysis_tab = ttk.Frame(control_tabs, style='TabContent.TFrame', padding=10)
        control_tabs.add(analysis_tab, text="Analysis")
        
        # Setup each tab's content
        self.setup_data_tab(data_tab)
        self.setup_test_tab(test_tab)
        self.setup_analysis_tab(analysis_tab)
        
        # Stats section at the bottom
        stats_frame = ttk.LabelFrame(self.control_panel, text="Statistics", padding=10)
        stats_frame = ttk.LabelFrame(self.control_panel, text="Statistics", padding=10,  style='Card.TLabelframe')
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_label = ttk.Label(stats_frame, text="Items: 0\nBST Height: 0")
        self.stats_label.pack(fill=tk.X)

        control_tabs = ttk.Notebook(self.control_panel, style='TNotebook')
        control_tabs.pack(fill=tk.BOTH, expand=True)

    def setup_data_tab(self, parent):
        """Setup the Data Management tab"""
        # Manual Insert Section
        manual_frame = ttk.LabelFrame(parent, text="Manual Insert", padding=10)
        manual_frame = ttk.LabelFrame(parent, text="Manual Insert", padding=10, style='Card.TLabelframe')
        manual_frame.pack(fill=tk.X, pady=5)
        
        input_frame = ttk.Frame(manual_frame)
        input_frame = ttk.Frame(manual_frame, style='Card.TFrame')
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Value:").pack(side=tk.LEFT, padx=(0, 5))
        self.style.configure('Clean.TEntry', borderwidth=1)
        self.style.map('Clean.TEntry', fieldbackground=[('!disabled', 'white')])
        self.entry = ttk.Entry(input_frame, width=10, style='Clean.TEntry')
        self.entry.pack(side=tk.LEFT, padx=(0, 5))
        
        button_frame = ttk.Frame(manual_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        insert_btn = ttk.Button(button_frame, text="Insert Value", style="Primary.TButton",
                              command=self.insert_value)
        insert_btn.pack(fill=tk.X, pady=2)
        ToolTip(insert_btn, "Insert the value into both data structures")

        # Bulk Insert Section
        bulk_frame = ttk.LabelFrame(parent, text="Bulk Insert", padding=10)
        bulk_frame = ttk.LabelFrame(parent, text="Bulk Insert", padding=10, style='Card.TLabelframe')
        bulk_frame.pack(fill=tk.X, pady=10)
        
        random_btn = ttk.Button(bulk_frame, text="Add 50 Random Values", 
                              style="Success.TButton", command=self.insert_random)
        random_btn.pack(fill=tk.X, pady=2)
        ToolTip(random_btn, "Insert 50 random integers between 1 and 1000")
        
        large_dataset_btn = ttk.Button(bulk_frame, text="Add 10,000 Values", 
                                     style="Action.TButton", command=self.insert_large_dataset)
        large_dataset_btn.pack(fill=tk.X, pady=2)
        ToolTip(large_dataset_btn, "Insert 10,000 random integers (may take a moment)")
        
        # Data Management Section
        manage_frame = ttk.LabelFrame(parent, text="Data Management", padding=10)
        manage_frame = ttk.LabelFrame(parent, text="Data Management", padding=10, style='Card.TLabelframe')
        manage_frame.pack(fill=tk.X, pady=10)
        
        reset_btn = ttk.Button(manage_frame, text="Clear All Data", 
                            style="Warning.TButton", command=self.reset_all)
        reset_btn.pack(fill=tk.X, pady=2)
        ToolTip(reset_btn, "Remove all data from both structures")

        balance_btn = ttk.Button(manage_frame, text="Balance Tree", 
                         style="Success.TButton", command=self.balance_tree)
        balance_btn.pack(fill=tk.X, pady=2)
        ToolTip(balance_btn, "Balance the Binary Search Tree")

    def setup_test_tab(self, parent):
        """Setup the Testing tab"""
        # Search Section
        search_frame = ttk.LabelFrame(parent, text="Search Operations", padding=10)
        search_frame = ttk.LabelFrame(parent, text="Search Operations", padding=10, style='Card.TLabelframe')
        search_frame.pack(fill=tk.X, pady=5)
        
        simple_search_btn = ttk.Button(search_frame, text="Search Value", style="Primary.TButton", 
                                    command=self.search_value)
        simple_search_btn.pack(fill=tk.X, pady=2)
        ToolTip(simple_search_btn, "Search for the value in both data structures")
        
        # Animated Simulation Section
        sim_frame = ttk.LabelFrame(parent, text="Visualization", padding=10)
        sim_frame = ttk.LabelFrame(parent, text="Visualization", padding=10, style='Card.TLabelframe')
        sim_frame.pack(fill=tk.X, pady=10)
        
        sim_btn = ttk.Button(sim_frame, text="Simulate Lookup Process", 
                          style="Success.TButton", command=self.show_search_simulation)
        sim_btn.pack(fill=tk.X, pady=5)
        ToolTip(sim_btn, "Open a new window with animated search visualization")

    def setup_analysis_tab(self, parent):
        """Setup the Analysis tab"""
        # Performance Testing
        perf_frame = ttk.LabelFrame(parent, text="Performance Testing", padding=10)
        perf_frame = ttk.LabelFrame(parent, text="Performance Testing", padding=10, style='Card.TLabelframe')
        perf_frame.pack(fill=tk.X, pady=5)
        
        # Test configuration section
        config_frame = ttk.Frame(perf_frame)
        config_frame = ttk.Frame(perf_frame, style='Card.TFrame')
        config_frame.pack(fill=tk.X, pady=5)
        
        # Max sample size with slider
        ttk.Label(config_frame, text="Maximum Sample Size:").pack(anchor='w', pady=(0, 5))
        
        sample_frame = ttk.Frame(config_frame)
        sample_frame = ttk.Frame(config_frame, style='Card.TFrame')
        sample_frame.pack(fill=tk.X)
        
        self.search_count = tk.StringVar(value="100")
        self.sample_label = ttk.Label(sample_frame, text="100", width=8)
        self.sample_label.pack(side=tk.RIGHT)
        
        sample_slider = ttk.Scale(sample_frame, from_=0, to=5, orient=tk.HORIZONTAL,
                               length=150, command=self.update_sample_size)
        sample_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sample_slider.set(1)  # Default to 100 (index 1)
        
        # Test type selection
        ttk.Label(config_frame, text="Test Type:").pack(anchor='w', pady=(10, 5))
        
        self.test_type = tk.StringVar(value="Random")
        self.style.configure('Card.TRadiobutton', background='white')

        test_types = [("Random", "Random lookups from your data"),
                    ("Best-case", "Always search for the first value"),
                    ("Worst-case", "Search for values that don't exist")]
        
        for test, description in test_types:
            test_frame = ttk.Frame(config_frame)
            test_frame = ttk.Frame(config_frame, style='Card.TFrame')
            test_frame.pack(fill=tk.X, pady=2)
            
            radio = ttk.Radiobutton(test_frame, text=test, value=test, variable=self.test_type)
            radio = ttk.Radiobutton(test_frame, text=test, value=test, variable=self.test_type, style='Card.TRadiobutton')
            radio.pack(side=tk.LEFT)
            ToolTip(radio, description)
        
        # Run comparison button
        run_frame = ttk.Frame(perf_frame)
        run_frame.pack(fill=tk.X, pady=10)
        
        compare_btn = ttk.Button(run_frame, text="Run Performance Comparison", 
                              style="Action.TButton", command=self.compare_times)
        compare_btn.pack(fill=tk.X)
        ToolTip(compare_btn, "Compare BST and Hash Table lookup performance across sample sizes")

    def update_sample_size(self, value):
        """Update the sample size based on slider position"""
        # Convert slider value to sample size
        sizes = [30, 100, 500, 1000, 5000, 10000]
        index = min(int(float(value)), len(sizes)-1)
        self.search_count.set(str(sizes[index]))
        self.sample_label.config(text=str(sizes[index]))

    def setup_visualization_area(self, parent):
        """Set up the visualization area with tabs"""
        # Create a notebook for visualizations
        self.viz_notebook = ttk.Notebook(parent)
        self.viz_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Binary Search Tree visualization tab - apply white background
        bst_frame = ttk.Frame(self.viz_notebook, padding=5, style='TabContent.TFrame')
        self.viz_notebook.add(bst_frame, text="Binary Search Tree")
        
        # Hash Table visualization tab - apply white background
        hash_frame = ttk.Frame(self.viz_notebook, padding=5, style='TabContent.TFrame')
        self.viz_notebook.add(hash_frame, text="Hash Table")
        
        # Performance Comparison tab - apply white background
        comp_frame = ttk.Frame(self.viz_notebook, padding=5, style='TabContent.TFrame')
        self.viz_notebook.add(comp_frame, text="Performance Comparison")
        
        # Setup each visualization
        self.setup_bst_visualization(bst_frame)
        self.setup_hash_visualization(hash_frame)
        self.setup_comparison_visualization(comp_frame)

    def setup_bst_visualization(self, parent):
        """Setup the BST visualization tab"""
        # Info panel at the top
        info_frame = ttk.Frame(parent, style='TabContent.TFrame')
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(info_frame, text="Binary Search Tree Visualization", 
                style="Heading.TLabel").pack(side=tk.LEFT)
        
        # Legend for BST
        legend_frame = ttk.Frame(info_frame, style='TabContent.TFrame')
        legend_frame.pack(side=tk.RIGHT)
        
        self.create_legend_item(legend_frame, self.colors["primary"], "Node")
        self.create_legend_item(legend_frame, "#666666", "Edge")
        
        # Scrollable canvas for BST
        canvas_frame = ttk.Frame(parent, style='TabContent.TFrame')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.canvas.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas.configure(yscrollcommand=y_scrollbar.set, 
                           xscrollcommand=x_scrollbar.set,
                           scrollregion=(0, 0, 1200, 2000))
        
        # Add zoom controls
        zoom_frame = ttk.Frame(parent)
        zoom_frame.pack(side=tk.BOTTOM, anchor='e', padx=5, pady=5)
        
        zoom_in_btn = ttk.Button(zoom_frame, text="➕", width=3, command=lambda: self.zoom_bst(1.2))
        zoom_in_btn.pack(side=tk.LEFT, padx=2)
        ToolTip(zoom_in_btn, "Zoom in")
        
        zoom_out_btn = ttk.Button(zoom_frame, text="➖", width=3, command=lambda: self.zoom_bst(0.8))
        zoom_out_btn.pack(side=tk.LEFT, padx=2)
        ToolTip(zoom_out_btn, "Zoom out")
        
        reset_view_btn = ttk.Button(zoom_frame, text="Reset View", command=self.reset_bst_view)
        reset_view_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(reset_view_btn, "Reset zoom and position")
        
        # Add mouse wheel zoom support
        self.canvas.bind("<MouseWheel>", self.mouse_wheel_zoom)  # Windows
        self.canvas.bind("<Button-4>", self.mouse_wheel_zoom)    # Linux
        self.canvas.bind("<Button-5>", self.mouse_wheel_zoom)    # Linux
        
        # Add drag-to-pan support
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan_canvas)
        
        # For tracking pan operations
        self.pan_start_x = 0
        self.pan_start_y = 0

        # ensure all tree items get the tag “tree”
        self.tree_tag = "tree"

    def mouse_wheel_zoom(self, event):
        """Zoom in/out with mouse wheel"""
        # Determine zoom direction
        if event.num == 5 or event.delta < 0:  # Zoom out
            self.zoom_bst(0.9)
        if event.num == 4 or event.delta > 0:  # Zoom in
            self.zoom_bst(1.1)
        return "break"  # Prevent default behavior

    def start_pan(self, event):
        """Start panning the canvas"""
        self.canvas.scan_mark(event.x, event.y)
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def pan_canvas(self, event):
        """Pan the canvas as the mouse moves"""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def update_depth_limit(self):
        """Update depth limit and redraw the tree"""
        self.depth_label.config(text=str(self.max_depth_var.get()))
        self.draw_visuals()

    def set_max_depth(self, depth):
        """Set a specific depth limit"""
        self.max_depth_var.set(depth)
        self.depth_label.config(text="All" if depth == 0 else str(depth))
        self.draw_visuals()

    def zoom_bst(self, factor):
        """Zoom in or out on the BST visualization"""
        self.bst_zoom *= factor
        self.draw_visuals()  # Redraw with new zoom

    def reset_bst_view(self):
        """Reset BST view to original size and position"""
        self.bst_zoom = 1.0
        self.draw_visuals()
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0.5)

    def create_legend_item(self, parent, color, text):
        """Create a legend item with color box and label"""
        frame = ttk.Frame(parent)
        frame.pack(side=tk.LEFT, padx=10)
        
        # Color box
        color_box = tk.Canvas(frame, width=15, height=15, bg=color, highlightthickness=0)
        color_box.pack(side=tk.LEFT, padx=(0, 5))
        
        # Label
        ttk.Label(frame, text=text).pack(side=tk.LEFT)

    def setup_hash_visualization(self, parent):
        """Setup the Hash Table visualization tab"""
        # Info panel at the top
        info_frame = ttk.Frame(parent, style='TabContent.TFrame')
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(info_frame, text="Hash Table Visualization", 
                style="Heading.TLabel").pack(side=tk.LEFT)
        
        # Legend for Hash Table
        legend_frame = ttk.Frame(info_frame, style='TabContent.TFrame')
        legend_frame.pack(side=tk.RIGHT)
        
        self.create_legend_item(legend_frame, "#e6e6e6", "Bucket Index")
        self.create_legend_item(legend_frame, "#f0f0f0", "Bucket Values")
        
        # Scrollable canvas for Hash Table
        hash_canvas_frame = ttk.Frame(parent, style='TabContent.TFrame')
        hash_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.hash_canvas = tk.Canvas(hash_canvas_frame, bg="white", highlightthickness=0)
        self.hash_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        hash_y_scrollbar = ttk.Scrollbar(hash_canvas_frame, orient=tk.VERTICAL, 
                                      command=self.hash_canvas.yview)
        hash_y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        hash_x_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, 
                                      command=self.hash_canvas.xview)
        hash_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.hash_canvas.configure(yscrollcommand=hash_y_scrollbar.set, 
                                xscrollcommand=hash_x_scrollbar.set,
                                scrollregion=(0, 0, 600, 1000))
        
        # Information panel at the bottom
        info_label = ttk.Label(parent, text="The hash function used is: h(key) = key % table_size", 
                            font=("Segoe UI", 9, "italic"))
        info_label.pack(side=tk.BOTTOM, anchor='w', padx=5, pady=5)

    def setup_comparison_visualization(self, parent):
        """Setup the Performance Comparison tab"""
        # Info panel at the top
        info_frame = ttk.Frame(parent, style='TabContent.TFrame')
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(info_frame, text="Performance Comparison", 
                style="Heading.TLabel").pack(side=tk.LEFT)
        
        # Create scrollable canvas for results
        comp_canvas_frame = ttk.Frame(parent, style='TabContent.TFrame')
        comp_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.comp_canvas = tk.Canvas(comp_canvas_frame, bg="white", highlightthickness=0)
        self.comp_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        comp_y_scrollbar = ttk.Scrollbar(comp_canvas_frame, orient=tk.VERTICAL, 
                                       command=self.comp_canvas.yview)
        comp_y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        comp_x_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, 
                                       command=self.comp_canvas.xview)
        comp_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.comp_canvas.configure(yscrollcommand=comp_y_scrollbar.set, 
                                xscrollcommand=comp_x_scrollbar.set)
        
        # Create a frame inside the canvas for charts
        self.comp_inner_frame = ttk.Frame(self.comp_canvas)
        self.comp_inner_frame = ttk.Frame(self.comp_canvas, style='TabContent.TFrame')
        self.comp_canvas.create_window((0, 0), window=self.comp_inner_frame, anchor='nw')
        
        # Placeholder message
        self.comp_label = ttk.Label(self.comp_inner_frame, 
                                 text="Run a performance comparison to see results", 
                                 style="Heading.TLabel")
        self.comp_label.pack(pady=50)
        
        # Bind frame size changes to update scroll region
        self.comp_inner_frame.bind('<Configure>', lambda e: 
                                 self.comp_canvas.configure(scrollregion=self.comp_canvas.bbox("all")))

    def setup_status_bar(self):
        """Create a status bar at the bottom of the window"""
        status_frame = ttk.Frame(self.root, style='TFrame')
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_bar = ttk.Label(status_frame, text="Ready", style='Status.TLabel')
        self.status_bar.pack(fill=tk.X, ipady=2)

    def update_status(self, message):
        """Update the status bar message"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()

    def insert_value(self):
        """Insert a single value from the entry field"""
        try:
            val = int(self.entry.get())
            self.values.append(val)
            self.bst.insert(val)
            self.ht.insert(val)
            self.entry.delete(0, tk.END)
            self.update_stats()
            self.draw_visuals()
            self.update_status(f"Inserted value: {val}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer.")
            self.update_status("Error: Invalid input")

    def insert_random(self):
        """Insert 50 random values"""
        self.update_status("Adding 50 random values...")
        for _ in range(50):
            val = random.randint(1, 1000)
            self.values.append(val)
            self.bst.insert(val)
            self.ht.insert(val)
        self.update_stats()
        self.draw_visuals()
        self.update_status(f"Added 50 random values. Total items: {len(self.values)}")

    def search_value(self):
        """Search for a value and compare performance"""
        try:
            val = int(self.entry.get())
            
            self.update_status(f"Searching for value: {val}...")
            
            bst_start = time.perf_counter()
            bst_result = self.bst.search(val)
            bst_time = time.perf_counter() - bst_start
            
            ht_start = time.perf_counter()
            ht_result = self.ht.search(val)
            ht_time = time.perf_counter() - ht_start
            
            # Create a styled result dialog
            result_dialog = tk.Toplevel(self.root)
            result_dialog.title("Search Results")
            result_dialog.geometry("400x250")
            result_dialog.transient(self.root)
            result_dialog.grab_set()
            
            # Style the dialog
            result_frame = ttk.Frame(result_dialog, padding=20)
            result_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(result_frame, text=f"Search Results for {val}", 
                    style="Subtitle.TLabel").pack(pady=(0, 15))
            
            # BST result
            bst_frame = ttk.Frame(result_frame, style="Card.TFrame", padding=10)
            bst_frame.pack(fill=tk.X, pady=5)
            
            bst_color = self.colors["secondary"] if bst_result else self.colors["warning"]
            bst_status = "Found" if bst_result else "Not Found"
            
            ttk.Label(bst_frame, text="Binary Search Tree:", 
                    font=("Segoe UI", 11, "bold")).pack(anchor='w')
            ttk.Label(bst_frame, text=f"Status: {bst_status}",
                    foreground=bst_color).pack(anchor='w')
            ttk.Label(bst_frame, text=f"Time: {bst_time:.8f} seconds",
                    font=("Consolas", 10)).pack(anchor='w')
            
            # Hash Table result
            ht_frame = ttk.Frame(result_frame, style="Card.TFrame", padding=10)
            ht_frame.pack(fill=tk.X, pady=5)
            
            ht_color = self.colors["secondary"] if ht_result else self.colors["warning"]
            ht_status = "Found" if ht_result else "Not Found"
            
            ttk.Label(ht_frame, text="Hash Table:", 
                    font=("Segoe UI", 11, "bold")).pack(anchor='w')
            ttk.Label(ht_frame, text=f"Status: {ht_status}", 
                    foreground=ht_color).pack(anchor='w')
            ttk.Label(ht_frame, text=f"Time: {ht_time:.8f} seconds",
                    font=("Consolas", 10)).pack(anchor='w')
            
            # Comparison
            if bst_time > 0 and ht_time > 0:
                speedup = bst_time / ht_time if ht_time > bst_time else ht_time / bst_time
                faster = "Hash Table" if ht_time < bst_time else "BST"
                
                ttk.Separator(result_frame, orient='horizontal').pack(fill=tk.X, pady=10)
                ttk.Label(result_frame, text=f"{faster} was {speedup:.1f}x faster",
                        font=("Segoe UI", 10, "bold")).pack()
            
            # Close button
            ttk.Button(result_frame, text="Close", command=result_dialog.destroy).pack(pady=10)
            
            self.update_status("Search completed")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer.")
            self.update_status("Error: Invalid input")

    def compare_times(self):
        """Compare lookup times between BST and Hash Table across multiple sample sizes"""
        if not self.values:
            messagebox.showwarning("No Data", "Insert values first to compare.")
            return
        
        # Clear previous charts
        for widget in self.comp_inner_frame.winfo_children():
            widget.destroy()
        
        # Main title for the comparison tab
        ttk.Label(self.comp_inner_frame, text="Performance Comparison Across Sample Sizes", 
                style="Subtitle.TLabel").pack(pady=(10, 5))
        
        # Processing indicator
        process_frame = ttk.Frame(self.comp_inner_frame)
        process_frame.pack(fill=tk.X, pady=10)
        
        process_label = ttk.Label(process_frame, text="Processing... Please wait")
        process_label.pack(side=tk.LEFT, padx=10)
        
        progress = ttk.Progressbar(process_frame, mode='indeterminate', length=200)
        progress.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        progress.start()
        
        self.root.update()
        self.update_status("Running performance comparison...")
        
        # Define all standard sample sizes
        all_sample_sizes = [30, 100, 500, 1000, 5000, 10000]
        
        # Get the selected maximum sample size from the slider/variable
        try:
            # Parse the value, removing any commas
            max_sample = int(self.search_count.get().replace(',', ''))
            
            # Include all sample sizes up to and including the selected value
            sample_sizes = [size for size in all_sample_sizes if size <= max_sample]
        except ValueError:
            # Fallback to default sample sizes if there's an error
            sample_sizes = [100]
        
        # Check if we have enough data
        available_samples = [size for size in sample_sizes if size <= len(self.values)]
        
        # Show a message if none of the sample sizes can be used
        if not available_samples:
            messagebox.showwarning(
                "Insufficient Data", 
                f"You selected a maximum sample size of {max_sample} but only have {len(self.values)} values. " 
                f"Please add more data or select a smaller sample size."
            )
            process_frame.destroy()
            self.update_status("Comparison aborted: Insufficient data")
            return
        
        # Get the test type selection from the variable
        test_type = self.test_type.get()
        all_stats = []
        
        # Run tests for each available sample size
        for sample_size in available_samples:
            bst_times = []
            ht_times = []
            
            # Select lookup values based on test type
            if test_type == "Random":
                search_vals = random.sample(self.values, sample_size)
            elif test_type == "Best-case":
                # Best-case: Search for the first inserted value
                search_vals = [self.values[0]] * sample_size
            elif test_type == "Worst-case":
                # Worst-case: Searching for a value known not to exist
                search_vals = [-1] * sample_size
            else:
                search_vals = random.sample(self.values, sample_size)
            
            # Perform searches and measure times
            for val in search_vals:
                t1 = time.perf_counter()
                self.bst.search(val)
                bst_times.append(time.perf_counter() - t1)

                t2 = time.perf_counter()
                self.ht.search(val)
                ht_times.append(time.perf_counter() - t2)
            
            bst_avg = sum(bst_times) / len(bst_times)
            ht_avg = sum(ht_times) / len(ht_times)
            speedup = bst_avg / ht_avg if ht_avg > 0 else 0
            
            all_stats.append({
                'sample_size': sample_size,
                'bst_avg': bst_avg,
                'ht_avg': ht_avg,
                'speedup': speedup
            })
            
            # Create a card for this sample size
            card_frame = ttk.Frame(self.comp_inner_frame, style="Card.TFrame")
            card_frame.pack(fill=tk.X, padx=20, pady=10)
            
            # Header with sample size and stats
            header_frame = ttk.Frame(card_frame, padding=10)
            header_frame = ttk.Frame(card_frame, padding=10, style='Card.TFrame')
            header_frame.pack(fill=tk.X)
            
            ttk.Label(header_frame, text=f"Sample Size: {sample_size} Searches", 
                   style="Heading.TLabel").pack(side=tk.LEFT)
            
            # Efficiency display on the right
            faster = "Hash Table" if ht_avg < bst_avg else "BST"
            factor = max(bst_avg, ht_avg) / min(bst_avg, ht_avg) if min(bst_avg, ht_avg) > 0 else 0
            
            eff_frame = ttk.Frame(header_frame)
            eff_frame = ttk.Frame(header_frame, style='Card.TFrame')
            eff_frame.pack(side=tk.RIGHT)
            
            ttk.Label(eff_frame, text=f"{faster} was ", font=("Segoe UI", 10), style='Card.TLabel').pack(side=tk.LEFT)
            ttk.Label(eff_frame, text=f"{factor:.1f}x", style='Card.TLabel', font=("Segoe UI", 10, "bold"), foreground=self.colors["secondary"]).pack(side=tk.LEFT)
            ttk.Label(eff_frame, text=" faster", font=("Segoe UI", 10), style='Card.TLabel').pack(side=tk.LEFT)
            
            # Stats in the middle
            stats_frame = ttk.Frame(card_frame, padding=(10, 0, 10, 10))
            stats_frame = ttk.Frame(card_frame, padding=(10, 0, 10, 10), style='Card.TFrame')
            stats_frame.pack(fill=tk.X)
            
            # BST stats
            bst_stat_frame = ttk.Frame(stats_frame)
            bst_stat_frame = ttk.Frame(stats_frame, style='Card.TFrame')
            bst_stat_frame.pack(side=tk.LEFT, padx=10)
            
            ttk.Label(bst_stat_frame, text="BST Average:",  
                   font=("Segoe UI", 9), style='Card.TLabel').pack(anchor='w')
            ttk.Label(bst_stat_frame, text=f"{bst_avg:.8f} seconds", 
                   font=("Consolas", 9, "bold"), 
                   foreground=self.colors["primary"], style='Card.TLabel').pack(anchor='w')
            
            # HT stats
            ht_stat_frame = ttk.Frame(stats_frame)
            ht_stat_frame = ttk.Frame(stats_frame, style='Card.TFrame')
            ht_stat_frame.pack(side=tk.LEFT, padx=10)
            
            ttk.Label(ht_stat_frame, text="Hash Table Average:", 
                   font=("Segoe UI", 9), style='Card.TLabel').pack(anchor='w')
            ttk.Label(ht_stat_frame, text=f"{ht_avg:.8f} seconds", 
                   font=("Consolas", 9, "bold"), 
                   foreground=self.colors["primary"], style='Card.TLabel').pack(anchor='w')
            
            # Create line plot for the current sample size
            fig = plt.Figure(figsize=(9, 3), dpi=100)
            ax = fig.add_subplot(111)
            chart = FigureCanvasTkAgg(fig, card_frame)
            chart.get_tk_widget().pack(padx=10, pady=5, fill=tk.X)
            
            # Customize the plot appearance
            ax.plot(bst_times, label='BST', marker='o', markersize=3, 
                 color=self.colors["primary"], alpha=0.8, linewidth=1)
            ax.plot(ht_times, label='Hash Table', marker='x', markersize=3, 
                 color=self.colors["warning"], alpha=0.8, linewidth=1)
            
            ax.set_xlabel('Search #')
            ax.set_ylabel('Time (s)')
            ax.set_title(f'Lookup Performance ({sample_size} searches) - {test_type} test')
            ax.legend()
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
        
        # Remove processing indicator
        process_frame.destroy()
        
        # Create summary chart if we have multiple sample sizes
        if len(available_samples) > 1:
            self.create_summary_chart(all_stats)
        
        self.comp_canvas.configure(scrollregion=self.comp_canvas.bbox("all"))
        self.update_status(f"Completed performance comparison across {len(available_samples)} sample sizes")

    def create_summary_chart(self, stats):
        """Create a summary chart comparing all sample sizes"""
        # Create a separator
        ttk.Separator(self.comp_inner_frame, orient='horizontal').pack(fill=tk.X, padx=20, pady=20)
        
        # Create summary section
        summary_frame = ttk.Frame(self.comp_inner_frame, style="Card.TFrame")
        summary_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(summary_frame, text="Summary Comparison", 
               style="Heading.TLabel").pack(pady=10)
        
        # Extract data for the chart
        sample_sizes = [stat['sample_size'] for stat in stats]
        bst_avgs = [stat['bst_avg'] for stat in stats]
        ht_avgs = [stat['ht_avg'] for stat in stats]
        
        # Create the chart
        fig = plt.Figure(figsize=(9, 5), dpi=100)
        ax = fig.add_subplot(111)
        chart = FigureCanvasTkAgg(fig, summary_frame)
        chart.get_tk_widget().pack(padx=20, pady=10, fill=tk.BOTH)
        
        # Plot the data with nicer styling
        width = 0.35
        x = range(len(sample_sizes))
        
        bst_bars = ax.bar([i - width/2 for i in x], bst_avgs, width, label='BST', 
                        color=self.colors["primary"], alpha=0.8)
        ht_bars = ax.bar([i + width/2 for i in x], ht_avgs, width, label='Hash Table', 
                       color=self.colors["warning"], alpha=0.8)
        
        # Add value labels on top of bars
        for bar in bst_bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.00001,
                 f'{height:.7f}',
                 ha='center', va='bottom', rotation=90, fontsize=8)
        
        for bar in ht_bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.00001,
                 f'{height:.7f}',
                 ha='center', va='bottom', rotation=90, fontsize=8)
        
        # Customize the chart
        ax.set_ylabel('Average Time (s)')
        ax.set_xlabel('Sample Size')
        ax.set_title(f'Lookup Performance Comparison by Sample Size - {self.test_type.get()} Test')
        ax.set_xticks(x)
        ax.set_xticklabels(sample_sizes)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add a note about the results
        best_for_small = "Hash Table" if ht_avgs[0] < bst_avgs[0] else "BST"
        best_for_large = "Hash Table" if ht_avgs[-1] < bst_avgs[-1] else "BST"
        
        note_text = (f"• For small samples ({sample_sizes[0]} searches), {best_for_small} performed better.\n"
                   f"• For large samples ({sample_sizes[-1]} searches), {best_for_large} performed better.")
        
        ttk.Label(summary_frame, text="Analysis:", 
               font=("Segoe UI", 11, "bold")).pack(anchor='w', padx=20, pady=(10, 5))
        ttk.Label(summary_frame, text=note_text, 
               font=("Segoe UI", 10)).pack(anchor='w', padx=20, pady=(0, 10))
        
        # Add explanation of time complexity
        complexity_text = (
            "Time Complexity:\n"
            "• BST: O(log n) average case, O(n) worst case (unbalanced tree)\n"
            "• Hash Table: O(1) average case, O(n) worst case (many collisions)"
        )
        
        ttk.Label(summary_frame, text=complexity_text, 
               font=("Segoe UI", 9), foreground="#555555").pack(anchor='w', padx=20, pady=(0, 10))

    def _compute_node_positions(self):
        """
        Assign each node a depth and an x-position so that
        parents are centered over their children.
        """
        # 1) In-order pass to give every node a unique leaf index
        in_index = {}
        counter = {'x': 0}
        def _inorder(n):
            if not n: return
            _inorder(n.left)
            in_index[n] = counter['x']
            counter['x'] += 1
            _inorder(n.right)
        _inorder(self.bst.root)

        # 2) Post-order pass to compute final x as midpoint of children (or leaf index)
        positions = {}
        def _assign(n, depth=0):
            if not n: return
            _assign(n.left, depth+1)
            _assign(n.right, depth+1)
            if n.left and n.right:
                x = (positions[n.left][0] + positions[n.right][0]) / 2
            elif n.left:
                x = positions[n.left][0]
            elif n.right:
                x = positions[n.right][0]
            else:
                x = in_index[n]
            positions[n] = (x, depth)
        _assign(self.bst.root, 0)
        return positions
    
    def draw_visuals(self):
        """Draw visualizations of both data structures with even spacing."""
        self.canvas.delete("all")
        self.hash_canvas.delete("all")

        # Decide simple vs detailed
        self.simple_render = len(self.values) > self.large_tree_threshold

        # First compute even positions for each BST node
        node_pos = self._compute_node_positions()
        if node_pos:
            # horizontal & vertical spacing
            h_spacing = 40 * self.bst_zoom
            v_spacing = 40 * self.bst_zoom
            x_offset = 30    # left margin
            y_offset = 30    # top margin

            # Draw edges first
            for node, (col, depth) in node_pos.items():
                x, y = x_offset + col*h_spacing, y_offset + depth*v_spacing
                for child in (node.left, node.right):
                    if child and child in node_pos:
                        cx, cy = node_pos[child]
                        cx = x_offset + cx*h_spacing
                        cy = y_offset + (depth+1)*v_spacing
                        self.canvas.create_line(x, y, cx, cy,
                                                fill="#666", width=1,
                                                tags=(self.tree_tag,))

            # Draw nodes and labels
            for node, (col, depth) in node_pos.items():
                x, y = x_offset + col*h_spacing, y_offset + depth*v_spacing
                node_size = max(15*self.bst_zoom, 5)
                # circle
                self.canvas.create_oval(x-node_size, y-node_size,
                                        x+node_size, y+node_size,
                                        fill=self.colors["primary"], outline="",
                                        tags=(self.tree_tag,))
                if not self.simple_render:
                    self.canvas.create_arc(x-node_size, y-node_size,
                                           x+node_size, y-node_size+node_size*2,
                                           start=45, extent=180, fill="#3b77db", outline="",
                                           tags=(self.tree_tag,))
                # text
                font_size = max(int(9*self.bst_zoom), 7)
                self.canvas.create_text(x, y, text=str(node.key),
                                        fill="white",
                                        font=("Segoe UI", font_size),
                                        tags=(self.tree_tag,))

        # now the hash‐table
        self.draw_hashtable()
        # update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_bst_info_panel(self):
        """Update the BST information panel"""
        def count_nodes(node):
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)
        
        total_nodes = count_nodes(self.bst.root)
        visible_nodes = self.count_visible_nodes()
        max_depth = self.max_depth_var.get()
        
        info_text = (
            f"Total nodes: {total_nodes}\n"
            f"Visible nodes: {visible_nodes}\n"
            f"Depth limit: {max_depth if max_depth > 0 else 'All'}\n"
            f"Zoom level: {self.bst_zoom:.1f}x"
        )
    
        # Update your info panel with this text
        self.bst_info_label.config(text=info_text)

    def count_visible_nodes(self):
        """Count nodes that are within the current depth limit"""
        max_depth = self.max_depth_var.get()
        if max_depth == 0:
            return len(self.values)
        
        def count_to_depth(node, current_depth=0):
            if not node or (max_depth > 0 and current_depth > max_depth):
                return 0
            return 1 + count_to_depth(node.left, current_depth+1) + count_to_depth(node.right, current_depth+1)
    
        return count_to_depth(self.bst.root)

    def draw_tree(self, node, x, y, offset, current_depth=0):
        """Draw the BST on the canvas; in large mode skip 3D effects."""
        if not node:
            return
        max_depth = self.max_depth_var.get()
        if max_depth and current_depth>max_depth:
            self.canvas.create_text(x, y+20, text="…", font=("Segoe UI",14,"bold"), fill="#666")
            return

        # draw edges
        if node.left:
            self.canvas.create_line(x, y, x-offset, y+60,
                fill="#666", width=1, tags=(self.tree_tag,))
            self.draw_tree(node.left, x-offset, y+60, offset/1.5, current_depth+1)
        if node.right:
            self.canvas.create_line(x, y, x+offset, y+60,
                fill="#666", width=1, tags=(self.tree_tag,))
            self.draw_tree(node.right, x+offset, y+60, offset/1.5, current_depth+1)

        # draw node
        node_size = max(15*self.bst_zoom, 5)
        self.canvas.create_oval(x-node_size, y-node_size,
            x+node_size, y+node_size,
            fill=self.colors["primary"], outline="",
            tags=(self.tree_tag,))
        if not self.simple_render:
            self.canvas.create_arc(x-node_size, y-node_size,
                x+node_size, y+node_size,
                start=45, extent=180, fill="#3b77db", outline="",
                tags=(self.tree_tag,))

        # draw key
        font_size = max(int(9*self.bst_zoom),7)
        self.canvas.create_text(x, y, text=str(node.key),
            fill="white", font=("Segoe UI", font_size),
            tags=(self.tree_tag,))
        
    def draw_hashtable(self):
        """Draw the hash table visualization"""
        self.hash_canvas.delete("all")
        
        # Improved hash table styling
        table_width = 550
        row_height = 40
        header_height = 50
        
        # Draw title and explanation
        self.hash_canvas.create_text(50 + table_width/2, 20, 
                                  text="Hash Table Visualization", 
                                  fill=self.colors["text"], 
                                  font=("Segoe UI", 14, "bold"))
        
        # Draw table header
        self.hash_canvas.create_rectangle(50, 50, 50 + table_width, 50 + header_height, 
                                       fill=self.colors["primary"], outline="")
        
        # Header columns
        self.hash_canvas.create_line(150, 50, 150, 50 + header_height, 
                                  fill="white", width=2)
        
        # Header text
        self.hash_canvas.create_text(100, 50 + header_height/2, 
                                  text="Index", fill="white", 
                                  font=("Segoe UI", 12, "bold"))
        self.hash_canvas.create_text(150 + (table_width-150)/2, 50 + header_height/2, 
                                  text="Values (Collision Chain)", fill="white", 
                                  font=("Segoe UI", 12, "bold"))
        
        # Show a subset of buckets (first 50)
        visible_buckets = min(50, self.ht.size)
        
        # Count non-empty buckets for visualization
        non_empty = sum(1 for bucket in self.ht.table[:visible_buckets] if bucket)
        
        if non_empty > 0:
            # Show all non-empty buckets and some empty ones
            min_empty_to_show = min(10, visible_buckets - non_empty)
            
            # First show non-empty buckets
            row = 0
            y_start = 50 + header_height
            
            for i in range(visible_buckets):
                bucket = self.ht.table[i]
                if bucket:  # Non-empty bucket
                    y_pos = y_start + row * row_height
                    
                    # Alternating row colors
                    bg_color = "#f8f8f8" if row % 2 == 0 else "white"
                    
                    # Draw row background
                    self.hash_canvas.create_rectangle(50, y_pos, 
                                                   50 + table_width, 
                                                   y_pos + row_height, 
                                                   fill=bg_color, outline="#e0e0e0")
                    
                    # Draw index column
                    self.hash_canvas.create_rectangle(50, y_pos, 
                                                   150, y_pos + row_height, 
                                                   fill="#e6e6e6", outline="#d0d0d0")
                    self.hash_canvas.create_text(100, y_pos + row_height/2, 
                                              text=str(i), 
                                              font=("Consolas", 11, "bold"))
                    
                    # Format values in the bucket
                    if len(bucket) > 10:
                        # Show first 10 values with ellipsis
                        items_text = ", ".join(map(str, bucket[:10])) + f", ... (+{len(bucket) - 10} more)"
                    else:
                        items_text = ", ".join(map(str, bucket))
                    
                    # Draw bucket contents with overflow handling
                    self.hash_canvas.create_text(160, y_pos + row_height/2, 
                                              text=items_text, anchor="w", width=table_width-160-10,
                                              font=("Segoe UI", 10))
                    
                    row += 1
            
            # Now show some empty buckets
            empty_shown = 0
            for i in range(visible_buckets):
                bucket = self.ht.table[i]
                if not bucket and empty_shown < min_empty_to_show:  # Empty bucket
                    y_pos = y_start + row * row_height
                    
                    # Alternating row colors (lighter for empty)
                    bg_color = "#f9f9f9" if row % 2 == 0 else "white"
                    
                    # Draw row background
                    self.hash_canvas.create_rectangle(50, y_pos, 
                                                   50 + table_width, 
                                                   y_pos + row_height, 
                                                   fill=bg_color, outline="#e8e8e8")
                    
                    # Draw index column
                    self.hash_canvas.create_rectangle(50, y_pos, 
                                                   150, y_pos + row_height, 
                                                   fill="#f0f0f0", outline="#e0e0e0")
                    self.hash_canvas.create_text(100, y_pos + row_height/2, 
                                              text=str(i), 
                                              font=("Consolas", 11))
                    
                    # Draw empty notation
                    self.hash_canvas.create_text(160, y_pos + row_height/2, 
                                              text="(empty)", anchor="w", 
                                              font=("Segoe UI", 10, "italic"), 
                                              fill="#999999")
                    
                    row += 1
                    empty_shown += 1
            
            # Update stats
            total_height = y_start + row * row_height + 50
            
            # Draw hash table statistics
            stats_y = y_start + row * row_height + 20
            
            self.hash_canvas.create_text(50, stats_y, 
                                      text=f"Total buckets: {self.ht.size}", 
                                      anchor="w", font=("Segoe UI", 10))
            self.hash_canvas.create_text(50, stats_y + 20, 
                                      text=f"Non-empty buckets: {non_empty} ({non_empty/self.ht.size*100:.1f}%)", 
                                      anchor="w", font=("Segoe UI", 10))
            
            load_factor = len(self.values) / self.ht.size
            self.hash_canvas.create_text(350, stats_y, 
                                      text=f"Load factor: {load_factor:.2f}", 
                                      anchor="w", font=("Segoe UI", 10))
            self.hash_canvas.create_text(350, stats_y + 20, 
                                      text=f"Longest chain: {max(len(b) for b in self.ht.table)}", 
                                      anchor="w", font=("Segoe UI", 10))
            
            # Update the canvas scroll region
            self.hash_canvas.configure(scrollregion=(0, 0, table_width + 100, total_height))
        else:
            # No data - show empty state
            self.hash_canvas.create_text(50 + table_width/2, 150, 
                                      text="Hash table is empty. Add data to visualize.", 
                                      fill="#999999", font=("Segoe UI", 12, "italic"))
            self.hash_canvas.configure(scrollregion=(0, 0, table_width + 100, 200))

    def update_stats(self):
        """Update statistics display"""
        # Calculate BST height
        def get_height(node):
            if not node:
                return 0
            return max(get_height(node.left), get_height(node.right)) + 1
        
        height = get_height(self.bst.root)
        count = len(self.values)
        
        # Create more detailed stats
        stats_text = (f"Total Items: {count}\n"
                    f"BST Height: {height}\n"
                    f"BST Theoretical Min Height: {int(max(0, count).bit_length())}\n"
                    f"Hash Table Size: {self.ht.size}\n"
                    f"Hash Table Load Factor: {count/self.ht.size:.2f}")
        
        self.stats_label.config(text=stats_text)

    def reset_all(self):
        """Clear all data structures and visualizations"""
        # Ask for confirmation
        if self.values and messagebox.askyesno("Confirm Reset", 
                                            "Are you sure you want to clear all data?"):
            self.bst.clear()
            self.ht.clear()
            self.values.clear()
            self.update_stats()
            self.draw_visuals()
            
            # Reset the comparison charts
            for widget in self.comp_inner_frame.winfo_children():
                widget.destroy()
            
            self.comp_label = ttk.Label(self.comp_inner_frame, 
                                     text="Run a performance comparison to see results", 
                                     style="Heading.TLabel")
            self.comp_label.pack(pady=50)
            
            self.comp_canvas.configure(scrollregion=self.comp_canvas.bbox("all"))
            self.update_status("All data cleared")

    def show_search_simulation(self):
        """Open a new window to simulate lookups in BST and Hash Table"""
        if not self.values:
            messagebox.showwarning("No Data", "Insert values first to run a simulation.")
            return

        try:
            val = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer to search for.")
            return

        # Create simulation window with modern styling
        sim_window = tk.Toplevel(self.root)
        sim_window.title("Lookup Simulation")
        sim_window.geometry("1200x700")
        sim_window.configure(bg=self.colors["light_bg"])

        # --- NEW: use grid and center everything ---
        sim_window.columnconfigure(0, weight=1)
        sim_window.rowconfigure(1, weight=1)

        # Title
        ttk.Label(sim_window, text="Data Structure Lookup Simulation",
                  style="Title.TLabel") \
            .grid(row=0, column=0, pady=10)

        # Notebook (will expand)
        sim_notebook = ttk.Notebook(sim_window)
        sim_notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))

        # BST simulation tab
        bst_frame = ttk.Frame(sim_notebook, padding=10)
        sim_notebook.add(bst_frame, text="BST Lookup Simulation")

        # Hash Table simulation tab
        hash_frame = ttk.Frame(sim_notebook, padding=10)
        sim_notebook.add(hash_frame, text="Hash Table Lookup Simulation")
        
        # Setup BST visualization with scrollbars
        bst_canvas_frame = ttk.Frame(bst_frame)
        bst_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        bst_canvas = tk.Canvas(bst_canvas_frame, bg="white", highlightthickness=0)
        bst_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbars for BST canvas
        bst_y_scrollbar = ttk.Scrollbar(bst_canvas_frame, orient=tk.VERTICAL, command=bst_canvas.yview)
        bst_y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        bst_x_scrollbar = ttk.Scrollbar(bst_frame, orient=tk.HORIZONTAL, command=bst_canvas.xview)
        bst_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        bst_canvas.configure(yscrollcommand=bst_y_scrollbar.set, 
                          xscrollcommand=bst_x_scrollbar.set,
                          scrollregion=(0, 0, 800, 600))
        
        # Setup Hash Table visualization with scrollbars
        hash_canvas_frame = ttk.Frame(hash_frame)
        hash_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        hash_canvas = tk.Canvas(hash_canvas_frame, bg="white", highlightthickness=0)
        hash_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbars for Hash Table canvas
        hash_y_scrollbar = ttk.Scrollbar(hash_canvas_frame, orient=tk.VERTICAL, command=hash_canvas.yview)
        hash_y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        hash_x_scrollbar = ttk.Scrollbar(hash_frame, orient=tk.HORIZONTAL, command=hash_canvas.xview)
        hash_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        hash_canvas.configure(yscrollcommand=hash_y_scrollbar.set, 
                           xscrollcommand=hash_x_scrollbar.set,
                           scrollregion=(0, 0, 800, 600))
        
        # Controls frame
        control_frame = ttk.Frame(sim_window, padding=10, style="Card.TFrame")
        control_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        # Value being searched display
        ttk.Label(control_frame, text="Searching for value: ",
                  font=("Segoe UI", 11)) \
            .pack(side=tk.LEFT, padx=(10, 0))
        ttk.Label(control_frame, text=f"{val}",
                  font=("Segoe UI", 11, "bold"),
                  foreground=self.colors["primary"]) \
            .pack(side=tk.LEFT, padx=(0, 10))
        
        # Speed control with modern slider
        ttk.Label(control_frame, text="Animation Speed:", 
                font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(20, 5))
        
        speed_var = tk.IntVar(value=50)
        speed_scale = ttk.Scale(control_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                             variable=speed_var, length=200)
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Speed display label
        speed_label = ttk.Label(control_frame, text="Normal", width=8)
        speed_label.pack(side=tk.LEFT)
        
        # Update speed label when slider changes
        def update_speed_label(val):
            speed = int(float(val))
            if speed < 30:
                speed_label.config(text="Slow")
            elif speed > 70:
                speed_label.config(text="Fast")
            else:
                speed_label.config(text="Normal")
        
        speed_scale.config(command=update_speed_label)
        
        # Start button
        start_btn = ttk.Button(control_frame, text="Start Animation", style="Primary.TButton",
                            command=lambda: self.start_simulation(val, bst_canvas, hash_canvas, speed_var))
        start_btn.pack(side=tk.RIGHT, padx=10)
        
        # Draw initial state
        self.draw_bst_for_animation(bst_canvas)
        self.draw_hashtable_for_animation(hash_canvas)
        
        self.update_status(f"Opened simulation window for value: {val}")

    def animate_draw_tree(self, canvas, node, x, y, offset):
        """Draw the BST nodes for animation with tags for identification"""
        if not node:
            return
        
        # Draw current node with 3D effect
        canvas.create_oval(x-20, y-20, x+20, y+20, fill=self.colors["primary"], outline="", 
                        tags=f"node_{node.key}")
        canvas.create_arc(x-20, y-20, x+20, y+20, start=45, extent=180, 
                       fill="#3b77db", outline="", tags=f"arc_{node.key}")
        canvas.create_text(x, y, text=str(node.key), fill="white", font=("Segoe UI", 10), 
                        tags=f"text_{node.key}")
        
        # Draw edges to children
        if node.left:
            canvas.create_line(x, y+20, x-offset, y+80, fill="#666666", width=1.5, 
                            tags=f"edge_left_{node.key}")
            self.animate_draw_tree(canvas, node.left, x-offset, y+100, offset//2)
            
        if node.right:
            canvas.create_line(x, y+20, x+offset, y+80, fill="#666666", width=1.5, 
                            tags=f"edge_right_{node.key}")
            self.animate_draw_tree(canvas, node.right, x+offset, y+100, offset//2)

    def draw_bst_for_animation(self, canvas):
        """Draw the BST in its initial state for animation"""
        canvas.delete("all")
        canvas.create_text(400, 30, text="Binary Search Tree Lookup Simulation", 
                        font=("Segoe UI", 14, "bold"), fill=self.colors["text"])
        
        # Move legend below the title to prevent overlap
        legend_frame = canvas.create_rectangle(300, 60, 530, 100, fill="#f8f9fa", outline="#dadce0")
        canvas.create_oval(320, 70, 340, 90, fill=self.colors["primary"], outline="")
        canvas.create_text(360, 80, text="Node", anchor="w", font=("Segoe UI", 9))
        canvas.create_oval(400, 70, 420, 90, fill="#ff9800", outline="")
        canvas.create_text(440, 80, text="Current Node", anchor="w", font=("Segoe UI", 9))
        
        # Draw the tree
        tree_height = self.get_tree_height(self.bst.root)
        self.animate_draw_tree(canvas, self.bst.root, 400, 130, 200)
        
        # Update scroll region to fit the tree
        # Approximate the required size based on tree height
        width = max(800, 400 + 2**(tree_height-1) * 40)  # Width expands exponentially with height
        height = max(600, 100 + tree_height * 120)       # Height grows linearly with tree height
        canvas.configure(scrollregion=(0, 0, width, height))

    def get_tree_height(self, node):
        if not node:
            return 0
        return max(self.get_tree_height(node.left), self.get_tree_height(node.right)) + 1

    def draw_hashtable_for_animation(self, canvas):
        """Draw the hash table in its initial state for animation"""
        canvas.delete("all")
        canvas.create_text(400, 30, text="Hash Table Lookup Simulation", 
                        font=("Segoe UI", 14, "bold"), fill=self.colors["text"])
        
        # Add legend
        legend_frame = canvas.create_rectangle(550, 10, 780, 50, fill="#f8f9fa", outline="#dadce0")
        canvas.create_rectangle(570, 20, 590, 40, fill="#ffe0b2", outline="#ffcc80")
        canvas.create_text(610, 30, text="Current Bucket", anchor="w", font=("Segoe UI", 9))
        
        # Draw table background
        table_width = 700
        row_height = 40
        table_x = 50
        table_y = 100
        
        # Header
        canvas.create_rectangle(table_x, table_y, table_x + table_width, table_y + row_height,
                             fill=self.colors["primary"], outline="")
        canvas.create_text(table_x + table_width/2, table_y + row_height/2,
                        text="Hash Table Buckets", fill="white", font=("Segoe UI", 12, "bold"))
        
        # Show more buckets - increase from 15 to 30
        visible_buckets = min(30, self.ht.size)
        
        # Calculate total height including space for results
        total_height = table_y + (visible_buckets + 1) * row_height + 300
        
        for i in range(visible_buckets):
            y_pos = table_y + (i+1) * row_height
            bucket = self.ht.table[i]
            
            # Alternating colors
            bg_color = "#f0f0f0" if i % 2 == 0 else "#ffffff"
            
            # Draw row
            canvas.create_rectangle(table_x, y_pos, table_x + table_width, y_pos + row_height,
                                 fill=bg_color, outline="#dddddd", tags=f"bucket_{i}")
            
            # Draw index column
            canvas.create_rectangle(table_x, y_pos, table_x + 50, y_pos + row_height,
                                 fill="#e6e6e6", outline="#dddddd")
            canvas.create_text(table_x + 25, y_pos + row_height/2, text=str(i),
                            font=("Segoe UI", 10), tags=f"index_{i}")
            
            # Draw bucket contents - show more items (20 instead of 15)
            items_text = ", ".join(map(str, bucket[:20]))
            if len(bucket) > 20:
                items_text += f", ... (+{len(bucket) - 20} more)"
            
            if not bucket:
                items_text = "(empty)"
                
            canvas.create_text(table_x + 70, y_pos + row_height/2, text=items_text,
                            anchor="w", font=("Segoe UI", 10), tags=f"items_{i}")
        
        # Set a larger scroll region to ensure all content is visible
        canvas.configure(scrollregion=(0, 0, table_width + 200, total_height))
    
    def start_simulation(self, key, bst_canvas, hash_canvas, speed_var):
        """Start the animation for both BST and hash table lookups"""
        # Reset canvases to initial state
        self.draw_bst_for_animation(bst_canvas)
        self.draw_hashtable_for_animation(hash_canvas)
        
        # Get animation delay from speed control (invert so higher value = faster)
        delay = 1100 - speed_var.get() * 10
        
        # Schedule the animations
        self.root.after(500, lambda: self.animate_bst_search(key, bst_canvas, self.bst.root, delay))
        self.root.after(500, lambda: self.animate_hash_search(key, hash_canvas, delay))
    
    def animate_bst_search(self, key, canvas, node, delay, path=None):
        """Animate the BST search process"""
        if path is None:
            path = []
        
        if not node:
            # Search unsuccessful
            self.show_bst_result(canvas, key, False, path, delay)
            return
        
        # Highlight current node being examined
        canvas.itemconfig(f"node_{node.key}", fill="#ff9800")
        canvas.itemconfig(f"arc_{node.key}", fill="#f57c00")
        
        # Add step to search path
        path.append(node.key)
        
        # Create comparison text
        compare_text = f"Comparing {key} with {node.key}"
        text_id = canvas.create_text(400, 60, text=compare_text, 
                                  font=("Segoe UI", 11), fill=self.colors["text"])
        
        if key == node.key:
            # Found the key
            self.root.after(delay, lambda: canvas.itemconfig(f"node_{node.key}", fill=self.colors["secondary"]))
            self.root.after(delay, lambda: canvas.itemconfig(f"arc_{node.key}", fill="#2d9748"))
            self.root.after(delay, lambda: self.show_bst_result(canvas, key, True, path, delay))
        elif key < node.key:
            # Go left
            self.root.after(delay, lambda: canvas.delete(text_id))
            self.root.after(delay, lambda: canvas.itemconfig(f"node_{node.key}", fill=self.colors["primary"]))
            self.root.after(delay, lambda: canvas.itemconfig(f"arc_{node.key}", fill="#3b77db"))
            
            if node.left:
                self.root.after(delay, lambda: canvas.itemconfig(f"edge_left_{node.key}", 
                                                              fill="#ff9800", width=2.5))
            self.root.after(delay*2, lambda: self.animate_bst_search(key, canvas, node.left, delay, path))
        else:
            # Go right
            self.root.after(delay, lambda: canvas.delete(text_id))
            self.root.after(delay, lambda: canvas.itemconfig(f"node_{node.key}", fill=self.colors["primary"]))
            self.root.after(delay, lambda: canvas.itemconfig(f"arc_{node.key}", fill="#3b77db"))
            
            if node.right:
                self.root.after(delay, lambda: canvas.itemconfig(f"edge_right_{node.key}", 
                                                              fill="#ff9800", width=2.5))
            self.root.after(delay*2, lambda: self.animate_bst_search(key, canvas, node.right, delay, path))
    
    def show_bst_result(self, canvas, key, found, path, delay):
        """Show the result of the BST search"""
        result_text = f"{'Found' if found else 'Not found'} key {key}"
        path_text = f"Search path: {' → '.join(map(str, path))}"
        
        y_pos = 500
        result_color = self.colors["secondary"] if found else self.colors["warning"]
        
        # Create card for results
        canvas.create_rectangle(100, y_pos-40, 700, y_pos+50, 
                             fill="#f5f5f5", outline="#dadce0", width=1)
        canvas.create_text(400, y_pos-20, text=result_text, 
                        font=("Segoe UI", 12, "bold"), fill=result_color)
        canvas.create_text(400, y_pos+10, text=path_text, 
                        font=("Segoe UI", 10), fill=self.colors["text"])
        
        # Add complexity information
        canvas.create_text(400, y_pos+35, 
                        text=f"Time Complexity: O(log n) average, O(n) worst case", 
                        font=("Segoe UI", 9, "italic"), fill="#555555")
    
    def animate_hash_search(self, key, canvas, delay):
        """Animate the hash table search process"""
        # Calculate hash for the key
        hash_value = key % self.ht.size
        
        # Show hash calculation
        calc_text = f"Hash calculation: {key} % {self.ht.size} = {hash_value}"
        text_id = canvas.create_text(400, 60, text=calc_text, 
                                  font=("Segoe UI", 11), fill=self.colors["text"])
        
        # Check if key exists in the bucket
        bucket = self.ht.table[hash_value]
        found = key in bucket
        
        # If bucket is not in visible range (beyond bucket_29), add a note
        visible_buckets = min(30, self.ht.size)
        
        # Determine if the bucket is in visible range
        bucket_visible = hash_value < visible_buckets
        
        # If bucket is visible, animate highlighting it and scroll to it
        if bucket_visible:
            # Calculate y position of the bucket
            table_y = 100
            row_height = 40
            bucket_y = table_y + (hash_value + 1) * row_height
            
            # Scroll to make the bucket visible (after a short delay)
            self.root.after(delay, lambda: canvas.yview_moveto((bucket_y - 150) / canvas.bbox("all")[3]))
            
            # Highlight the bucket
            self.root.after(delay, lambda: canvas.itemconfig(f"bucket_{hash_value}", fill="#ffe0b2"))
            self.root.after(delay*2, lambda: canvas.itemconfig(f"index_{hash_value}", fill="#ff9800"))
        
            # Clear previous text after delay
            self.root.after(delay*3, lambda: canvas.delete(text_id))
            
            # Show searching in bucket text
            search_text = f"Searching in bucket {hash_value}..."
            search_id = canvas.create_text(400, 60, text=search_text, 
                                        font=("Segoe UI", 11), fill=self.colors["text"])
            
            # Highlight found item or show not found
            if found:
                bucket_text = canvas.itemcget(f"items_{hash_value}", "text")
                
                # Update the text to highlight the found item
                highlighted_text = bucket_text.replace(
                    str(key), f"[{key}]"
                )
                self.root.after(delay*4, lambda: canvas.itemconfig(f"items_{hash_value}", 
                                                                text=highlighted_text))
                
            self.root.after(delay*5, lambda: canvas.delete(search_id))
        else:
            # If bucket is not visible, display a message
            self.root.after(delay*2, lambda: canvas.delete(text_id))
            message_text = f"Bucket {hash_value} is outside the visible range (0-{visible_buckets-1})"
            message_id = canvas.create_text(400, 60, text=message_text, 
                                         font=("Segoe UI", 11), fill=self.colors["warning"])
            self.root.after(delay*4, lambda: canvas.delete(message_id))
        
        # Show final result
        self.root.after(delay*6, lambda: self.show_hash_result(canvas, key, hash_value, found, bucket, bucket_visible))
    
    def show_hash_result(self, canvas, key, hash_value, found, bucket, bucket_visible=True):
        """Show the result of the hash table search"""
        result_text = f"{'Found' if found else 'Not found'} key {key} in bucket {hash_value}"
        
        # Format bucket contents to prevent overly long text
        if len(bucket) > 10:
            bucket_display = str(bucket[:10])[:-1] + ", ... ]"  # Show first 10 items with ellipsis
        else:
            bucket_display = bucket
            
        bucket_text = f"Bucket {hash_value} contents: {bucket_display}"
        
        if not bucket_visible:
            bucket_text += f"\n(This bucket is outside the visible range shown in the animation)"
        
        y_pos = 500
        result_color = self.colors["secondary"] if found else self.colors["warning"]
        
        # Create card for results
        canvas.create_rectangle(50, y_pos-40, 750, y_pos+80, 
                             fill="#f5f5f5", outline="#dadce0", width=1)
        canvas.create_text(400, y_pos-20, text=result_text, 
                        font=("Segoe UI", 12, "bold"), fill=result_color)
        canvas.create_text(400, y_pos+20, text=bucket_text, 
                        font=("Segoe UI", 10), fill=self.colors["text"], width=650)
        
        # Add complexity information
        canvas.create_text(400, y_pos+60, 
                        text=f"Time Complexity: O(1) average, O(n) worst case", 
                        font=("Segoe UI", 9, "italic"), fill="#555555")
        
    def insert_large_dataset(self):
        """Insert 10,000 random integers for large-scale performance testing"""
        # Show a confirmation dialog since this might take a moment
        confirm = messagebox.askyesno(
            "Add Large Dataset", 
            "This will add 10,000 random values.\nThis operation may take a few moments. Continue?"
        )
        
        if not confirm:
            return
        
        self.update_status("Adding 10,000 random values...")
        
        # Show a progress indicator
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Adding Data")
        progress_window.geometry("400x150")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Style the progress window
        progress_frame = ttk.Frame(progress_window, padding=20)
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(progress_frame, text="Adding 10,000 random values", 
                style="Heading.TLabel").pack(pady=(0, 10))
        
        # Progress bar and percentage
        progress_var = tk.DoubleVar()
        progress = ttk.Progressbar(progress_frame, orient="horizontal", 
                                length=350, mode="determinate", variable=progress_var)
        progress.pack(pady=10, fill=tk.X)
        
        percent_label = ttk.Label(progress_frame, text="0%")
        percent_label.pack()
        
        # Cancel button
        cancel_var = tk.BooleanVar(value=False)
        cancel_btn = ttk.Button(progress_frame, text="Cancel", 
                             command=lambda: cancel_var.set(True))
        cancel_btn.pack(pady=10)
        
        # Update the window to show progress
        progress_window.update()
        
        # Add the random values in batches
        batch_size = 500  # Process in batches to keep UI responsive
        total_items = 10000
        
        added_count = 0
        canceled = False
        
        for i in range(0, total_items, batch_size):
            # Check if canceled
            if cancel_var.get():
                canceled = True
                break
                
            # Process a batch of items
            for _ in range(min(batch_size, total_items - i)):
                val = random.randint(1, 50000)  # Larger range to reduce duplicates
                self.values.append(val)
                self.bst.insert(val)
                self.ht.insert(val)
                added_count += 1
            
            # Update progress
            progress_var.set(added_count / total_items * 100)
            percent_label.config(text=f"{added_count / total_items * 100:.1f}%")
            
            # Update progress window
            progress_window.update()
        
        # Close progress window
        progress_window.destroy()
        
        # Update the UI
        self.update_stats()
        self.draw_visuals()
        
        # Show completion message
        if canceled:
            messagebox.showinfo("Operation Canceled", 
                             f"Operation canceled. Added {added_count} random values.")
            self.update_status(f"Added {added_count} random values (canceled)")
        else:
            messagebox.showinfo("Data Added", 
                             f"Successfully added 10,000 random values.\nTotal items: {len(self.values)}")
            self.update_status(f"Added 10,000 random values. Total items: {len(self.values)}")
    def balance_tree(self):
        """Balance the Binary Search Tree."""
        self.bst.balance()
        self.draw_visuals()
        self.update_status("Balanced the Binary Search Tree")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()