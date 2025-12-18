"""
Basic Tests for Computer Networks Chat Application
Tests basic functionality without requiring GUI
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import socket
        print("✓ socket module available")
    except ImportError:
        print("✗ socket module not available")
        return False
    
    try:
        import threading
        print("✓ threading module available")
    except ImportError:
        print("✗ threading module not available")
        return False
    
    try:
        import json
        print("✓ json module available")
    except ImportError:
        print("✗ json module not available")
        return False
    
    try:
        import base64
        print("✓ base64 module available")
    except ImportError:
        print("✗ base64 module not available")
        return False
    
    try:
        import datetime
        print("✓ datetime module available")
    except ImportError:
        print("✗ datetime module not available")
        return False
    
    # Note: tkinter is only needed for client GUI, skip in headless tests
    
    print("\nAll required modules available!")
    return True

def test_socket_creation():
    """Test that we can create TCP sockets"""
    print("\nTesting socket creation...")
    
    try:
        import socket
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.close()
        print("✓ TCP socket creation successful")
        return True
    except Exception as e:
        print(f"✗ Socket creation failed: {e}")
        return False

def test_json_serialization():
    """Test JSON encoding and decoding"""
    print("\nTesting JSON serialization...")
    
    try:
        import json
        
        # Test message
        message = {
            'type': 'message',
            'sender': 'TestUser',
            'content': 'Test message',
            'timestamp': '2024-01-01 12:00:00'
        }
        
        # Encode
        encoded = json.dumps(message)
        
        # Decode
        decoded = json.loads(encoded)
        
        if decoded == message:
            print("✓ JSON serialization working correctly")
            return True
        else:
            print("✗ JSON serialization mismatch")
            return False
            
    except Exception as e:
        print(f"✗ JSON serialization failed: {e}")
        return False

def test_base64_encoding():
    """Test Base64 file encoding"""
    print("\nTesting Base64 encoding...")
    
    try:
        import base64
        
        # Test data
        test_data = b"Hello, this is test file data!"
        
        # Encode
        encoded = base64.b64encode(test_data).decode('utf-8')
        
        # Decode
        decoded = base64.b64decode(encoded)
        
        if decoded == test_data:
            print("✓ Base64 encoding working correctly")
            return True
        else:
            print("✗ Base64 encoding mismatch")
            return False
            
    except Exception as e:
        print(f"✗ Base64 encoding failed: {e}")
        return False

def test_threading():
    """Test threading capability"""
    print("\nTesting threading...")
    
    try:
        import threading
        import time
        
        test_value = [0]
        
        def increment():
            test_value[0] += 1
        
        thread = threading.Thread(target=increment)
        thread.start()
        thread.join()
        
        if test_value[0] == 1:
            print("✓ Threading working correctly")
            return True
        else:
            print("✗ Threading test failed")
            return False
            
    except Exception as e:
        print(f"✗ Threading failed: {e}")
        return False

def test_server_import():
    """Test that server module can be imported"""
    print("\nTesting server module import...")
    
    try:
        # Import without running
        import server
        print("✓ Server module imports successfully")
        return True
    except Exception as e:
        print(f"✗ Server import failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("COMPUTER NETWORKS CHAT APPLICATION - BASIC TESTS")
    print("=" * 60)
    print()
    
    tests = [
        ("Import Test", test_imports),
        ("Socket Creation", test_socket_creation),
        ("JSON Serialization", test_json_serialization),
        ("Base64 Encoding", test_base64_encoding),
        ("Threading", test_threading),
        ("Server Import", test_server_import),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        print()
    
    print("=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
