import os
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar, filedialog, Listbox, OptionMenu, MULTIPLE, END, DISABLED, NORMAL
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler
from concurrent.futures import ThreadPoolExecutor

# Helper Functions
def crawl_images(keyword, save_dir, engine, num_images, filters, status_widget):
    """Crawls images for a specific keyword using the chosen engine."""
    engine_mapping = {
        'google': GoogleImageCrawler,
        'bing': BingImageCrawler,
        'baidu': BaiduImageCrawler
    }
    crawler_class = engine_mapping.get(engine.lower())
    
    if not crawler_class:
        thread_safe_update_status(status_widget, f"Invalid engine: {engine}. Skipping...\n")
        return

    try:
        thread_safe_update_status(status_widget, f"Starting crawl for keyword: {keyword} using {engine.capitalize()}...\n")
        crawler = crawler_class(storage={'root_dir': save_dir})
        crawler.crawl(keyword=keyword, max_num=num_images, filters=filters)
        thread_safe_update_status(status_widget, f"Finished crawling for: {keyword} using {engine.capitalize()}.\n")
    except Exception as e:
        thread_safe_update_status(status_widget, f"Error for keyword {keyword} with {engine.capitalize()}: {e}\n")

def crawl_images_with_progress(keyword, save_dir, engine, num_images, filters, status_widget, total_tasks, task_var):
    """Crawls images and updates progress bar."""
    crawl_images(keyword, save_dir, engine, num_images, filters, status_widget)
    task_var.set(task_var.get() + 1)  # Update completed task count
    progress = (task_var.get() / total_tasks) * 100
    progress_var.set(progress)  # Update progress bar

def update_status(widget, message):
    """Appends a message to the status box."""
    widget.configure(state=NORMAL)
    widget.insert(END, message)
    widget.configure(state=DISABLED)
    widget.yview(END)

def thread_safe_update_status(widget, message):
    """Safely updates the status box from threads."""
    widget.after(0, lambda: update_status(widget, message))

def validate_inputs(search_terms, save_directory, selected_engines, num_images, threads):
    """Validates user inputs before starting the crawl."""
    if not search_terms:
        return "No search terms provided."
    if not save_directory or not os.path.exists(save_directory):
        return "Invalid or non-existent save directory."
    if not selected_engines:
        return "No search engine selected."
    if num_images <= 0:
        return "Number of images must be greater than 0."
    if threads <= 0:
        return "Number of threads must be greater than 0."
    return None

import threading  # Import threading module

def start_crawling():
    """Starts the image crawling process in a background thread."""
    def background_crawling():
        """The actual crawling logic that runs in a separate thread."""
        search_terms = [term.strip() for term in search_terms_var.get().split(',') if term.strip()]
        save_directory = directory_var.get()
        selected_engines = [engine_listbox.get(i) for i in engine_listbox.curselection()]
        num_images = num_images_var.get()
        threads = threads_var.get()

        validation_error = validate_inputs(search_terms, save_directory, selected_engines, num_images, threads)
        if validation_error:
            thread_safe_update_status(status_box, validation_error + "\n")
            return

        filters = {}
        if size_filter_var.get():
            filters['size'] = size_filter_var.get()
        if type_filter_var.get():
            filters['type'] = type_filter_var.get()

        total_tasks = len(search_terms) * len(selected_engines)
        progress_var.set(0)
        task_var = IntVar(value=0)

        def crawl_task(keyword, engine):
            crawl_images_with_progress(
                keyword, save_directory, engine.lower(), num_images, filters, status_box, total_tasks, task_var
            )

        thread_safe_update_status(status_box, f"Starting crawling with {threads} threads...\n")
        try:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                for engine in selected_engines:
                    for keyword in search_terms:
                        futures.append(executor.submit(crawl_task, keyword, engine))
                for future in futures:
                    future.result()  # Ensure all tasks complete
        except Exception as e:
            thread_safe_update_status(status_box, f"Error during crawling: {e}\n")
        finally:
            thread_safe_update_status(status_box, "Crawling completed.\n")

    # Run crawling logic in a separate thread
    crawl_thread = threading.Thread(target=background_crawling)
    crawl_thread.start()



def export_log():
    """Exports the status log to a text file."""
    log_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if log_file:
        with open(log_file, 'w') as file:
            file.write(status_box.get("1.0", END))

def create_gui():
    """Creates the GUI layout."""
    Label(root, text="Search Terms (comma-separated):").grid(row=0, column=0, sticky='w', padx=10, pady=5)
    Entry(root, textvariable=search_terms_var, width=40).grid(row=0, column=1, padx=10, pady=5)

    Label(root, text="Save Directory:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
    Entry(root, textvariable=directory_var, width=30).grid(row=1, column=1, padx=10, pady=5)
    Button(root, text="Browse", command=lambda: directory_var.set(filedialog.askdirectory())).grid(row=1, column=2, padx=5, pady=5)

    Label(root, text="Search Engines (select one or more):").grid(row=2, column=0, sticky='nw', padx=10, pady=5)
    engine_listbox.grid(row=2, column=1, sticky='w', padx=10, pady=5)

    Label(root, text="Number of Images per Term:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
    Entry(root, textvariable=num_images_var, width=10).grid(row=3, column=1, sticky='w', padx=10, pady=5)

    Label(root, text="Number of Threads:").grid(row=4, column=0, sticky='w', padx=10, pady=5)
    Entry(root, textvariable=threads_var, width=10).grid(row=4, column=1, sticky='w', padx=10, pady=5)

    Label(root, text="Image Size Filter:").grid(row=5, column=0, sticky='w', padx=10, pady=5)
    OptionMenu(root, size_filter_var, *size_options).grid(row=5, column=1, sticky='w', padx=10, pady=5)

    Label(root, text="Image Type Filter:").grid(row=6, column=0, sticky='w', padx=10, pady=5)
    OptionMenu(root, type_filter_var, *type_options).grid(row=6, column=1, sticky='w', padx=10, pady=5)

    Button(root, text="Start Crawling", command=start_crawling).grid(row=7, columnspan=3, pady=20)

    Label(root, text="Status:").grid(row=8, column=0, sticky='nw', padx=10, pady=5)
    status_box.grid(row=9, column=0, columnspan=3, padx=10, pady=5)

    Button(root, text="Export Log", command=export_log).grid(row=10, columnspan=3, pady=5)

    # Add progress bar
    progress_bar.grid(row=11, column=0, columnspan=3, padx=10, pady=10, sticky='we')

# Main
root = Tk()
root.title("[Machine Learning] Image Crawler")

# Variables
search_terms_var = StringVar()
directory_var = StringVar()
num_images_var = IntVar(value=10)
threads_var = IntVar(value=1)
size_filter_var = StringVar()
type_filter_var = StringVar()

# Options
size_options = ["", "large", "medium", "small"]
type_options = ["", "photo", "clipart", "lineart", "animated"]

engine_listbox = Listbox(root, selectmode=MULTIPLE, height=3, exportselection=False)
for engine in ["Google", "Bing", "Baidu"]:
    engine_listbox.insert(END, engine)

status_box = ScrolledText(root, state=DISABLED, width=80, height=20)
progress_var = IntVar()  # Progress tracking variable
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)

# Initialize GUI
create_gui()
root.mainloop()
