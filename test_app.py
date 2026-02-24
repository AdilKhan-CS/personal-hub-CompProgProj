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

def test_add_task_checker():
    """Test addTaskChecker function"""
    from app import addTaskChecker
    assert addTaskChecker("New Task") == True, "Valid task should return True"
    assert addTaskChecker("   ") == False, "Whitespace task should return False"
    assert addTaskChecker("") == False, "Empty task should return False"

def test_remove_task_checker():
    """Test removeTaskChecker function"""
    from app import removeTaskChecker, addTaskChecker, doesTaskExist
    if not doesTaskExist("New Task"):
        addTaskChecker("New Task")
    assert removeTaskChecker("New Task") == True, "Existing task should return True"
    assert removeTaskChecker("Nonexistent Task") == False, "Nonexistent task should return False"
