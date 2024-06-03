import pytest
import builtins
from emoji_enhancer.cli import main

def test_main(monkeypatch, capsys):
    """
    Test the main function of the CLI.
    """
    # Mock command-line arguments
    test_args = ['cli.py', 'She likes apple.', '-n']
    monkeypatch.setattr('sys.argv', test_args)

    # Mock user input to select the first emoji option
    inputs = iter(['1'])  # User selects the first emoji option for 'apple'
    monkeypatch.setattr(builtins, 'input', lambda _: next(inputs))

    # Run the main function
    main()

    # Capture printed output
    captured = capsys.readouterr()

    # Check if the expected output is in the captured output
    assert "Options for apple:" in captured.out
    # Check example emoji, adjust based on actual emoji returned
    assert "1. 🍎" in captured.out  
    # Check expected revised text
    assert "Revised text: She likes apple🍎" in captured.out  

