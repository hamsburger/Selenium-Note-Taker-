def main():
    try: 
        anotherFunction()
    except:
        print("NESTED ERROR CAUGHT")
    finally:
        print("Finished")

def anotherFunction():
    i = 1/0


if __name__ == "__main__":
    main()