import tkinter as tk
from tkinter import messagebox
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
        self.root.title("BST vs Hash Table Lookup")
        self.root.geometry("1200x700")
        self.bst = BST()
        self.ht = HashTable()
        self.values = []

        self.setup_ui()

    def setup_ui(self):
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame = tk.Frame(self.root, padx=10, pady=10, bg="lightsteelblue") # Set background color for control frame
        control_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(control_frame, text="Value:", bg="lightgreen", fg="darkblue", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.entry = tk.Entry(control_frame)
        self.entry.pack(side=tk.LEFT)

        tk.Button(control_frame, text="Insert", command=self.insert_value, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Search", command=self.search_value, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Insert Random (50)", command=self.insert_random, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Compare Lookup Times", command=self.compare_times, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Clear All", command=self.reset_all, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)


        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="aliceblue") # Set background color for canvas
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 1200, 2000))

    def insert_value(self):
        try:
            val = int(self.entry.get())
            self.values.append(val)
            self.bst.insert(val)
            self.ht.insert(val)
            self.entry.delete(0, tk.END)
            self.draw_visuals()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer.")

    def insert_random(self):
        for _ in range(50):
            val = random.randint(1, 1000)
            self.values.append(val)
            self.bst.insert(val)
            self.ht.insert(val)
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

        bst_times = []
        ht_times = []
        search_vals = random.sample(self.values, min(30, len(self.values)))
        for val in search_vals:
            t1 = time.perf_counter()
            self.bst.search(val)
            bst_times.append(time.perf_counter() - t1)

            t2 = time.perf_counter()
            self.ht.search(val)
            ht_times.append(time.perf_counter() - t2)

        fig, ax = plt.subplots()
        ax.plot(bst_times, label='BST Lookup Times', marker='o')
        ax.plot(ht_times, label='Hash Table Lookup Times', marker='x')
        ax.set_xlabel('Search #')
        ax.set_ylabel('Time (s)')
        ax.set_title('BST vs Hash Table Lookup Performance')
        ax.legend()

        plt.show()

    def draw_visuals(self):
        self.canvas.delete("all")
        self.draw_tree(self.bst.root, 300, 30, 100)
        self.draw_hashtable(700, 20)

    def draw_tree(self, node, x, y, offset):
        if not node:
            return
        if node.left:
            self.canvas.create_line(x, y, x - offset, y + 60, fill="gray")
            self.draw_tree(node.left, x - offset, y + 60, offset // 1.5)
        if node.right:
            self.canvas.create_line(x, y, x + offset, y + 60, fill="gray")
            self.draw_tree(node.right, x + offset, y + 60, offset // 1.5)
        self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightblue")
        self.canvas.create_text(x, y, text=str(node.key))

    def draw_hashtable(self, x, y):
        for i in range(10):
            bucket = self.ht.table[i]
            self.canvas.create_rectangle(x, y + i*30, x + 250, y + 30 + i*30, outline="black", fill="#f0f0f0")
            text = f"{i}: " + ", ".join(map(str, bucket[:5]))
            self.canvas.create_text(x + 125, y + 15 + i*30, text=text, anchor="center", font=("Courier", 10))

    def reset_all(self):
        self.bst.clear()
        self.ht.clear()
        self.values.clear()
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()