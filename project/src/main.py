from Assistant import Assistant

def main():
    paths = [
            "../data/262ba704-1f02-45ea-9119-da7d33708d46_PN Rally Zemaitija 2025.md",
            "../data/614cd4e6-4cbc-4512-85ea-acaf192c3f16_6 Ekipažų saugos įranga.md"
             ]
    assistant = Assistant(paths)
    assistant.user_input()
    

if __name__ == "__main__":
    main()
