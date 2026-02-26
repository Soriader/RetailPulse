from retailpulse.db import smoke_test

if __name__ == "__main__":
    result = smoke_test()
    print("DB smoke test result:", result)