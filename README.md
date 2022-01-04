# clipboard_watcher
Watches the clipboard for urls

Run clipper.py from the command line. It will write all copied urls to a text file named "clipper.txt" in the same directory. Only copy one url at a time. All command line arguments are ignored.

# dependencies
Install all dependencies

    pip install -r requirements.txt

# cx_freeze
Build executable

    setup.py build_exe

Build MSI installer

    setup.py bdist_msi