def test_import():
    """Make sure tkinter is installed"""
    try:
        import tkinter
    except:
        assert "Tkinter must be installed"

def test_python_version():
    """Correct python version"""
    import sys
    assert sys.version_info.major == 3, "Python version 3 must be installed"

def test_file_read():
    """File open and close"""
    try:
        open("data_files/movies.json", "r")
    except:
        assert "File cannot be opened, Is there a resource accessing the file?"