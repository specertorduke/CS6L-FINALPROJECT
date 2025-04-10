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

# GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("BST vs Hash Table Lookup")
        self.bst = BST()
        self.ht = HashTable()
        self.values = []

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="Value:").grid(row=0, column=0)
        self.entry = tk.Entry(frame)
        self.entry.grid(row=0, column=1)

        tk.Button(frame, text="Insert", command=self.insert_value).grid(row=0, column=2)
        tk.Button(frame, text="Search", command=self.search_value).grid(row=0, column=3)
        tk.Button(frame, text="Insert Random (50)", command=self.insert_random).grid(row=1, column=1)
        tk.Button(frame, text="Compare Lookup Times", command=self.compare_times).grid(row=1, column=2)

        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack()

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
        self.draw_tree(self.bst.root, 400, 20, 180)
        self.draw_hashtable(500, 250)

    def draw_tree(self, node, x, y, offset):
        if not node:
            return
        if node.left:
            self.canvas.create_line(x, y, x - offset, y + 50)
            self.draw_tree(node.left, x - offset, y + 50, offset // 2)
        if node.right:
            self.canvas.create_line(x, y, x + offset, y + 50)
            self.draw_tree(node.right, x + offset, y + 50, offset // 2)
        self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightblue")
        self.canvas.create_text(x, y, text=str(node.key))

    def draw_hashtable(self, x, y):
        for i in range(10):
            bucket = self.ht.table[i]
            self.canvas.create_rectangle(x, y + i*25, x + 200, y + 25 + i*25, outline="black")
            text = f"{i}: " + ", ".join(map(str, bucket[:5]))
            self.canvas.create_text(x + 100, y + 12 + i*25, text=text, anchor="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
