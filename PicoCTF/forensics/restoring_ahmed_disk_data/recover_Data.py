
# import os
# import shutil
# import time

# # ============================
# # CONFIGURATION
# # ============================
# SOURCE_DIR = r"E:\\restored_data"                  
# DEST_DIR   = r"F:\\"                  

# IMG_EXT      = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp"}
# DOC_EXT      = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}
# VIDEO_EXT    = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"}
# SOUND_EXT     = {".mp3", ".wav", ".aac", ".m4a", ".ogg"}
# ZIPPED_EXT    = {".zip", ".rar", ".7z", ".tar", ".gz"}

# MAX_OTHER_FOLDER_SIZE = 1 * 1024 * 1024 * 1024   # 1GB


# # ============================
# # HELPERS
# # ============================

# def ensure_folder(path):
#     if not os.path.exists(path):
#         os.makedirs(path)

# def get_folder_size(path):
#     total = 0
#     for root, dirs, files in os.walk(path):
#         for f in files:
#             fp = os.path.join(root, f)
#             try:
#                 total += os.path.getsize(fp)
#             except:
#                 pass
#     return total

# def get_or_create_other_subfolder():
#     others_base = os.path.join(DEST_DIR, "Others")
#     ensure_folder(others_base)

#     i = 1
#     while True:
#         candidate = os.path.join(others_base, f"Part_{i}")
#         ensure_folder(candidate)
#         if get_folder_size(candidate) < MAX_OTHER_FOLDER_SIZE:
#             return candidate
#         i += 1


# # ============================
# # MAIN SCRIPT
# # ============================
# now = time.time()
# print("Starting file sorting...")

# ensure_folder(DEST_DIR)

# IMG_DIR    = os.path.join(DEST_DIR, "imgs")
# DOC_DIR    = os.path.join(DEST_DIR, "documents_and_presentations")
# VIDEO_DIR  = os.path.join(DEST_DIR, "videos")
# SOUND_DIR  = os.path.join(DEST_DIR, "sounds")
# ZIPPED_DIR = os.path.join(DEST_DIR, "zipped_files")

# for d in [IMG_DIR, DOC_DIR, VIDEO_DIR, SOUND_DIR, ZIPPED_DIR]:
#     ensure_folder(d)

# # Loop through recup_dir folders
# for folder in os.listdir(SOURCE_DIR):
#     folder_path = os.path.join(SOURCE_DIR, folder)
#     if not os.path.isdir(folder_path):
#         continue

#     print(f"[+] Scanning {folder}")

#     for file in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, file)

#         if not os.path.isfile(file_path):
#             print(f'[-] Skipping non-file: {file_path}')
#             continue

#         ext = os.path.splitext(file)[1].lower()

#         # IMAGE
#         if ext in IMG_EXT:
#             shutil.move(file_path, os.path.join(IMG_DIR, file))

#         # DOCUMENT
#         elif ext in DOC_EXT:
#             shutil.move(file_path, os.path.join(DOC_DIR, file))

#         # VIDEO
#         elif ext in VIDEO_EXT:
#             shutil.move(file_path, os.path.join(VIDEO_DIR, file))

#         # SOUND
#         elif ext in SOUND_EXT:
#             shutil.move(file_path, os.path.join(SOUND_DIR, file))
#         # ZIPPED
#         elif ext in ZIPPED_EXT:
#             shutil.move(file_path, os.path.join(ZIPPED_DIR, file))

#         # OTHERS (1GB per subfolder)
#         else:
#             target_folder = get_or_create_other_subfolder()
#             shutil.move(file_path, os.path.join(target_folder, file))
#     print(f' time taken for this folder: {time.time() - now}')
#     now = time.time()

# print("\nDONE! All files sorted successfully.")


## Multithreaded version: 
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ============================
# CONFIGURATION
# ============================
SOURCE_DIR = r"E:\\restored_data"
DEST_DIR   = r"F:\\"

IMG_EXT   = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp"}
DOC_EXT   = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}
VIDEO_EXT = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"}
SOUND_EXT = {".mp3", ".wav", ".aac", ".m4a", ".ogg"}
ZIPPED_EXT = {".zip", ".rar", ".7z", ".tar", ".gz"}

MAX_OTHER_FOLDER_SIZE = 1 * 1024 * 1024 * 1024   # 1GB

# GLOBAL LOCK
other_lock = Lock()
folder_size_cache = {}


# ============================
# HELPERS
# ============================
def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def get_folder_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except:
                pass
    return total


def get_or_create_other_subfolder():
    """
    Ensure we safely pick a Part_N folder without race conditions.
    """
    with other_lock:
        base = os.path.join(DEST_DIR, "Others")
        ensure_folder(base)

        i = 1
        while True:
            folder = os.path.join(base, f"Part_{i}")
            ensure_folder(folder)

            if folder not in folder_size_cache:
                folder_size_cache[folder] = get_folder_size(folder)

            if folder_size_cache[folder] < MAX_OTHER_FOLDER_SIZE:
                return folder

            i += 1


# ============================
# WORKER FUNCTION
# ============================
def process_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    file = os.path.basename(file_path)

    # Destination folders
    if ext in IMG_EXT:
        target = IMG_DIR
    elif ext in DOC_EXT:
        target = DOC_DIR
    elif ext in VIDEO_EXT:
        target = VIDEO_DIR
    elif ext in SOUND_EXT:
        target = SOUND_DIR
    elif ext in ZIPPED_EXT:
        target = ZIPPED_DIR
    else:
        target = get_or_create_other_subfolder()

    try:
        shutil.move(file_path, os.path.join(target, file))

        # Update folder size cache
        if "Others" in target:
            with other_lock:
                folder_size_cache[target] += os.path.getsize(os.path.join(target, file))
    except Exception as e:
        print(f"Error moving {file_path}: {e}")


# ============================
# MAIN SCRIPT
# ============================
start = time.time()

# Ensure base folders
IMG_DIR   = os.path.join(DEST_DIR, "imgs")
DOC_DIR   = os.path.join(DEST_DIR, "documents_and_presentations")
VIDEO_DIR = os.path.join(DEST_DIR, "videos")
SOUND_DIR = os.path.join(DEST_DIR, "sounds")
ZIPPED_DIR = os.path.join(DEST_DIR, "zipped_files")

for d in [IMG_DIR, DOC_DIR, VIDEO_DIR, SOUND_DIR, ZIPPED_DIR]:
    ensure_folder(d)

print("Starting parallel sorting...")

file_tasks = []

# Collect all files first
for folder in os.listdir(SOURCE_DIR):
    folder_path = os.path.join(SOURCE_DIR, folder)
    if not os.path.isdir(folder_path):
        continue

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            file_tasks.append(file_path)

print(f"Total files: {len(file_tasks)}")

# PROCESS WITH THREADPOOL
with ThreadPoolExecutor(max_workers=16) as executor:
    futures = [executor.submit(process_file, f) for f in file_tasks]

    for fut in as_completed(futures):
        pass

print("DONE! Time:", time.time() - start, "seconds")
