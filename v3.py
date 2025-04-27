import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("BST vs Hash Table Comparison")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f5f5f5")  # Light gray background
        self.bst = BST()
        self.ht = HashTable()
        self.values = []

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 10), background='#4a86e8', foreground='white')
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        
        self.setup_ui()

    def setup_ui(self):
        # Main layout with two frames
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Controls and input
        control_panel = ttk.Frame(main_frame, padding="10", relief="ridge", borderwidth=1)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Right side - Visualization
        visualization_frame = ttk.Frame(main_frame, padding="5")
        visualization_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Control panel elements
        ttk.Label(control_panel, text="Data Structure Comparison", 
                 font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))
        
        # Input section
        input_frame = ttk.Frame(control_panel)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Value:").pack(side=tk.LEFT, padx=(0, 5))
        self.entry = ttk.Entry(input_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Button section
        button_frame = ttk.Frame(control_panel)
        button_frame.pack(fill=tk.X, pady=5)
        
        insert_btn = ttk.Button(button_frame, text="Insert", command=self.insert_value)
        insert_btn.pack(fill=tk.X, pady=2)
        
        search_btn = ttk.Button(button_frame, text="Search", command=self.search_value)
        search_btn.pack(fill=tk.X, pady=2)
        
        # Action section
        action_frame = ttk.Frame(control_panel)
        action_frame.pack(fill=tk.X, pady=10)
        
        sim_btn = ttk.Button(action_frame, text="Simulate Lookup", command=self.show_search_simulation)
        sim_btn.pack(fill=tk.X, pady=2)

        random_btn = ttk.Button(action_frame, text="Insert Random (50)", 
                            command=self.insert_random)
        random_btn.pack(fill=tk.X, pady=2)
        
        # Replace the single comparison button with dropdown + button
        compare_frame = ttk.Frame(action_frame)
        compare_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(compare_frame, text="Search Sample:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_count = tk.StringVar(value="100")
        search_dropdown = ttk.Combobox(compare_frame, width=6, textvariable=self.search_count)
        search_dropdown['values'] = ('30', '100', '500', '1000', '5000', '10,000')
        search_dropdown.pack(side=tk.LEFT, padx=5)
        
        # --- New Test Type Selector ---
        ttk.Label(compare_frame, text="Test Type:").pack(side=tk.LEFT, padx=(0, 5))
        self.test_type = tk.StringVar(value="Random")
        test_type_dropdown = ttk.Combobox(compare_frame, width=10, textvariable=self.test_type)
        test_type_dropdown['values'] = ("Random", "Best-case", "Worst-case")
        test_type_dropdown.pack(side=tk.LEFT, padx=5)
        
        compare_btn = ttk.Button(action_frame, text="Compare Lookup Times", 
                                command=self.compare_times)
        compare_btn.pack(fill=tk.X, pady=2)
        
        reset_btn = ttk.Button(action_frame, text="Clear All", command=self.reset_all)
        reset_btn.pack(fill=tk.X, pady=10)
        
        # Stats section
        stats_frame = ttk.LabelFrame(control_panel, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_label = ttk.Label(stats_frame, text="Items: 0\nBST Height: 0")
        self.stats_label.pack(fill=tk.X)
        
        # Visualization area
        canvas_container = ttk.Frame(visualization_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        # Tabs for different visualizations
        notebook = ttk.Notebook(canvas_container)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # BST tab
        bst_frame = ttk.Frame(notebook)
        notebook.add(bst_frame, text="Binary Search Tree")
        
        # Hash Table tab
        hash_frame = ttk.Frame(notebook)
        notebook.add(hash_frame, text="Hash Table")
        
        # Create scrollable canvas for Hash Table
        hash_canvas_frame = ttk.Frame(hash_frame)
        hash_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.hash_canvas = tk.Canvas(hash_canvas_frame, bg="#ffffff", highlightthickness=0)
        self.hash_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Hash table scrollbars
        hash_y_scrollbar = ttk.Scrollbar(hash_canvas_frame, orient=tk.VERTICAL, command=self.hash_canvas.yview)
        hash_y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        hash_x_scrollbar = ttk.Scrollbar(hash_frame, orient=tk.HORIZONTAL, command=self.hash_canvas.xview)
        hash_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.hash_canvas.configure(yscrollcommand=hash_y_scrollbar.set, 
                                xscrollcommand=hash_x_scrollbar.set,
                                scrollregion=(0, 0, 600, 1000))
                
        # Comparison tab with scrolling
        comp_frame = ttk.Frame(notebook)
        notebook.add(comp_frame, text="Performance Comparison")
        
        # Create scrollable canvas for comparison charts
        comp_canvas_frame = ttk.Frame(comp_frame)
        comp_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.comp_canvas = tk.Canvas(comp_canvas_frame, bg="#ffffff", highlightthickness=0)
        self.comp_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars for comparison charts
        comp_y_scrollbar = ttk.Scrollbar(comp_canvas_frame, orient=tk.VERTICAL, command=self.comp_canvas.yview)
        comp_y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        comp_x_scrollbar = ttk.Scrollbar(comp_frame, orient=tk.HORIZONTAL, command=self.comp_canvas.xview)
        comp_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.comp_canvas.configure(yscrollcommand=comp_y_scrollbar.set, 
                                xscrollcommand=comp_x_scrollbar.set)
        
        # Create a frame inside the canvas for charts
        self.comp_inner_frame = ttk.Frame(self.comp_canvas)
        self.comp_canvas.create_window((0, 0), window=self.comp_inner_frame, anchor='nw')
        
        # Placeholder message
        self.comp_label = ttk.Label(self.comp_inner_frame, text="Run comparison to see results", 
                                font=("Segoe UI", 12))
        self.comp_label.pack(pady=20)
        
        # Bind frame size changes to update scroll region
        self.comp_inner_frame.bind('<Configure>', lambda e: 
                                self.comp_canvas.configure(scrollregion=self.comp_canvas.bbox("all")))
        
        # Create scrollable canvas for BST
        canvas_frame = ttk.Frame(bst_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars for BST
        y_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = ttk.Scrollbar(bst_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas.configure(yscrollcommand=y_scrollbar.set, 
                            xscrollcommand=x_scrollbar.set,
                            scrollregion=(0, 0, 1200, 2000))
        
         # Instead of creating self.fig and self.ax here, just create the comp_inner_frame
        self.comp_inner_frame = ttk.Frame(self.comp_canvas)
        self.comp_canvas.create_window((0, 0), window=self.comp_inner_frame, anchor='nw')
        
        # Placeholder message
        self.comp_label = ttk.Label(self.comp_inner_frame, text="Run comparison to see results", 
                                font=("Segoe UI", 12))
        self.comp_label.pack(pady=20)
        
        # Bind frame size changes to update scroll region
        self.comp_inner_frame.bind('<Configure>', lambda e: 
                                self.comp_canvas.configure(scrollregion=self.comp_canvas.bbox("all")))
        

    def insert_value(self):
        try:
            val = int(self.entry.get())
            self.values.append(val)
            self.bst.insert(val)
            self.ht.insert(val)
            self.entry.delete(0, tk.END)
            self.update_stats()
            self.draw_visuals()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer.")

    def insert_random(self):
        for _ in range(50):
            val = random.randint(1, 1000)
            self.values.append(val)
            self.bst.insert(val)
            self.ht.insert(val)
        self.update_stats()
        self.draw_visuals()

    def search_value(self):
        try:
            val = int(self.entry.get())
            bst_start = time.perf_counter()
            bst_result = self.bst.search(val)
            bst_time = time.perf_counter() - bst_start

            ht_start = time.perf_counter()
            ht_result = self.ht.search(val)
            ht_time = time.perf_counter() - ht_start

            result = f"BST: {'Found' if bst_result else 'Not Found'} in {bst_time:.6f}s\n"
            result += f"HashTable: {'Found' if ht_result else 'Not Found'} in {ht_time:.6f}s"
            messagebox.showinfo("Search Result", result)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer.")

    def compare_times(self):
        if not self.values:
            messagebox.showwarning("No Data", "Insert values first to compare.")
            return
        
        # Clear previous charts
        for widget in self.comp_inner_frame.winfo_children():
            widget.destroy()
        
        # Main title for the comparison tab
        ttk.Label(self.comp_inner_frame, text="Performance Comparison Across Different Sample Sizes", 
                  font=("Segoe UI", 14, "bold")).pack(pady=(10, 5))
        
        # Processing indicator
        process_label = ttk.Label(self.comp_inner_frame, text="Processing... Please wait")
        process_label.pack(pady=5)
        self.root.update()
        
        # Define the sample sizes to test
        sample_sizes = [30, 100, 500, 1000, 5000]
        available_samples = [size for size in sample_sizes if size <= len(self.values)]
        if not available_samples:
            messagebox.showinfo("Info", f"Not enough values. Using all {len(self.values)} available values.")
            available_samples = [len(self.values)]
        
        # Get the test type selection from the new combobox
        test_type = self.test_type.get()
        all_stats = []
        
        for sample_size in available_samples:
            bst_times = []
            ht_times = []
            
            # Select lookup values based on test type
            if test_type == "Random":
                search_vals = random.sample(self.values, min(sample_size, len(self.values)))
            elif test_type == "Best-case":
                # Best-case: Search for the first inserted value (if available)
                search_vals = [self.values[0]] * sample_size if self.values else [0] * sample_size
            elif test_type == "Worst-case":
                # Worst-case: Searching for a value known not to exist (e.g. -1)
                search_vals = [-1] * sample_size
            else:
                search_vals = random.sample(self.values, min(sample_size, len(self.values)))
            
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
            
            # Create section header with statistics for this sample
            section_frame = ttk.Frame(self.comp_inner_frame)
            section_frame.pack(fill=tk.X, pady=(20, 5))
            ttk.Label(section_frame, 
                      text=f"Sample Size: {sample_size} Searches", 
                      font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT, padx=20)
            stats_text = (
                f"BST Avg: {bst_avg:.8f}s | Hash Table Avg: {ht_avg:.8f}s | "
                f"Speed Difference: {speedup:.1f}x"
            )
            ttk.Label(section_frame, text=stats_text, font=("Consolas", 9)).pack(side=tk.RIGHT, padx=20)
            
            # Create line plot for the current sample size
            line_frame = ttk.Frame(self.comp_inner_frame)
            line_frame.pack(fill=tk.X, expand=True, padx=20, pady=5)
            
            fig = plt.Figure(figsize=(10, 4), dpi=100)
            ax = fig.add_subplot(111)
            chart = FigureCanvasTkAgg(fig, line_frame)
            chart.get_tk_widget().pack(fill=tk.BOTH)
            
            ax.plot(bst_times, label='BST Lookup Times', marker='o', color='#3366cc')
            ax.plot(ht_times, label='Hash Table Lookup Times', marker='x', color='#dc3912')
            ax.set_xlabel('Search #')
            ax.set_ylabel('Time (s)')
            ax.set_title(f'Lookup Performance ({sample_size} searches) - {test_type} test')
            ax.legend()
            ax.grid(True)
            fig.tight_layout()
            
            # Add a visual separator
            ttk.Separator(self.comp_inner_frame, orient='horizontal').pack(fill=tk.X, padx=20, pady=10)
        
        process_label.destroy()
        self.comp_canvas.configure(scrollregion=self.comp_canvas.bbox("all"))

    def draw_visuals(self):
        self.canvas.delete("all")
        self.hash_canvas.delete("all")
        self.draw_tree(self.bst.root, 600, 30, 250)
        self.draw_hashtable()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_tree(self, node, x, y, offset):
        if not node:
            return
        if node.left:
            self.canvas.create_line(x, y, x - offset, y + 60, fill="#666666", width=1.5)
            self.draw_tree(node.left, x - offset, y + 60, offset // 1.5)
        if node.right:
            self.canvas.create_line(x, y, x + offset, y + 60, fill="#666666", width=1.5)
            self.draw_tree(node.right, x + offset, y + 60, offset // 1.5)
        self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="#4a86e8", outline="")
        self.canvas.create_text(x, y, text=str(node.key), fill="white", font=("Segoe UI", 9))

    def draw_hashtable(self):
        self.hash_canvas.delete("all")
        table_width = 500
        row_height = 35
        
        # Draw table header
        self.hash_canvas.create_rectangle(50, 20, 50 + table_width, 20 + row_height, 
                                        fill="#4a86e8", outline="")
        self.hash_canvas.create_text(50 + table_width/2, 20 + row_height/2, 
                                    text="Hash Table", fill="white", 
                                    font=("Segoe UI", 12, "bold"))
        
        # Show more buckets for better visualization
        visible_buckets = 50  # Increased from 20 to show more buckets
        
        for i in range(visible_buckets):
            y_pos = 20 + (i+1) * row_height
            bucket = self.ht.table[i]
            
            # Alternating row colors
            bg_color = "#f0f0f0" if i % 2 == 0 else "#ffffff"
            
            # Draw row background
            self.hash_canvas.create_rectangle(50, y_pos, 50 + table_width, y_pos + row_height, 
                                            fill=bg_color, outline="#dddddd")
            
            # Draw index
            self.hash_canvas.create_rectangle(50, y_pos, 100, y_pos + row_height, 
                                            fill="#e6e6e6", outline="#dddddd")
            self.hash_canvas.create_text(75, y_pos + row_height/2, text=str(i), 
                                        font=("Segoe UI", 10))
            
            # Draw bucket contents
            items_text = ", ".join(map(str, bucket[:8]))
            if len(bucket) > 8:
                items_text += f", ... (+{len(bucket) - 8} more)"
            
            self.hash_canvas.create_text(110, y_pos + row_height/2, text=items_text, 
                                        anchor="w", font=("Segoe UI", 10))
        
        # Update the canvas scroll region to fit all content
        total_height = 20 + (visible_buckets + 1) * row_height
        self.hash_canvas.configure(scrollregion=(0, 0, table_width + 100, total_height))

    def update_stats(self):
        # Calculate BST height
        def get_height(node):
            if not node:
                return 0
            return max(get_height(node.left), get_height(node.right)) + 1
        
        height = get_height(self.bst.root)
        
        # Count total items
        count = len(self.values)
        
        # Update stats
        self.stats_label.config(text=f"Items: {count}\nBST Height: {height}")

    def reset_all(self):
        self.bst.clear()
        self.ht.clear()
        self.values.clear()
        self.update_stats()
        self.draw_visuals()
        
        # Reset the comparison charts
        for widget in self.comp_inner_frame.winfo_children():
            widget.destroy()
        
        self.comp_label = ttk.Label(self.comp_inner_frame, text="Run comparison to see results", 
                                font=("Segoe UI", 12))
        self.comp_label.pack(pady=20)
        self.comp_canvas.configure(scrollregion=self.comp_canvas.bbox("all"))
    
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
            
        # Create simulation window
        sim_window = tk.Toplevel(self.root)
        sim_window.title("Lookup Simulation")
        sim_window.geometry("1200x700")  # Increased from 1000x600
        
        # Create tabs for BST and Hash Table simulations
        sim_notebook = ttk.Notebook(sim_window)
        sim_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
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
        control_frame = ttk.Frame(sim_window, padding=10)
        control_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Speed control
        ttk.Label(control_frame, text="Animation Speed:").pack(side=tk.LEFT)
        speed_var = tk.IntVar(value=50)
        speed_scale = ttk.Scale(control_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                            variable=speed_var, length=200)
        speed_scale.pack(side=tk.LEFT, padx=10)
        
        # Start button
        start_btn = ttk.Button(control_frame, text="Start Animation", 
                            command=lambda: self.start_simulation(val, bst_canvas, hash_canvas, speed_var))
        start_btn.pack(side=tk.RIGHT, padx=10)
        
        # Draw initial state
        self.draw_bst_for_animation(bst_canvas)
        self.draw_hashtable_for_animation(hash_canvas)

    def animate_draw_tree(self, canvas, node, x, y, offset):
        """Draw the BST nodes for animation with tags for identification"""
        if not node:
            return
        
        # Draw current node
        canvas.create_oval(x-20, y-20, x+20, y+20, fill="#4a86e8", outline="", 
                        tags=f"node_{node.key}")
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
                        font=("Segoe UI", 14, "bold"))
        
        # Draw the tree
        tree_height = self.get_tree_height(self.bst.root)
        self.animate_draw_tree(canvas, self.bst.root, 400, 100, 200)
        
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
                        font=("Segoe UI", 14, "bold"))
        
        # Draw table background
        table_width = 700
        row_height = 40
        table_x = 50
        table_y = 100
        
        # Header
        canvas.create_rectangle(table_x, table_y, table_x + table_width, table_y + row_height,
                            fill="#4a86e8", outline="")
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
        
        # Add step to search path
        path.append(node.key)
        
        # Create comparison text
        compare_text = f"Comparing {key} with {node.key}"
        text_id = canvas.create_text(400, 60, text=compare_text, font=("Segoe UI", 11), fill="#333333")
        
        if key == node.key:
            # Found the key
            self.root.after(delay, lambda: canvas.itemconfig(f"node_{node.key}", fill="#4caf50"))
            self.root.after(delay, lambda: self.show_bst_result(canvas, key, True, path, delay))
        elif key < node.key:
            # Go left
            self.root.after(delay, lambda: canvas.delete(text_id))
            self.root.after(delay, lambda: canvas.itemconfig(f"node_{node.key}", fill="#2196f3"))
            if node.left:
                self.root.after(delay, lambda: canvas.itemconfig(f"edge_left_{node.key}", fill="#ff9800", width=2.5))
            self.root.after(delay*2, lambda: self.animate_bst_search(key, canvas, node.left, delay, path))
        else:
            # Go right
            self.root.after(delay, lambda: canvas.delete(text_id))
            self.root.after(delay, lambda: canvas.itemconfig(f"node_{node.key}", fill="#2196f3"))
            if node.right:
                self.root.after(delay, lambda: canvas.itemconfig(f"edge_right_{node.key}", fill="#ff9800", width=2.5))
            self.root.after(delay*2, lambda: self.animate_bst_search(key, canvas, node.right, delay, path))
    
    def show_bst_result(self, canvas, key, found, path, delay):
        """Show the result of the BST search"""
        result_text = f"{'Found' if found else 'Not found'} key {key}"
        path_text = f"Search path: {' → '.join(map(str, path))}"
        
        y_pos = 500
        result_color = "#4caf50" if found else "#f44336"
        
        canvas.create_rectangle(100, y_pos-30, 700, y_pos+50, fill="#f5f5f5", outline="#dddddd")
        canvas.create_text(400, y_pos, text=result_text, font=("Segoe UI", 12, "bold"), fill=result_color)
        canvas.create_text(400, y_pos+20, text=path_text, font=("Segoe UI", 10), fill="#333333")
    
    def animate_hash_search(self, key, canvas, delay):
        """Animate the hash table search process"""
        # Calculate hash for the key
        hash_value = key % self.ht.size
        
        # Show hash calculation
        calc_text = f"Hash calculation: {key} % {self.ht.size} = {hash_value}"
        text_id = canvas.create_text(400, 60, text=calc_text, font=("Segoe UI", 11), fill="#333333")
        
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
            search_id = canvas.create_text(400, 60, text=search_text, font=("Segoe UI", 11), fill="#333333")
            
            # Highlight found item or show not found
            if found:
                bucket_text = canvas.itemcget(f"items_{hash_value}", "text")
                
                # Update the text to highlight the found item
                highlighted_text = bucket_text.replace(
                    str(key), f"[{key}]"
                )
                self.root.after(delay*4, lambda: canvas.itemconfig(f"items_{hash_value}", text=highlighted_text))
                
            self.root.after(delay*5, lambda: canvas.delete(search_id))
        else:
            # If bucket is not visible, display a message
            self.root.after(delay*2, lambda: canvas.delete(text_id))
            message_text = f"Bucket {hash_value} is outside the visible range (0-{visible_buckets-1})"
            message_id = canvas.create_text(400, 60, text=message_text, 
                                        font=("Segoe UI", 11), fill="#d32f2f")
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
        result_color = "#4caf50" if found else "#f44336"
        
        # Create result box with more space
        canvas.create_rectangle(50, y_pos-40, 750, y_pos+80, 
                            fill="#f5f5f5", outline="#dddddd")
        canvas.create_text(400, y_pos-15, text=result_text, 
                        font=("Segoe UI", 12, "bold"), fill=result_color)
        canvas.create_text(400, y_pos+20, text=bucket_text, 
                        font=("Segoe UI", 10), fill="#333333", width=650)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()