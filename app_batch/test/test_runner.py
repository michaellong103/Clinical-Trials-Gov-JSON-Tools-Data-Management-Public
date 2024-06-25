import subprocess

def run_test(test_script):
    subprocess.run(["python3", test_script])

def main():
    while True:
        print("\033[33mAutomated Test Runner\033[0m")
        print("Choose a test to run:")
        print("1. Number of files in extracted vs number of files in extracted_working")
        print("2. Number of files in extracted_working vs the number of files in the cleaned folder")
        print("3. Number of clinical trials in four random folders in categorized_conditions vs the corresponding txt file")
        print("4. Number of clinical trials in each condition subdirectory in categorized_conditions vs the corresponding txt file")
        print("5. Check for .txt files larger than 10MB")
        print("6. Check files are moved from cleaned to categorized correctly")
        print("7. Go back to app_batch.py")
        print("0. Exit")
        
        choice = input("Enter the number of the test you want to run: ").strip()

        if choice == '1':
            run_test("test/test_1.py")
        elif choice == '2':
            run_test("test/test_2.py")
        elif choice == '3':
            run_test("test/test_3.py")
        elif choice == '4':
            run_test("test/test_4.py")
        elif choice == '5':
            run_test("test/test_5.py")
        elif choice == '6':
            run_test("test/test_6.py")
        elif choice == '7':
            subprocess.run(["python3", "app_batch.py"])
            break
        elif choice == '0':
            break
        else:
            print("\033[91mInvalid choice. Please enter a number from 0 to 7.\033[0m")

if __name__ == "__main__":
    main()
